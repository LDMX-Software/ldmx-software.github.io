# Simulation from Scoring Plane Hits

~~~admonish note title="Not Re-Sim"
The `FromScoringPlane` generator is mainly focused on doing "two stage" simulation
where _replication_ is not required.  If you want to **fully replicate**
past events within an input file, you should use the [re-simulation
infrastructure](resim.md).
~~~

Two-stage simulation is helpful when two parts of the simulation are
physically separate enough that the physical effects are approximately one direction.
For example, the tracking, target, and trigger scintillator ("tracking") region compared
to the ecal and hcal ("calorimeter") region. These two regions are separated into two distinct
areas along the beam line and (excluding the lower rate and lower energy "backsplash"),
particles pass through the upstream region and then pass through the downstream
calorimeter region.
Another example would be if we wanted to simulate some beamline components upstream
of our detector apparatus.

Since these two stages are physically separate, we can simulate them separately and
get physically-reasonable events (even if the events we simulate are not identical
to if we simulated the two regions together at once).
Below, I walk through an example of doing a two-stage simulation where we first
simulate the tracking region alone and then simulate the calorimeter region.
We separate out the tracking region because, since it has less mass in the detector,
it doesn't cause the beam particle to shower and so the simluation has less particles
to deal with and therefore completes much faster.
In this way, we can simulate many more events in the tracking region and then
filter out events from that sample that are particularly troublesome that we
want to study in more detail with the calorimeter simulation as well.

## Stage One: "simtrk"
In this stage, we do a normal simulation but we omit the detector volumes
and sensitive detectors (SDs) that are not within the region we care about.
The tracking region already has a GDML detector model constructed that is
equivalent to the full v14 detector but without the two calorimeters,
so we can just use that model.

For example,
```python
from LDMX.SimCore import simulator, generators, sensitive_detectors
sim = simulator.simulator('sim')
sim.setDetector('ldmx-det-v14-8gev-no-cals')
sim.generators = [
    generators.single_8gev_e_upstream_tagger()
]
sim.description = 'single electron 8gev beam, no calorimeters, no biasing or filtering'
# manually add the sensitive detectors that we want
sim.sensitive_detectors = [
    sensitive_detectors.TrackerSD.tagger(),
    sensitive_detectors.TrackerSD.recoil(),
    sensitive_detectors.TrigScintSD.target(),
    sensitive_detectors.TrigScintSD.pad1(),
    sensitive_detectors.TrigScintSD.pad2(),
    sensitive_detectors.TrigScintSD.pad3(),
    sensitive_detectors.ScoringPlaneSD.tracker(),
    sensitive_detectors.ScoringPlaneSD.target(),
    sensitive_detectors.ScoringPlaneSD.ecal(),
    sensitive_detectors.ScoringPlaneSD.hcal()
]
sim.beamSpotSmear = [20.0, 80.0, 0.0] # mm
```
We want to remove all of the SDs that pertain to subsystems we are not
including (e.g. `EcalSD` and `HcalSD` are omitted), but we do want to
include the scoring planes for the area from which we want to start
stage two (in this case, `ScoringPlaneSD.hcal()` contains one "plane"
at the front of the calorimeter region, `ScoringPlaneSD.ecal()` has
a similar one but it is not as large in the transverse direction).

## Stage Two: "simcal"
The `FromScoringPlane` generator requires an input file to be given to the
process so that (a) the prior pass's information is copied into the output
file for analysis and (b) so this generator can access the prior
pass's scoring plane hits to start the second stage of simulation.

You should also make sure the pass name is different for the stage two run so that both sets of simulation collections (e.g. `SimParticles`) are able to be stored in the output event file.
```python
p = ldmxcfg.Process("simcal")
p.input_files = ["output-file-from-stage-one.root"]
```

And then the simulation can use the special generator that uses hits from the input file to create primary particles.

```python
# sim is a normal simulator.Simulator
from LDMX.SimCore.generators import FromScoringPlane
sim.generators = [
    FromScoringPlane(
        # default is EcalScoringPlaneHits but you can use
        # the HcalSP if they are available
        coll_name = "HcalScoringPlaneHits",
        # usually you want to choose the front plane
        # 31 for EcalSP, 41 for HcalSP
        select_planes = [41]
    )
]
```

You can do a similar thing as stage one where you tune the `sim.sensitive_detectors` to only the subsystems that are of-interest in this stage. Technically, that is not necessary but it would be helpful to avoid downstream confusion during analysis.

### Analysis Comments
The file output by "Stage Two" of the simulation is complicated since it was constructed in a abnormal way.

**Be Careful with Pass Names**: Remember that both stages could have contributed a collection with the same name, so make sure the two stages have different pass names and you choose the correct pass name when analyzing the resulting file. For example, I know that the `RecoilSimHits` collection from the `simcal` pass will only be back-splash hits while the `RecoilSimHits` collection from the `simtrk` pass will be near-normal.
