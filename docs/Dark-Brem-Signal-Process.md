---
layout: default
---

The signal generation is done by a custom Geant4 physics process. This custom physics process `G4eDarkBremsstrahlung` has a corresponding model `G4eDarkBremsstrahlungModel` which handles most of the simulation work. The physics list entry `APrimePhysics` and the process are mainly there to conform to Geant4's framework and pass parameters to the model.

The model is written to take in LHE files that have A' vertices (like the old signal sim below) and then scale them to the actual energy of the electron (when Geant4 decides for the dark brem to happen).

The four parameters are detailed below.

- APrimeMass
  - **required**
  - This is the mass of the A' in MeV. It _must_ match the mass of the A' that the LHE files were generated with.
  - Example: `simulation.parameters[ "APrimeMass" ] = 10. #MeV`
- darkbrem.madGraphFilePath
  - **required**
  - Path to the LHE file that contains the e-->e-A' vertices.
  - Example: `simulation.parameters[ "darkbrem.madgraphfilepath" ] = myVertices.lhe`
- darkbrem.globalxsecfactor
  - Global factor to increase the dark brem cross section by.
  - The default for this optional variable is set to `1.`.
  - Example: `simulation.parameters[ "darkbrem.globalxsecfactor" ] = 9000.`
- darkbrem.method
  - The method of how the model should interpret the imported vertices.
  - Example: `simulation.parameters[ "darkbrem.method" ] = 1 #Forward Only`
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

---
# Old Simulation Style

The old simulation style used the [LHEPrimaryGenerator]({% link docs/Configuring-the-Simulation.md %}) to setup the electron and A' as primaries. The vertex of the primaries imported from the LHE files would be smeared around the target, but the electron's energy would stay fixed at the energy simulated for the LHE files.
