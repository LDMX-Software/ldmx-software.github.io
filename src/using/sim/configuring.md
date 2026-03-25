# Configuring the Simulation

This page details some of the parameters you can use to tune the simulation to behave how you want it to.
This page is manually written and is focused on introducing folks to important parameters.
Please refer to the [Python Configuration Reference](https://ldmx-software.github.io/ldmx-sw/python/index.html) for a more complete list of parameters - many of which are documented from the code itself.

General
---

Like any other Producer, the simulation is configured by passing parameters to it in the python configuration file.
```python
simulation.parameter_name = parameter_value
```
The parameter keys, types, accessing locations, and descriptions are documented on this page.
A minimal working example is displayed on [Generating Simulation Samples](./generating.md)

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`detector` | string | Simulator | Full path to detector gdml description
`description` | string | Simulator and RootPersistencyManager | Concise phrase describing this simulation in a human-readable way
`verbosity` | int | Simulator | Integer flag describing how verbose to be
`scoring_planes` | string | RunManager | Full path to scoring plane gdml description
`pre_init_commands` | vector of strings | Simulator | Geant4 commands to run before the run is initialized
`post_init_commands` | vector of strings | Simulator | Geant4 commands to run after the run is initialized

### Biasing

Biasing is helpful for efficiently simulating the detector's response to various
events. The biasing parameters are given directly to the simulation and are
listed below.

In v3.0.0 of ldmx-sw, we transitioned the biasing operators to be configured by their own Python classes.
Those operators are stored in the `SimCore.bias_operators` module and are attached to the `Simulator` class similar to generators and actions.
```python
# config script snippet example for biasing
from LDMX.SimCore import bias_operators
# Enable and configure the biasing
sim.biasing_operators = [ 
    bias_operators.PhotoNuclear('ecal', 450., 2500., only_children_of_primary=True)
]
```

### Dark Brem Process (Signal)

The signal generation is done by enabling the dark bremsstrahlung process in Geant4.
We do this using another Python configuration class `DarkBrem` in the `SimCore.dark_brem` module.
A more full description of the Dark Brem process and how these parameters affect its abilities is described [on its own page]({% link docs/Dark-Brem-Signal-Process.md %}).
The most direct way of starting the dark brem process is to simply activate by providing the minimal parameters for it to run.
```python
# config script snipet example for dark brem
from LDMX.SimCore import dark_brem
db_model = dark_brem.G4DarkBreMModel(lhe)
db_model.threshold = 2. #GeV - minimum energy electron needs to have to dark brem
db_model.epsilon   = 0.01 #decrease epsilon from one to help with Geant4 biasing calculations
sim.dark_brem.activate(ap_mass , db_model)
```

UserActions
---

Because of the wide variety and flexibility of Geant4's UserActions, 
we have implemented a way for these various classes to all be passed along with their parameters.
This method is extremely similar to how you create Event Processors and give them parameters.
The best way to illustrate how to use one is with an example:
```python
# First create the UserAction, configuring its various parameters
from LDMX.Biasing import filters
target_brem_filter = filters.TargetBremFilter(
    recoil_max_p_threshold = 3000.0, # MeV
    brem_min_energy_threshold = 5000.0 # MeV
)
# Then give the UserAction to the simulation so that it knows to use it
simulation.actions.append( target_brem_filter )
```
No matter the UserAction, the last line above is how you tell the simulation to use it.

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`actions` | vector of UserActions | RunManager | UserActions to plug into simulation

The details of how each UserAction works and what parameters are used are (read: should be) documented within each of those classes.
There are a few user actions that do more technical things modifying how the simulation progresses.
The majority of user actions are "filters" of some kind which are explained in a bit more detail below.

### Filters

These UserActions filter for specific behavior in the simulation. Some of them abort an event if certain criteria aren't met and others make sure tracks matching certain criteria are saved into the output simulation file.

Access with: `from LDMX.Biasing import filters`

The first type of filter aborts events if certain requirements aren't met.

Filter | Requirement on Event
---|---
`TargetBremFilter()` | "hard-enough" brem in the target (hard-enough defined by the parameters)
`NonFiducialFilter()` | electron misses the ECal
`EcalProcessFilter()` | PN interaction happens in the ECal
`DeepEcalProcessFilter()` | PN interaction happens deeper (larger z) in the ECal
`TargetENFilter()` | EN interaction happens in the Target
`TargetProcessFilter()` | some specific interaction happens in the target
`TargetDarkBremFilter()` | dark brem happens in the target
`EcalDarkBremFilter()` | dark brem happens in the ECal
`TaggerVetoFilter()` | Primary electron doesn't fall below a certain energy before reaching target
`PrimaryToEcalFilter()` | make sure primary electron reaches the Ecal with a minimum energy
`MidShowerNuclearBkgdFilter()` | a minimum amount of energy goes into EN and PN interactions in the ECal
`MidShowerDiMuonBkgdFilter()` | a minimum amount of energy goes into a muon conversion in the ECal
`TaggerHitFilter()` | require a certain number of tagger tracker layers to be hit

The other type of filter looks for tracks (what Geant4 call's individual particles) in Geant4 that match certain conditions and tell Geant4 (and our simulation) to save them in the output SimParticles collection.

Filter | Keeps all tracks...
---|---
`TrackProcessFilter` | produced by a specific interaction (e.g. PN, EN, or dark brem)
`DecayChildrenKeeper` | which are children of a specific particle's decay

Generators
---
There are a few general options that determine how primaries are generated. These parameters must be passed directly to the simulation (like the biasing parameters).

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`generators` | vector of PrimaryGenerators | PrimaryGeneratorManager | List the primary generators to use in this simulation run

Like UserActions, PrimaryGenerator is a python class that you can create using the `LDMX.SimCore.simcfg` python module. And actually, there are several helpful functions defined in the `LDMX.SimCore.generators` python module. These helpful functions return the correct python class and set some helpful defaults. Look at that file for more details. The most widely used primary generator is a simple one: a single 4GeV electron fired from upstream of the tagger. You could use that generator in your simulation with the following lines:
```python
from LDMX.SimCore import generators
simulation.generators = [ generators.single_4gev_e_upstream_tagger() ]
```

Several of these generators can be used at once, although not all combinations have been tested.
All of these generators have a `beam_spot_smear` parameter that defines how to smear the primary vertex it generates in each of the Cartesian directions (x,y,z).

A more detailed description of the parameters you can pass the various generators are listed below. All of the python code below requires the `LDMX.SimCore.generators` module to be imported:
```python
from LDMX.SimCore import generators
```

#### Simple Particle Gun

This generator is the basic Geant4 particle gun. It can shoot one particle of a definite position and momentum into the simulation. Create a ParticleGun with:
```python
myParticleGun = generators.Gun( "myParticleGun" )
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
myLHE = generators.Lhe("path/to/file.lhe")
```

#### Geant4's General Particle Source

This generator is the "General Particle Source". It is implemented in Geant4, and has too many parameters to copy over into our framework. This means you will pass the GPS commands as strings that will be given to Geant4.
Create one with:
```python
myGPS = generators.Gps(
  init_commands = [
    # list of init commands for GPS messenger
  ]
)
```

Parameter | Type | Accessed By | Description
--- | --- | --- | ---
`init_commands` | vector of strings | GeneralParticleSource | List of Geant4 commands to configure the General Particle Source

#### Multiple Particle Gun

This generator can generate multiple copies of the same primary particle with the same kinematics. The number of primaries it generates can also be Poisson distributed. Create one with:
```python
myMPG = generators.Multi(
  # set the parameters
)
```
Here are the parameters you have access to:

Parameter | Type | AccessedBy | Description
--- | --- | --- | ---
`n_particles` | int | MultiParticleGunPrimaryGenerator | number of particles to create (or the mean of the Poisson distribution)
`enable_poisson` | bool | MultiParticleGunPrimaryGenerator | Should the number of particles be Poisson distributed?
`pdg_id` | int | MultiParticleGunPrimaryGenerator | PDG ID of the particle(s) to be the primary
`vertex` | vector of doubles | MultiParticleGunPrimaryGenerator | location of primary vertex to shoot the particle(s) from (mm)
`momentum` | vector of doubles | MultiParticleGunPrimaryGenerator | 3-momentum of primary particle(s) (MeV)


Photonuclear model
---

The hadronic interaction used by Geant4 in ldmx-sw to perform photonuclear
interactions can be configured to load an arbitrary other model from a dynamic
library. There are a couple available within ldmx-sw that are listed here but
you can add new ones from any library and load them the same way. For details
about this, see [Alternative photo-nuclear models](./Alternative-Photo-Nuclear-Models.md).

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
| `NoPhotoNuclearModel`          |                                                    | Removes photonuclear interactions entirely from the simulation                                                                                   |




