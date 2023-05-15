---
layout: default
---

This page details all of the parameters you can use to tune the simulation to behave how you want it to.

General
---

Like any other Producer, the simulation is configured by passing parameters to it in the python configuration file.
```python
simulation.parameterKey = parameterValue
```
The parameter keys, types, accessing locations, and descriptions are documented on this page.
A minimal working example is displayed on [Generating Simulation Samples]({% link docs/Generating-Simulation-Samples.md %})

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`detector` | string | Simulator | Full path to detector gdml description
`description` | string | Simulator and RootPersistencyManager | Concise phrase describing this simulation in a human-readable way
`verbosity` | int | Simulator | Integer flag describing how verbose to be
`scoringPlanes` | string | RunManager | Full path to scoring plane gdml description
`randomSeeds` | vector of ints | Simulator | Lists random seeds to pass to Geant4
`preInitCommands` | vector of strings | Simulator | Geant4 commands to run before the run is initialized
`postInitCommands` | vector of strings | Simulator | Geant4 commands to run after the run is initialized
`enableHitContribs` | bool | RootPersistencyManager | Should the simulation allow for the different contributors to an ECal hit be stored?
`compressHitContribs` | bool | RootPersistencyManager | Should the simulation compress the contributors by combining any contributors with the same PDG ID?


Note: In earlier versions of LDMX-sw, you would set the `runNumber` parameter in
the simulator. The `runNumber` is a unique number (int) that identifies this
run. In current versions of LDMX-sw, the `runNumber` is called `run` and is set as a parameter to
the process directly. In other words, along the lines of
```python
p = ldmxcfg.Process("simulation")
p.run = 9001
```

### Biasing

Biasing is helpful for efficiently simulating the detector's response to various
events. The biasing parameters are given directly to the simulation and are
listed below.

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`biasing_enabled` | bool | DetectorConstruction and RunManager | Should we bias?
`biasing_process` | string | DetectorConstruction | Geant4 process to bias
`biasing_volume` | string | DetectorConstruction | Geant4 volume to bias inside of
`biasing_particle` | string | DetectorConstruction and RunManager | Geant4 particle to bias
`biasing_all` | bool | DetectorConstruction | Should Geant4 bias all particles of the input type?
`biasing_incident` | bool | DetectorConstruction | Should Geant4 bias only the incident particle of the input type?
`biasing_disableEMBiasing` | bool | DetectorConstruction | Should Geant4 disable down-biasing EM?
`biasing_threshold` | double | DetectorConstruction | Minium energy threshold to bias (MeV)
`biasing_factor` | int | DetectorConstruction | Factor to multiply cross-section by

In v3.0.0 of ldmx-sw, we transitioned the biasing operators to be configured by their own Python classes.
Those operators are stored in the `SimCore.bias_operators` module and are attached to the `simulator` class similar to generators and actions.
```python
# config script snippet example for biasing
from LDMX.SimCore import bias_operators
# Enable and configure the biasing
#   In order to conform to older samples,
#   we can only attach to some of the volumes in the ecal
#   so we ask for this operator to be attached to the 'old_ecal'
sim.biasing_operators = [ 
  bias_operators.PhotoNuclear('old_ecal',450.,2500.,only_children_of_primary = True) ]
```

### Dark Brem Process (Signal)

The signal generation is done by enabling the dark bremsstrahlung process in Geant4.
We do this using another Python configuration class `DarkBrem` in the `SimCore.dark_brem` module.
A more full description of the Dark Brem process and how these parameters affect its abilities is described [on its own page]({% link docs/Dark-Brem-Signal-Process.md %}).
The most direct way of starting the dark brem process is to simply activate by providing the minimal parameters for it to run.
```python
# config script snipet example for dark brem
from LDMX.SimCore import dark_brem
db_model = dark_brem.VertexLibraryModel( lhe )
db_model.threshold = 2. #GeV - minimum energy electron needs to have to dark brem
db_model.epsilon   = 0.01 #decrease epsilon from one to help with Geant4 biasing calculations
sim.dark_brem.activate( ap_mass , db_model )
```

UserActions
---

Because of the wide variety and flexibility of Geant4's UserActions, 
we have implemented a way for these various classes to all be passed along with their parameters.
This method is extremely similar to how you create Event Processors and give them parameters.
The best way to illustrate how to use one is with an example:
```python
# First create the UserAction using the simcfg module
from LDMX.Biasing import filters
target_brem_filter = filters.TargetBremFilter() #import template
# Set the parameters that the UserAction uses
# the template provides reasonable defaults, but you can change them
target_brem_filter.recoilEnergyThreshold = 1500. #MeV - maximum recoil electron energy
target_brem_filter.bremEnergyThreshold = 2500. #MeV - minimum brem energy
# Then give the UserAction to the simulation so that it knows to use it
simulation.actions.append( target_brem_filter )
```
No matter the UserAction, the last line above is how you tell the simulation to use it.

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`actions` | vector of UserActions | RunManager | UserActions to plug into simulation

The details of how each UserAction works and what parameters are used are (read: should be) documented within each of those classes. Hopefully, we will get around to documenting the UserActions and how to use them. Right now, we have a list of UserActions that have their own template.

### Filters

These UserActions filter for specific behavior in the simulation. Some of them abort an event if certain criteria aren't met and others make sure tracks matching certain criteria are saved into the output simulation file.

Access with: `from LDMX.Biasing import filters`

The first type of filter aborts events if certain requirements aren't met.

Filter | Requirement on Event
---|---
`TargetBremFilter()` | "hard-enough" brem in the target (hard-enough defined by the parameters)
`EcalProcessFilter()` | PN interaction happens in the ECal
`TargetENFilter()` | EN interaction happens in the Target
`TargetPNFilter()` | PN interaction happens in the target
`DarkBremFilter()` | dark brem happens in the target
`TaggerVetoFilter()` | Primary electron doesn't lose fall below 3.8 GeV before reaching target

The other type of filter looks for tracks (what Geant4 call's individual particles) in Geant4 that match certain conditions and tell Geant4 (and our simulation) to save them in the output SimParticles collection.

Filter | Keeps all tracks...
---|---
`TrackProcessFilter.photo_nuclear()` | produced by the PN interaction
`TrackProcessFilter.electro_nuclear()` | produced by the EN interaction
`TrackProcessFilter.dark_brem()` | produced by a dark brem

Generators
---
There are a few general options that determine how primaries are generated. These parameters must be passed directly to the simulation (like the biasing parameters).

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`beamSpotSmear` | vector of doubles | PrimaryGeneratorAction | Define how much to smear the primary vertex in each of the Cartesian directions (x,y,z)
`generators` | vector of PrimaryGenerators | PrimaryGeneratorManager | List the primary generators to use in this simulation run

Like UserActions, PrimaryGenerator is a python class that you can create using the `LDMX.SimCore.simcfg` python module. And actually, there are several helpful functions defined in the `LDMX.SimCore.generators` python module. These helpful functions return the correct python class and set some helpful defaults. Look at that file for more details. The most widely used primary generator is a simple one: a single 4GeV electron fired from upstream of the tagger. You could use that generator in your simulation with the following lines:
```python
from LDMX.SimCore import generators
simulation.generators = [ generators.single_4gev_e_upstream_tagger() ]
```
You can send generators parameters in the same way as EventProcessors and UserActions:
```python
myGenerator.parameterKey = parameterValue
```

Several of these generators can be used at once, although not all combinations have been tested.

A more detailed description of the parameters you can pass the various generators are listed below. All of the python code below requires the `LDMX.SimCore.generators` module to be imported:
```python
from LDMX.SimCore import generators
```

#### Simple Particle Gun

This generator is the basic Geant4 particle gun. It can shoot one particle of a definite position and momentum into the simulation. Create a ParticleGun with:
```python
myParticleGun = generators.gun( "myParticleGun" )
# set the parameters, for example, to use electrons:
myParticleGun.particle = 'e-'
```

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`particle` | string | ParticleGun | Geant4 name of particle to use
`energy` | double | ParticleGun | Energy of primary particle (GeV)
`position` | vector of doubles | ParticleGun | Location to shoot particle from (mm)
`time` | double | ParticleGun | Time at which to shoot particle (ns)
`direction` | vector of doubles | ParticleGun | Direction to shoot particle (unit-less)

#### LHE vertices as primaries

This generator copies the primary vertex from an LHE file into our simulation framework.
Create one with:
```python
myLHE = generators.lhe( "myLHE" , "<path-to-LHE-file>" )
```

#### Root Re-sim from ECal Scoring Planes

_Note: unverified._

This generator re-simulates the event using the particles leaving the ECal scoring planes (heading into the HCal). Create one with:
```python
myReSimFromECal = generators.ecalSP( "myReSimFromECal" , "<path-to-root-file>" )
```
You also have access to the following variables if you need to tell the generator which scoring planes hits collection to use. These parameters are given reasonable defaults.

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`collection_name` | string | RootSimFromEcalSP | Name of ECal Scoring Planes Hits collection created by simulation
`pass_name` | string | RootSimFromEcalSP | Name of pass that generated the collection you want to use
`time_cutoff` | double | RootSimFromEcalSP | Maximum time to allow for a particle to to leave the ECal and be included in this re-sim

#### Root Re-sim from primaries

_Note: unverified._

This generator complete re-simulates the event from the original primary particles. Create one with:
```python
myCompleteReSim = generators.completeReSim( "myCompleteReSim" , "<path-to-ROOT-file>" )
```
Similar to the previous generator, you also have access to the following variables if you need to tell the generator which SimParticles collection to use. These parameters are given reasonable defaults.

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`collection_name` | string | RootCompleteReSim | Name of SimParticles collection created by simulation
`pass_name` | string | RootCompleteReSim | Name of pass that generated the collection you want to use

#### Geant4's General Particle Source

This generator is the "General Particle Source". It is implemented in Geant4, and has too many parameters to copy over into our framework. This means you will pass the GPS commands as strings that will be given to Geant4.
Create one with:
```python
myGPS = generators.gps( "myGPS" )
# set initCommands
```

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`initCommands` | vector of strings | GeneralParticleSource | List of Geant4 commands to configure the General Particle Source

#### Multiple Particle Gun

This generator can generate multiple copies of the same primary particle with the same kinematics. The number of primaries it generates can also be Poisson distributed. Create one with:
```python
myMPG = generators.multi( "myMPG" )
# set the parameters
```
Here are the parameters you have access to:

Parameter | Type | AccessedBy | Description
--- | --- | --- | ---
`nParticles` | int | MultiParticleGunPrimaryGenerator | number of particles to create (or the mean of the Poisson distribution)
`enablePoisson` | bool | MultiParticleGunPrimaryGenerator | Should the number of particles be Poisson distributed?
`pdgID` | int | MultiParticleGunPrimaryGenerator | PDG ID of the particle(s) to be the primary
`vertex` | vector of doubles | MultiParticleGunPrimaryGenerator | location of primary vertex to shoot the particle(s) from (mm)
`momentum` | vector of doubles | MultiParticleGunPrimaryGenerator | 3-momentum of primary particle(s) (MeV)


Photonuclear model
---

The hadronic interaction used by Geant4 in ldmx-sw to perform photonuclear
interactions can be configured to load an arbitrary other model from a dynamic
library. There are a couple available within ldmx-sw that are listed here but
you can add new ones from any library and load them the same way. For details
about this, see [Alternative Photo Nuclear Models]({% link
docs/Alternative-Photo-Nuclear-Models.md %}).

By default, the simulation will be configured to use the default version of the
Bertini model that comes with LDMX's version of Geant4. If you want to change to
a different model, you can do so through

```python
from LDMX.SimCore import photonuclear_models as pns
simulation.photonuclear_model = pns.SomeModel()
```

Note that some of these models should probably be used together with a
corresponding filter from `Biasing.particle_filter`.

| Model | Corresponding filter | Description |
--- | --- | --- 
| `BertiniModel`                 | None                                               | Default                                                                                                                                          |
| `BertiniNothingHardModel`      | `PhotoNuclearTopologyFilter.NothingHardFilter()`   | A model that forces high energy PN interactions with heavy nuclei to produce events where no product has more than some threshold kinetic energy |
| `BertiniSingleNeutronModel`    | `PhotoNuclearTopologyFilter.SingleNeutronFilter()` | Similar, but requires exactly one neutron with kinetic energy above the threshold. By default, is applied to interactions with any nucleus.      |
| `BertiniAtLeastNProductsModel` | A matching version of`PhotoNuclearProductsFilter`  | Similar, but requires at least N particles of a list of particle IDs (e.g. kaons) in the final state.                                            |




