_This page documents how particle generators worked for ldmx-sw v1.7.0 and older._

# Generators

***
1. Common Settings
- Beamspot
- Pileup
2. Particle Gun
3. LHE input
4. ROOT input
5. Multiparticle Gun
***

This page documents the various ways one can generate particles in ldmx-sw.  Particle generation and simulation is done via GEANT4 and the executable is `ldmx-sim`.  Job steering can be controlled through macros.  An example job would be:
```
ldmx-sim myexample.mac
```
where `myexample.mac` contains:
```
/persistency/gdml/read detector.gdml
/run/initialize
/gun/particle e-
/gun/energy 4 GeV
/gun/position 0 0 -10 mm
/gun/direction 0.0 0.0 1.0 
/ldmx/persistency/root/file test-input.root
/run/beamOn 100
```
"Primary generators" generate the primary (e.g. input) particles for an event.  There are a number of primary generators include the default `G4ParticleGun`, which is used in the example above.  Other available primary generators described below in `ldmx-sim` are LHE, ROOT, and a custom multi-particle gun.

## Common settings

These settings are common to all the different primary generators.

### Beamspot

These settings control the smearing of the beamspot size for incoming particles.  Available commands are:
```
/ldmx/generators/beamspot/enable
/ldmx/generators/beamspot/sizeX 20.0
/ldmx/generators/beamspot/sizeY 10.0
```
The first enables beamspot smearing.  The latter two set the beam X and Y width.  It is uniformly distributed.  The units are mm.  It is the full size of the beam spot (not half)

### Pileup 

Pileup is generated using the multi-particle generator.  See more documentation in the section dedicated to it.  Specifically for pileup, use the commands:
```
/ldmx/generators/mpgun/enable
/ldmx/generators/mpgun/nInteractions 1
/ldmx/generators/mpgun/enablePoisson
```

The first command enables the mpgun.  The second commands inputs the number of pileup vertices.  
The third command indicates whether you want to Poisson distribution the number of interactions defined in the second command.  
This functionality can be used with other particle generators, for example, the LHE inputs.  This is such that one can add pileup to signal simulation.  But it is *important* to call the command for LHE inputs *before* calling the mpgun in order to get the right amount of Poisson distributed interaction (incoming electrons). For example:
```
/ldmx/generators/lhe/open SLAC.4GeV.W.mchi.0.1.map.0.3.alpha0.1.fermionDM_unweighted_events.lhe

/ldmx/generators/beamspot/enable
/ldmx/generators/beamspot/sizeX 20.0
/ldmx/generators/beamspot/sizeY 10.0

/ldmx/generators/mpgun/enable
/ldmx/generators/mpgun/enablePoisson
/ldmx/generators/mpgun/nInteractions 1
/ldmx/generators/mpgun/pdgID 11
/ldmx/generators/mpgun/vertex 0 0 -10 mm
/ldmx/generators/mpgun/momentum 0 0 4 GeV
```

## Particle Gun

Particle gun comes default in GEANT.  It's for single particle generation.  Documentation can be found here:
[http://geant4.cern.ch/UserDocumentation/UsersGuides/ForApplicationDeveloper/html/AllResources/Control/UIcommands/_gun_.html](http://geant4.cern.ch/UserDocumentation/UsersGuides/ForApplicationDeveloper/html/AllResources/Control/UIcommands/_gun_.html)

## LHE input

LHE files can be read in as input, for example in the case of signal simulation.  The macro command to use the LHE as input and give the input filename is:
```
/ldmx/generators/lhe/open PATH/TO/FILENAME
```

## ROOT input

ROOT input takes an existing `ldmx-sim` output file and uses it as input.  The typical use case is to re-simulate a file with more information or filtering.  This requires the saving and re-initiating of the random seed.  N.B. If you want to _exactly_ resimulate an event, you need to be using the exact same geometry as was used to generate the original event.  The macro commands are:
```
/ldmx/generators/root/open PATH/TO/FILENAME
/ldmx/generators/root/useSeed
```
The first command sets the path to the file being used as input.  This sets the input to the generation as the input particle from the original file.  The second command `useSeed` indicates that you want to generate the same event exactly.  

## Multi-particle gun

The multi-particle gun shoots multiple versions of the same particle with possibility to shoot a Poisson-distributed number of those particles per event.  Configuration is as follows:
```
/ldmx/generators/mpgun/enable
/ldmx/generators/mpgun/enablePoisson
/ldmx/generators/mpgun/nInteractions 1
/ldmx/generators/mpgun/pdgID 11
/ldmx/generators/mpgun/vertex 0 0 -10 mm
/ldmx/generators/mpgun/momentum 0 0 4 GeV
```