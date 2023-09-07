# Legacy Information
Below, I've kept copies of previous documentation on this G4DarkBreM-style of generating signal samples.
If you are using an up-to-date version of ldmx-sw, it would be helpful to ignore the documentation below,
but it may be helpful if you need to generate signal samples when required to use an older version of ldmx-sw.

---
# v3.0.0 ldmx-sw

**Warning:** Names and source code has been moved in order to isolate this method of producing signal into its own package. These changes were applied to ldmx-sw in v3.2.1.

The signal generation is done by using a custom Geant4 physics process to interact with a "model" for how dark brem occurs.
Currently, we only have one "model" defined (the `VertexLibraryModel`), but the code structure allows for creating other models without changes to the physics process.

The dark brem process is configured using its own Python configuration class defined in the `LDMX.SimCore.dark_brem` module.
By default, the simulation is defined with a dark brem configuration that has the signal generation disabled.
The dark brem model _also_ has its own Python configuration class in order to pass it parameters.
In order to enable the signal generation, we "activate" the dark brem process by providing the mass of the dark photon in MeV and a model for the dark brem.

A standard example used is given here, this is just a code snipet where `sim` is a pre-defined `simulator` object.
```python
#Activiate dark bremming with a certain A' mass and LHE library
from LDMX.SimCore import dark_brem
db_model = dark_brem.VertexLibraryModel( lhe )
db_model.threshold = 2. #GeV - minimum energy electron needs to have to dark brem
db_model.epsilon   = 0.01 #decrease epsilon from one to help with Geant4 biasing calculations
sim.dark_brem.activate( ap_mass , db_model )
```

Usually the dark brem process needs to be biased so that the interaction occurs within the region of interest 
and at a frequent enough rate so we aren't wasting too much CPU time simulating events that aren't interesting.

A first discussion of the configurable parameters of the process and this first model is provided on 
[DocDB Document Number 6555](https://projects-docdb.fnal.gov/cgi-bin/private/ShowDocument?docid=6555).

---
# v2.3.0 ldmx-sw

**Warning:** Drastic updates done to the signal simulation apart of ldmx-sw v3.0.0.

The signal generation is done by a custom Geant4 physics process. This custom physics process `G4eDarkBremsstrahlung` has a corresponding model `G4eDarkBremsstrahlungModel` which handles most of the simulation work. The physics list entry `APrimePhysics` and the process are mainly there to conform to Geant4's framework and pass parameters to the model.

The model is written to take in LHE files that have A' vertices (like the old signal sim below) and then scale them to the actual energy of the electron (when Geant4 decides for the dark brem to happen).

The four parameters are detailed below.

- APrimeMass
  - **required**
  - This is the mass of the A' in MeV. It _must_ match the mass of the A' that the LHE files were generated with.
  - Example: `simulation.APrimeMass = 10. #MeV`
- darkbrem\_madGraphFilePath
  - **required**
  - Path to the LHE file that contains the e-->e-A' vertices.
  - Example: `simulation.darkbrem_madgraphfilepath = myVertices.lhe`
- darkbrem\_globalxsecfactor
  - Global factor to increase the dark brem cross section by.
  - The default for this optional variable is set to `1.`.
  - Example: `simulation.darkbrem_globalxsecfactor = 9000.`
- darkbrem\_method
  - The method of how the model should interpret the imported vertices.
  - Example: `simulation.darkbrem_method = 1 #Forward Only`
  - There are three options:

Method | Int to Pass | Default? | Description
--- | --- | --- | ---
ForwardOnly | 1 | Yes | Get the transverse momentum from the LHE vertex and combine it with the actual electron energy (checking to make sure the electron is still on mass shell)
CMScaling | 2 | No | Scale the LHE vertex to the actual electron energy using Lorentz boosts
Undefined | 3 | No | Use the LHE vertex as is

Each of these methods have their own positives and negatives.

Method | Positives | Negatives
--- | --- | ---
ForwardOnly | Always forward (into detector) and keeps angular distribution close to actual (LHE) distribution | Distorts the energy distribution as the electron gets further from the energy input into the LHE
CMScaling | Does not distort the energy distribution as much | May lose electrons (and A') to backwards scattering
Undefined | Mimics old simulation style, but allows Geant4 to have other processes go before the dark brem | Does not attempt to scale to the actual electron energy

The _Negatives_ category for `ForwardOnly` motivates a "dictionary" of LHE events so that we can always be "close enough" to the energy of the incoming electron. Analysis by Michael Revering (UMN) showed that "close-enough" was within 0.5-1 GeV, so using this feature is not seen as necessary for our current purposes. This feature can be implemented<sup>[1](#technical)</sup>; however, the first pass assumes only one input LHE file with a single beam energy for the electrons. 

<a name="technical">1</a>: Actually, Michael Revering already implemented this for his work on CMS. I (Tom Eichlersmith) just commented it out for easier integration into ldmx-sw. Implementing this feature would be as easy as uncommenting a section of code and change the parameter `madGraphFilePath` to mean a _directory_ of LHE files to read into the dictionary instead of a single file.
