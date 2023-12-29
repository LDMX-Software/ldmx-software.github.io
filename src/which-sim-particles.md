# Which SimParticles are saved?

Often, one of the first tasks users of ldmx-sw have is to inspect
the simulated particles that exist in an output file to learn about
what happened within an event. It is then fairly easy to find out that
not all of the simulated particles are actually saved into the output
file. One could find this out in multiple ways, but commonly, folks
find this out through one of two observations.

1. The track IDs (the key in the `std::map` they are stored in) skip
   numbers pretty regularly.
2. A SimParticle's "parent" or "daughter" is missing from the particles
   saved for that event.

In any case, this naturally leads to confusion; hence, this page trying
to explain it.

```admonish warning title="Vocabulary Confusion"
I should emphasize here that we copy a `G4Track` into our `SimParticle`.
Geant4 has chosen to use the word "particle" to mean the definition of a
particle and its properties. Individual particles moving through space and
time are "tracks" in Geant4. We undo this switch-a-roo because we have
other things called "tracks". To further add confusion, parts of our geometry
infrastructure refer to "trajectories" which are also the same thing.
```

```admonish tip title="Data Structure"
First, it is helpful to be aware of the structure of the stored simulated
particle data. We save this data as a `std::map<int, ldmx::SimParticle>`
where the key of the map is the Geant4 track ID of the particle (a unique
integer within each event) and the value is a 
[ldmx::SimParticle](https://ldmx-software.github.io/ldmx-sw/classldmx_1_1SimParticle.html)
that stores data about the particle.
```

## Motivation
Why not store all of the simulated particles?

The answer to this question is pretty simple: it is a waste of space.
When a high energy electron hits a huge block of material, it undergoes
a process we call "showering" creating hundreds if not thousands of particles
as it interacts with the material. Most of these particles created during
a shower are not "interesting" for our purposes, so it is helpful to just
skip saving them. We do have the ability to store all of the particles in
an event if you desire, you can follow 
[the same instructions](simulation/resim.md#storing-all-simulated-particles)
provided for storing all simulated particles during re-simulation.

## Implementation
We get around this phenomena of showering by only saving a select group of 
particles during normal simulation which satisfy one (or more) of the following.

1. The simulated particle is one of the primary particles
    - This is determined by the generators the user provides to the simulation.
2. The simulated particle is created in a region with `StoreTrajectories` set to `true`
    - This is set within the GDML of the detector where we define regions.
      In all of the current detectors, all of the regions will store trajectories _except_
      the calorimeters.
3. The simulated particle has its `SaveFlag` set to `true`
    - This is determined by any extra `UserAction`s the simulation has attached to it.

We do not usually have any `UserAction`s which set the `SaveFlag` to `false` because
`UserAction`s which are looking for particular simulated particles are usually trying
to get around the bulk "veto" imposed by the simulation throwing away simulated particles
that were created within the calorimeter region (either the ECal or the HCal).

`UserAction`s that focus on looking for particular particles and making sure they are saved
already exist and can be used as examples. These actions (and their example configs) largely
live within the `Biasing` module of ldmx-sw.

```admonish example title="Biasing/test/ecal_pn.py"
This config uses several user actions to make sure the a hard brem occurs within the target
and that high-energy photon undergoes a Photon-Nuclear (PN) interaction within the ECal. Since the PN interaction
is very interesting for us and it happens in the ECal, this config also uses the TrackProcessFilter
action which makes sure all particles that were created with the PN interaction are saved.

With this config, the sim particles that exist in the output file fall into three categories.

1. Starts outside of the ECal or HCal. This includes the primary electron that started the
   simulation, but also may include other particles that are created as the electron journeys
   from the beam into the calorimeters including the high energy photon created in the target.
2. Products of a PN Interaction. All particles that are created via the PN interaction are saved.
   Since a PN interaction is required to happen in the ECal, many of these particles will have
   daughter track IDs that do not exist in the particle map since they were not created via the
   PN interaction and thus do not pass the filter.
```

```admonish example title="SimCore/test/basic.py"
This config (as the name implies) does not use any user actions and is just here to help
test the basic running of a simulation.

With this config, the sim particles that exist are all created upstream of the calorimeters.
If you were to look at a distribution of all particles and their starting z location, you
would see none of them past ~200 mm where the front of the ECal and HCal are. These particles
include the primary electron fied by the generator and any particles it produces on its way
to the calorimeters.
```

```admonish note title="For Developers"
This particle saving infrastructure is handled by the
[simcore::UserTrackInformation](https://ldmx-software.github.io/ldmx-sw/classsimcore_1_1UserTrackInformation.html)
which stores the save flag referenced earlier and the
[simcore::g4user::TrackingAction](https://ldmx-software.github.io/ldmx-sw/classsimcore_1_1g4user_1_1TrackingAction.html)
which applies the defaults described above as well as passes the save decision onto
the class which creates the `SimParticle` for a `G4Track`.
```
