## Pre-Requisites

This page assumes you (the reader) already has experience with `git` and `C++` in order to focus on the specifics of `ldmx-sw`. If you are not as experienced with either of these, then you may need to use more resources than this guide to gain an understanding of `ldmx-sw`.

## 0. Installation and Test Run

Follow the instructions on [how to install ldmx-sw](https://github.com/LDMX-Software/ldmx-sw/wiki/Installing-ldmx-sw) to build an installation on your local computer. If you are using group resources, your group may already have an installation that you can use and you can skip this step.

Make sure the installation was built and linked correctly by running `ldmx-test` without any arguments. This should return a message describing saying that several tests passed, for example:
```bash
$ ldmx-test
===============================================================================
All tests passed (6 assertions in 1 test case)

```

To  use the the SLAC installation, or your own installation at SLAC, please see [these instructions](https://github.com/LDMX-Software/ldmx-sw/wiki/Getting-Started-with-ldmx-sw-at-SLAC).

## 1. Practice using `ldmx-app`

This is another test on your installation, but it gives you more freedom to explore `ldmx-sw`.

`ldmx-app` is run by using a "python configuration file." This config file is actually executed as a python script before run parameters are extracted, so you can use python to make your job easier.

### Write your first config file

For the purposes of the rest of these exercises, you should have a single file of ~100 events so that it can be analyzed fairly quickly. If you want to skip to writing your own analyzers and you already have an event file, then you can skip to the next exercise.

Read through [Running and Configuring `ldmx-app`](https://github.com/LDMX-Software/ldmx-sw/wiki/Running-and-configuring-ldmx-app) to learn more about the python configuration scripts. The configuration script provided there gives an example of a script you could use to generate the small event file to analyze. Mess around with the parameters and look at the processors used in that script to make your sample your own and learn more!

There are already several processors in _ldmx-sw_ that have a template python module that you can import into your config. Most processors that have this sort of template but it in their module's `python` directory.

## 2. Analyze a sample using `ldmx-app`

### General Description of Processing in `ldmx-app`

`ldmx-app` iterates through all of the events stored in a file. Each of these events has an _event bus_ that contains all of the objects that store data about the event. A good introductory way to think of this analysis is implied by the use of the phrase "event bus". Each file contains a line of buses and each bus stops at each processor in the sequence. Each processor can go onto the bus making additions or just getting information before the bus proceeds to the next processor in the sequence. A processor that is allowed to add objects to the bus are called _producers_ while a processor that is not allowed to add objects is called an _analyzer_. The event bus can contain singular objects or Standard Template Library (STL) collections of objects. Objects that can be in the event bus are called `EventBusPassenger`s and are listed in the `Event/include/EventDef.h` file. 

### Exercise

You can write your own processors in a fork of the [kickstart repository](https://github.com/LDMX-Software/ldmx-analysis). This repo requires you to provide it a path to your ldmx-sw installation, but after that, you don't need to compile ldmx-sw anymore!

Write your own `Analyzer` that makes some sort of histogram. The default example is the `DummyAnalyzer` in the `Framework` module. You can also generate an analyzer template using the `NewProcessor.py` script in the `utils` directory of the `ldmx-sw-scripts` [repository](https://github.com/LDMX-Software/ldmx-sw-scripts). You'll need to check this out if you'd  like to use it:

`git clone https://github.com/LDMX-Software/ldmx-sw-scripts.git`

A more specific exercise is given below.

### Goal: Fill a Histogram with the Transverse Momenta of All Particles

1. Use the `NewProcessor.py` script to generate a new analyzer in your fork of ldmx-analysis.
2. Make sure your new processor can be added to the processing sequence by having it print "Hello World" to the screen for each event. You will need to add your new processor to a python configuration file (like you used above) and have the processor in the sequence provided to the ldmx process.
3. Look at `DummyAnalyzer` to see how to list all of the products in each of your events. Get your analyzer to print out the PDG IDs of all of the simulated particles for each of the events in your sample.
4. Now that you have the collection of simulated particles in your analyzer, have your analyzer fill a histogram of the transverse momentum of each of the simulated particles. The `DummyAnalyzer` also fills a simple histogram, but it does not use the collection of simulated particles.

---
The rest of these exercises are much more code-heavy. If you are not developing for _ldmx-sw_, you can take a break from these exercises now and start writing your own physics analyses using what you have learned.

## 3. Construct a Producer using a pre-defined event object

All of the event objects that can be added to the event bus are in the `Event` module. You've probably already used a few of them while practicing making an analyzer in the previous exercise. Now, you will add your own version of one of these classes to the event bus. Most of the event objects are highly specialized, but a simpler one to use to practice is `HcalVetoResult`.

### Goal: Write your own HCal Veto

0. There is already an implementation of an HCal Veto: `EventProc::HcalVetoProcessor`. Look at it to gain some inspiration.
1. Look through the header and source files for `HcalVetoResult` to make sure you understand the aspects of this class.
2. Generate a new producer template using `NewProcessor.py` and make sure that it can be added to the processing sequence by having it print the number of `HcalHits` in each event.
3. Design your veto. Look at the `DummyProducer` and `HcalVetoProcessor` to find out different ways to add your object to the event bus.
4. Make sure your new object is being stored in the output file by opening it in `root`.

#### Bonus:
5. There is a way to tell `ldmx-app` to skip an event (i.e. not save it in the output file) from within a processor. Can you make your veto actually skip events that would have failed to pass it? Hint: You have to put new code in both your producer's source file *and* your python configuration file. There are examples of this in the `Configuration/python` directory of ldmx-sw.

## 4. Construct a Producer and your own event object

_Note: Currently, in order to write your own event object, you need to make additions to ldmx-sw and re-build and re-install ldmx-sw after these additions._

You've already written a producer in the previous exercise, but you were constrained to only using objects that have already been written for a different purpose. This is not how most new producers work. Most new producers have a corresponding new event object developed with it.

### Goal: Determine full path information of primary electron.

Before you get started there are some things you need to know about the simulation in order to do this task effectively and accurately.
 - Geant4 (G4) is the simulation toolkit that we use, and a lot of the terminology in `SimParticle` is borrowed from G4.
 - G4 uses the `TrackID` as a unique identifier for each particle, _but_ it is not perfect. In some interactions, the track ID changes even though we would consider one of the products to be the same as one of the incoming particles.
 - The kinematic information stored in `SimParticle` is what the particle had *at creation*. This is especially important to consider when looking at the primary electron.
 - The end point stored in `SimParticle` is when the given track ID is no longer used. This *may or may not* be the point where the particle actually is stopped or destroyed because there are interactions that change the track ID in G4 without destroying the particle.
 - Not all of the particles generated by G4 are stored in the simulation file. This is because thousands of particles are generated in the particle shower in the ECal, and storing them all would take too much space. This is important to remember when using the references to other particles. For example, the particle stored as the "parent" is may or may not be stored as well.

Now we are ready to track the path of the primary electron in the event.

0. We want to know the full kinematic information for the primary electron along its journey. Start by thinking of what we need to find and how we could calculate it if it isn't directly available in the data file. This isn't as easy as taking the starting and ending points stored in `SimParticle`. These points don't take into account any scattering that occurs along the particle's real path in the simulation which would lead to a curved path instead of a straight line.
1. Make a producer template and use it to try to track the primary electron through the first few events in your file. What collections do you need to get? How do you determine the electrons energy or momentum at a specific time/place? Print this information to your screen to see if it makes sense. This processor can be in your ldmx-analysis repository. Only the new event bus object needs to be inside of ldmx-sw.
2. Write a C++ class that will store this path information for the primary electron and follow the [instructions](https://github.com/LDMX-Software/ldmx-sw/wiki/Creating-a-new-Event-Bus-Object) on how to add it to the LDMX event bus. This step is complicated and _will_ take some patience.
3. Add your object to the event bus and check that it is being added. How would you check that the path is being determined correctly? How would you check that the momentum/energy at each point along the path is being determined correctly?
4. Write an analyzer to make a histogram of the real path length of the primary electron (_not_ the straight line distance between the starting and ending points). You could make this histogram inside of your producer, but you should make a separate analyzer to double check that the object you added to the event bus can be accessed by other processors.

## 5. Draw your new event object in `ldmx-eve`

_Note: The Event Display is not as cleanly structured as the other parts you have worked with. This exercise may take longer than the previous ones due to this complexity. It also requires your additions to be made inside of ldmx-sw instead of in your personal ldmx-analysis repository._

You now have a file containing the path of the primary electron for each event. This is a very visual object and it would be nice to be able to see what the path of the primary electron looks like. `ldmx-eve` is the event display tool inside of `ldmx-sw`, and you can add your object to the list of objects that are drawn so that you can see what your path looks like.

0. Look through the `EventDisplay` module to gain some familiarity with how it is structured. You will be editing the `EventDisplay` and `EventObjects` classes.
1. The `EventDisplay` class is the object that constructs the display and gets the objects from the event bus. Look through its header and source file and copy the structure of `hcalDigiHits` or some other event object (there are several). There are many places that need to be edited in both the header and source files.
2. The `EventObjects` class is the object that draws the objects found in the event bus. This is where you would add in a drawing method. Again, follow the examples already there to see what you need to do. A good starting point would be trying to get your new draw method to simply print some information about the primary electron path to the screen before you worry about drawing something in the display.
3. Make sure to cleanup any hanging pointers that you have created.