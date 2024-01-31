# Layer Weights

As a sampling calorimeter, the ECal needs to apply weights to all of the energies
it measures in order to account for the energy "lost" from particles traversing
material that is not active or sensitive. The ECal has sensitive silicon layers
that are actually making energy measurements while the rest of the material
(tungsten plates, cooling planes, printed circuit boards "PCB") are here treated
as "absorber".

Reconstructing the amount of energy deposited within a cell inside the sensitive
silicon is another topic, largely a question of interpreting the electronic signals
readout using our knowledge of the detector. This document starts with the assumption
that we already have an estimate for the amount of energy deposited in the silicon.

~~~admonish tip title="Energy Deposited in Silicon"
I am being intentionally vague here because the estimate for the energy deposited
in the silicon can be retrieved either from the `EcalRecHits` or the `EcalSimHits`.
The simulated hits exclude any of the electronic estimation and so are, in some
sense, less realistic; however they could be used to assign blame to energies within
the ECal which is helpful for some studies.

The estimated energy deposited in the silicon is stored in different names in these
two classes.
- `amplitude_` member variable of `EcalHit` (`getAmplitude()` accessor in C++)
- `edep_` member variable of `EcalSimHit` (`getEdep()` accessor in C++)
~~~

Our strategy to account for the absorbing material is to calculate a scaling factor \\(S\\)
increasing the energy deposited in the silicon \\(E_\text{silicon}\\) up to a value that estimates the
energy deposited in all of the absorbing material in front of this silicon layer
up to the next sensitive silicon layer \\(E_\text{absorber}\\). This strategy allows us to keep the relatively
accurate estimate of the energy deposited in the silicon as well as avoids double
counting absorber layers by uniquely assigning them to a single silicon sensitive layer.

\\[
  E_\text{absorber} \approx S E_\text{silicon}
\\]

We can estimate \\(S\\) by using our knowledge of the detector design and measurements of how
much energy particles lose inside of these materials. Many of the measurements of how much energy
is lost by particles is focused on "minimum-ionizing particles" or MIPs and so we factor this
out by first estimating the number of MIPs within the silicon and then multiplying that number
by the estimate energy loss per MIP in the absorbing material.

\\[
  S = L / E_\text{MIP in Si}
  \quad\Rightarrow\quad
  E_\text{absorber} \approx L \frac{E_\text{silicon}}{E_\text{MIP in Si}}
\\]

The \\(L\\) in this equation is what the layer weights stored within are software represent.
They are the estimated energy loss of a single MIP passing through the absorbing layers in
front of a silicon layer up to the next silicon layer.

~~~admonish note collapsible=true title="Calculating the Layer Weights"
The [`Detectors/util/ecal_layer_stack.py`](https://github.com/LDMX-Software/ldmx-sw/blob/trunk/Detectors/util/ecal_layer_stack.py)
python script calculate these layer weights as well as other aspects of the ECal detector design.
It copies the \\(dE/dx\\) values estimated within the PDG for the materials within our design
and then uses a coded definition of the material layers and their thicknesses to calculate
these layer weights as well as the positions of the sensitive layers.
~~~

Using this estimate for the energy deposited into the absorbing material, we can combine it
with our estimate of the energy deposited into the sensitive silicon to obtain a "total energy"
represented by a single hit.

\\[
  E = E_\text{absorber}+E_\text{silicon}
    \approx L E_\text{silicon} / E_\text{MIP in Si} + E_\text{silicon}
    = \left(1 + \frac{L}{E_\text{MIP in Si}}\right) E_\text{silicon}
\\]

~~~admonish note collapsible=true title="Second Order Corrections"
From simulations of the detector design, we found that this underestimated the energy of showers
within the ECal by a few percent, so we also introduces another scaling factor \\(C\\)
(called `secondOrderEnergyCorrection` in the reconstruction code) that multiplies this total
energy.

\\[
  E = C \left(1 + \frac{L}{E_\text{MIP in Si}}\right) E_\text{silicon}
\\]

This is helpful to keep in mind when editing the reconstruction code itself, but
for simplicity and understandability if you are manually applying the layer weights (e.g.
to use them with sim hits), you should not use this second order correction (i.e. just keep \\(C=1\\)).
~~~

Now that we have an estimate for the total energy represented by a single hit,
we can combine energies from multiple hits to obtain shower or cluster "features".

## Applying the Layer Weights
In many cases, one can just use the `energy_` member variable of the `EcalHit` class to get
this energy estimate (including the layer weights) already calculated by the reconstruction;
however, in some studies it is helpful to apply them manually. This could be used to study
different values of the layer weights or to apply the layer weights to the `EcalSimHits`
branch in order to estimate the geometric acceptance (i.e. neglect any electronic noise and
readout affects).

This section focuses on how to apply the layer weights within a python-based analysis
which uses the `uproot` and `awkward` packages. We are going to assume that you (the
user) have already loaded some data into an `ak.Array` with a form matching
```
N * var * {
  id: int32,
  amplitude: float32
  ... other stuff
}
```
The `N` represents the number of events and the `var` signals that this array has a
variable length sub-array. I am using the `EcalHit` terminology (i.e. `amplitude`
represents the energy deposited in just the silicon), but one could use the following
code with sim hits as well following a name change. You can view this form within
a jupyter notebook or by calling `show()` on the array of interest.

~~~admonish tip collapsible=true title="Loading Data into `ak.Array`"
Just as an example, here is how I load the `EcalRecHits` branch from a pass named
`example`.
```python
import uproot
import awkward as ak
f = uproot.open('path/to/file.root')
ecal_hits = f['LDMX_Events'].arrays(expressions = 'EcalRecHits_example')
# shorten names for easier access, just renaming columns not doing any data manipulation
ecal_hits = ak.zip({
    m[m.index('.')+1:].strip('_') : ecal_hits.EcalRecHits_valid[m]
    for m in ecal_hits.EcalRecHits_example.fields
})
```
~~~

From here on, I assume that the variable `ecal_hits` has a `ak.Array` of data
with a matching form.

### Obtain Layer Number
First, we need to obtain the layer number corresponding to each hit. This can be
extracted from the detector ID that accompanies each hit.
```python
ecal_hits["layer"] = (ecal_hits.id >> 17) & 0x3f
```
~~~admonish warning title="Bit Shifting Nonsense"
This bit shifting nonsense was manually deduced from the
[`ECalID` source code](https://github.com/LDMX-Software/ldmx-sw/blob/trunk/DetDescr/include/DetDescr/EcalID.h)
and should be double checked.
The layers should range in values from `0` up to the number
of sensitve layers minus one (currently `33`).

If you are running from within the ldmx-sw development or production container
(i.e. have access to an installation of `fire`), you could also do
```python
from libDetDescr import EcalID
import numpy as np
@np.vectorize
def to_layer(rawid):
    return EcalID(int(rawid)).layer()
```
to use the C++ code directly. This is less performant but is more likely to
be correct.
~~~

### Efficiently Broadcasting Layer Weights
Now, the complicated bit. We want to efficiently broadcast the layer weights
to all of the hits without having to copy around a bunch of data. `awkward`
has a solution for this we can use
[IndexedArray](https://awkward-array.org/doc/main/reference/generated/ak.contents.IndexedArray.html?highlight=indexedarray#ak.contents.IndexedArray) 
with the layer indices as the index and
[ListOffsetArray](https://awkward-array.org/doc/main/reference/generated/ak.contents.ListOffsetArray.html?highlight=listoffsetarray#ak.contents.ListOffsetArray)
with the offsets of the layers to get an `ak.Array`that presents the layer
weights for each hit without having to copy any data around.

First, store the layer weights in order by the layer they correspond to.
This is how the layer weights are stored within
[the python config](https://github.com/LDMX-Software/Ecal/blob/trunk/python/digi.py)
and so I have copied the v14 geometry values below.
```python
layer_weights = ak.Array([
    2.312, 4.312, 6.522, 7.490, 8.595, 10.253, 10.915, 10.915, 10.915, 10.915, 10.915,
    10.915, 10.915, 10.915, 10.915, 10.915, 10.915, 10.915, 10.915, 10.915, 10.915,
    10.915, 10.915, 14.783, 18.539, 18.539, 18.539, 18.539, 18.539, 18.539, 18.539,
    18.539, 18.539, 9.938
])
```
Then we use the special arrays linked above to present these layer
weights as if there is a copy of the correct one for each hit.
```python
layer_weight_of_each_hit = ak.Array(
    ak.contents.ListOffsetArray(
        ecal_hits.layer.layout.offsets,
        ak.contents.IndexedArray(
            ak.index.Index(ecal_hits.layer.layout.content.data),
            layer_weights.layout
        )
    )
)
```

### Applying Layer Weights
Now that we have an array that has a layer weight for each hit, we can go
through the calculation described above to apply these layer weights and
get an estimate for the total energy of each hit.
```python
mip_si_energy = 0.130 #MeV - corresponds to ~3.5 eV per e-h pair <- derived from 0.5mm thick Si
(1 + layer_weight_of_each_hit / mip_si_energy)*ecal_hits.amplitude
```
If you are re-applying the layer weights used in reconstruction, you can
also confirm that your code is functioning properly by comparing the array
calculated above with the energies that the reconstruction provides alongside
the `amplitude` member variable.
```python
# we need to remove the second order correct that the reconsturction applies
secondOrderEnergyCorrection = 4000. / 3940.5 # extra correction factor used within ldmx-sw for v14
ecal_hits.energy / secondOrderEnergyCorrection
```
