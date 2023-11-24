# Re-Simulation

Oftentimes it is helpful to select specific events from a sample and re-run
the full simulation of them while storing more simulation detail about what
transpired. Thanks to the excellent work by Einar Elén in
[SimCore #95](https://github.com/LDMX-Software/SimCore/pull/95) we are able
to re-run the simulation using an input file and optionally specifying
specific events to re-simulate.

## Basics
A key component of re-simulation is to keep the physics configuration of the
simulation _identical_ to what it was originally. With this in mind, the
suggested procedure is to make a copy of the original file used to run the
simulation and then make the following changes.

1. Use the previous output file as the input file
2. Tell the simulator to `resimulate` when adding it to the `p.sequence`

For change (1), I usually provide the previous output file as a command
line argument to the `fire` config script and so I have something like
this in my re-sim config.
```python
import sys
import os
p.inputFiles = [ sys.argv[1] ]
p.outputFiles = [ 'resim_'+os.path.basename(sys.argv[1]) ]
```
This writes the resim events into a file with the same name as the original
but with a `resim_` prefix added into the current directory.

For change (2), this is where you can optionally provide which events
you wish to select for re-simulation.
```python
p.sequence = [
  # sim is the simulator object created and configured earlier
  sim.resimulate(which_events = [42])
  # potentially other processors like normal
]
```
The `which_events` aregument is a integer list giving the event numbers
from that file that you wish to re-simulate. If `which_events` is not
given, then **all** of the events in the input file are re-simulated.

That's it! Running the updated copy of the simulation config will re-simulate
events from the original simulation in an identical manner. This plain re-simulation
may not be very helpful on its own, so below we have a few other modifications that
could be made to make the re-simulation more helpful.

### Running additional processors after re-simulation

After running the re-simulation, the output file will contain both the original sim-hit collection from the input file and the new one from the re-simulation. This means that if you want to run any processors after the simulation that use the collections, you either need to manually specify the re-sim pass name or drop the original collection (recommended). 

If you want to run producers after the re-simulation, it is usually easiest to do so with a separate configuration that uses the re-simulation output as an input-file and dropping the original collections during the re-simulation. 

As an example, if you wanted to run the Ecal reconstruction chain on a resimulation with pass-name "resim"

```python
# Resim config file 
p = ldmxcfg.Process('resim') 
# ...
p.inputFiles = ['original_simulation.root'] # Pass name "sim"
p.outputFiles = ['resimulation.root'] # Pass name "resim"
# Drop all collections that end with SimHits_sim
p.keep ["drop .SimHits_sim"] 
```

And later in your reconstruction config 
```python
# Resim config file 
p = ldmxcfg.Process('reconstruct') 
# ...
p.inputFiles = ['resimulation.root'] # Pass name "resim"
p.sequence = [
  ecal_digi, 
  ecal_reco
]
```

Alternatively, you can do it all in one configuration but you will have to manually specify the pass name for each processor that relies on simulated hits that you want to use. Unfortunately, different processors have different naming conventions for the pass name parameter so you will have to check manually how to do it for the processor that you are interested in.


```python
# Resim config file 
p = ldmxcfg.Process('resim') 
# ...
p.inputFiles = ['original_simulation.root'] # Pass name "sim"
p.outputFiles = ['resimulation.root'] # Pass name "resim"

# Digi producer needs the raw simhits 
ecal_digi = ...  
ecal_digi.inputPassName = 'resim' # Pick the resim version

p.sequence = [
  resim, 
  ecal_digi, 
  ecal_reco # Doesn't directly rely on simhits, so doesn't need pass name to be specified!
]
```

The latter approach gets cumbersome if you want to use more than a couple of processors.

## Storing all Simulated Particles
The shower that happens in the calorimeters often creates many hundreds or even thousands
of simulated particles. Thus we cannot save all of the simulated particles for all of our
events - otherwise we would run out of storage space on our computers! We get around this
issue by only saving a select group of particles during normal simulation which satisfy
one (or more) of the following.

1. The simulated particle is one of the primary particles
    - This is determined by the generators the user provides to the simulation.
2. The simulated particle is created in a region with `StoreTrajectories` set to `true`
    - This is set within the GDML of the detector where we define regions.
      In all of the current detectors, all of the regions will store trajectories _except_
      the calorimeters.
3. The simulated particle has its `SaveFlag` set to `true`
    - This is determined by any extra `UserAction`s the simulation has attached to it.

Currently, we do not have any `UserAction`s which set the `SaveFlag` to `false` because
`UserAction`s which are looking for particular simulated particles are usually trying
to get around the bulk "veto" imposed by the simulation throwing away simulated particles
that were created within the calorimeter region (either the ECal or the HCal). If your
simulation configuration has no `UserAction`s setting the `SaveFlag` to `false` (which
is highly likely), then we can insure that the simulation saves _all_ of the simulated
particles by setting `StoreTrajectories` to `true` _everywhere_.

First, make a local copy of the detector you are simulating so that you can reference it
within the config script.
```
cp path/to/ldmx-sw/install/data/detectors/<detector-name>/detector.gdml .
```
Update this detector to have all `StoreTrajectories` flags set to `true`.
```
sed -i '/StoreTrajectories/ s/false/true/g' detector.gdml
```
Finally, update the re-simulation config to use this slightly modified detector instead
of the original copy at the install location.
```python
# above we construct the simulator object sim
sim.setDetector( '<detector-name>' )
# update the path to use the new root detector.gdml with updated flags
#   here, we use a relative path and so we must run the config from the
#   directory where the edited detector.gdml is
sim.detector = 'detector.gdml'
```

Now when the re-simulation is run, all of the simulated particles will be in the
output file giving you as much detail about the particles and the processes that
they underwent as we can give from ldmx-sw (without modifying the C++ source code).

As mentioned earlier, this stores _a lot_ of particles (most of which are not important),
so this should only be done on small numbers of events (less than 100) to avoid the
files from getting too large and unweildy. In a production scenario, it would be better
to write your own `UserAction` which finds the particles that interest you rather than
storing all of the particles that are created.

## No Merging of Ecal Simulated Hits
Similar to the simulated particles, the number of simulated hits in the ECal is generally
too large and so we do a somewhat complicated procedure of merging them in order to reduce
the size of the output data file. There is a standing issue focused on improving this
merging algorithm [SimCore #31](https://github.com/LDMX-Software/SimCore/issues/31) and
if that issue is resolved, the parameters of the merging will likely change.

The `EcalSD` class is what handles each of the simulated hits created while Geant4 is
processing an event. It has two parameters for modifying how these hits should be
created.

- `enableHitContribs`, if `True`, allows `EcalSD` to create `SimCalorimeterHit` "contribs"
  when more than one hit occurs within the same Ecal cell. If `False`, all hits within a cell
  are combined by summing their respective energy deposits and choosing the earliest time.
  - The default is `True`.
- `compressHitContribs` is only used is `enableHitContribs` is `True`. If `compressHitContribs`
  is `True`, then a new contrib is only created for unique simulated particles. In other words,
  a contrib for a specific simulated particle is updated with more energy deposited and another
  deposit time if another hit is made by that simulated particle in the same ECal cell. If `False`,
  a new contrib is created for all simulated hits regardless on if any of the contribs originate
  from the same simulated particle.

The `compressHitContribs` is the parameter which causes the most confusion when interpreting ECal
simulated hit information and so removing it will give you a contrib for each simulated hit created
by Geant4 within the ECal. The code to put into your re-sim config is below.
```python
# sim is a simulator object created earlier
# must be done _after_ sim.setDetector is called
for sd in sim.sensitive_detectors:
    if 'EcalSD' in sd.class_name:
        sd.compressHitContribs = False
```

> Warning: The ECal digi-emulation and reconstruction pipeline has only been developed and tested
> with the default settings of the simulated hit merging. This means you should probably remove
> the ECal pipeline (or prepare yourself to help develop it) if you start playing with these parameters.

## Other Detector Designs
The two prior examples are all about storing _more_ information during the re-simulation process
so that certain "special" events can be studied in more detail. One could also imagine studying how
a select set of "special" events behave within a modified detector. Technically, this is easy - 
simply change the name provided to `setDetector` or specify a relative path like is done when
saving all of the sim particles above. However, there is a big caveat.

The random number generation in Geant4 is sequential. This means psuedo-random numbers are "created"
one-after-another and then given to the process requesting a random number. The simulated events will
only be identical if the requests from different functions are done in the _same exact order_ in order
to preserve the assignment of psuedo-random numbers to their roles in the simulation. We can initiate
this process correctly by setting up the RNG (random number generator) to be in the same state as it
was at the beginning of the original simulated event (what we call the `eventSeed` in the event header
represents this state); however, if the simulation is not configured the same as before, the order of
random number requests can change leading to different simulation results even though we used the same
initial state of the RNG.

With this disucssion of RNGs aside, I can get to the point: **The "special-ness" of an event needs to
be "decided earlier" than where the detector is being changed.** By "special-ness", I mean what happens
within the simulation that causes this event to be interesting (for example, a particularly nasty photon-nuclear
interaction followed by a kaon decay). By "decided earlier", I mean that this "special-ness" process needs
to happen in a detector volume that is processed by Geant4 _before_ any of the detector volumes that are being
changed. For example, if we want to inspect how changes to the HCal can help veto particularly nasty ECal photon-nuclear events, that is ok because we are not changing the ECal where the "special" stuff occurs. We cannot change
the ECal itself and expect the re-simulation to re-play the same "special" process since the RNG may not follow
the same path. Similarly, we cannot change the tagger or recoil or anything upstream of the ECal for fear of it
affecting the RNG.
