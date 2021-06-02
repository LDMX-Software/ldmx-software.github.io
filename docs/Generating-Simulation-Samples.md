---
layout: default
---

The generation of simulation samples is done mainly by the Geant4 package with several additions stored in the `SimCore` module of ldmx-sw. However, you do not need to know the simulation to this level of depth. The `Simulator` producer in the `SimCore` module is your messenger to run the simulation. Here, I will go through its basic usage. For more information about _all_ of the available parameters, please see the documentation on [Configuring the Simulation]({% link docs/Configuring-the-Simulation.md %}).

### Basic Usage
Running the simulation is just like any other producer in ldmx-sw. In your python configuration script, it is _required_ that you have the following lines (or equivalent):
```python
from LDMX.SimCore.simulator import simulator
mySimulator = simulator( "mySimulator" ) #create the simulator object
```
You can write your own detector description in the gdml format (if you want), but ldmx-sw already comes with several versions of the LDMX detector description. These versions are installed with it and can be accessed with some python (+ cmake!) code:
```python
mySimulator.setDetector( 'ldmx-det-v12' )
```
Okay, `mySimulator` now is created and has been given a path to an LDMX detector description.
What else is needed? Well, we need _at least_ one more thing. We need to tell the simulation _how_ to start the simulation. In Geant4 speak, this is called a "Primary Generator". In ldmx-sw, we already have several generators defined (more details on [Configuring the Simulation]({% link docs/Configuring-the-Simulation.md %})), but for this simple example, we will just import a standard generator.
```python
from LDMX.SimCore import generators
mySimulator.generators = [ generators.single_4gev_e_upstream_tagger() ]
```
Now you can add `mySimulator` to the process sequence:
```python
# p is a Process created earlier in your py config script
p.sequence = [ 
mySimulator 
#other processors?
]
```
Remember to tell the process how many events to simulate and where to put them:
```python
p.maxEvents = 10
p.outputFiles = [ "mySimulatorOutput.root" ]
```

Run: `ldmx fire myConfig.py`

### Other Available Templates
There are a lot of commonly used aspects of the simulation, so we have incorporated these common "templates" into the python interface for the simulation. 
This section is focused on listing these available templates and how to access them.

#### Generators
Access with: `from LDMX.SimCore import generators`.

This module contains functions that produce each of the generators. You should _always_ use these helper functions because sometimes the underlying naming conventions may change in future developments. More detail about the generators is in the Generators section of [Configuring the Simulation]({% link docs/Configuring-the-Simulation.md %}).

#### Biased Simulations
Several simulations with biased processes have been used frequently in the past, so we have written templates for using simulations with reasonably-defined defaults.

**Processes in ECal**
Access with: `from LDMX.Biasing import ecal`.

**Processes in Target**
Access with: `from LDMX.Biasing import target`.

Both `ecal` and `target` modules have three functions that allow you to choose which process is biased in that volume.

Function | Description
---|---
`photo_nuclear(detector,generator)` | PN process biased up and filtered for in (ecal or target)
`electro_nuclear(detector,generator)` | EN process biased up and filtered for in target
`dark_brem(massAPrime,lheFile,detector)` | Sets A' mass to massAPrime (in MeV) and uses the input LHE file as vertices for the dark brem simulation [more detail here]({% link docs/Dark-Brem-Signal-Process.md %})

### More Advanced Details
As I said earlier, you can definitely see all of the capabilities of `Simulator` by looking at the parameters that are available in the documentation (linked above). Two parameters that I would like to point out is `preInitCommands` and `postInitCommands`. These parameters are given directly to the Geant4 UI as a string, so you can still access Geant4 directly using these commands.

The hope is to remove any need for Geant4-style messengers inside of ldmx-sw, but we also don't want to re-write all of Geant4, so we provide this method for accessing the simulation library directly.

---
### Simple Configuration
Here is a simple configuration file that should generate a sample of 10 events without any biasing or signal and reconstructs the ECal and HCal hits.
```python
#simpleSim.py

# need the configuration python module
from LDMX.Framework import ldmxcfg

# Create the necessary process object (call this pass "sim")
p = ldmxcfg.Process( "sim" )

# import a template simulator and change some of its parameters
from LDMX.SimCore import generators
from LDMX.SimCore import simulator

mySim = simulator.simulator( "mySim" )
mySim.setDetector( 'ldmx-det-v12' )
mySim.generators = [ generators.single_4gev_e_upstream_tagger() ]
mySim.runNumber = 9001
mySim.description = 'I am a basic working example!'

# import chip/geometry conditions
import LDMX.Ecal.ecal_hardcoded_conditions
import LDMX.Hcal.HcalGeometry
import LDMX.Hcal.hcal_hardcoded_conditions
# import processor templates
import LDMX.Ecal.digi as ecal_digi
import LDMX.Hcal.digi as hcal_digi
# add them to the sequence
p.sequence = [
    mySim,
    ecal_digi.EcalDigiProducer(),
    ecal_digi.EcalRecProducer(),
    hcal_digi.HcalDigiProducer(),
    hcal_digi.HcalRecProducer()
    ]

# During production (simulation), maxEvents is used as the number
# of events to simulate.
# Other times (like when analyzing a file), maxEvents is used as
# a cutoff to prevent fire from running over the entire file.
p.maxEvents = 10

# how frequently should the process print messages to the screen?
p.logFrequency = 1

# I want to see all of the information messages (the default is only warnings and errors)
p.termLogLevel = 1

# give name of output file
p.outputFiles = [ "output.root" ]

# print process object to make sure configuration is correct
# at beginning of run and wait for user to press enter to start
p.pause()
```
