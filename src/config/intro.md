# Running and Configuring `fire`

The `fire` application is used for simulation, reconstruction, and analysis of data from the LDMX experiment.  The application receives its configuration for a given purpose by interpreting a python script which contains instructions about what C++ code to run and what parameters to use.  The python script is _not_ run for each event, but instead is used to determine the configuration of the C++ code which is run for each event.

## Brief summary of running `fire`

From the commandline, the application is run as follows:

    $ ldmx fire {configuration_script.py} [arguments for configuration script]

The configuration script language is discussed in more detail below.

### Configuration script arguments

Arguments after the `.py` file on the commandline will be passed to the script as normal arguments to any python script.
These can be used in many ways to adjust the behavior of the script.  Some examples are given below in the [Tips and Tricks](config-tips.md) section.

## Processing Modes
There are two processing modes that `fire` can run in which are defined by the presence of input data files[^1].

If there are no input data files, then `fire` is in _Production Mode_ while if there are input data files, then
`fire` is in _Reconstruction Mode_. The names of these two modes originate from how `fire` is used in LDMX research.

[^1]: In this context, an "input data file" is a data file previously produced by `fire`. There can be other types of data that are "input" into `fire` but unless `fire` is actually treating those input files as a reference, `fire` is considered to be in "Production Mode". See the `inputFiles` configuration parameter below.

## The Process Object

The Process object represents the overall processing step.  It **must be included** in any `fire` configuration.  When the Process is constructed, the user must provide a processing pass name.  This processing pass name is used to identify the products in the data file and cannot be repeated when later processing the same file.  The pass name is useful when a file has been processed multiple times -- for example, when reprocessing a file with new calibration constants. 

As an example, the pass name is `practice`, so the line which constructs the Process is:
```python
p = ldmxcfg.Process("practice")
```

Here is a list of some of the most important process options and what they control.
It is encouraged to browse the python modules themselves for all the details, 
but you can also call `help(ldmxcfg.Process)` in `python` to see the documentation.

- `passName` (string)
   - **required** Given in the constructor, tag for the process as a whole.
   - For example: `"10MeVSignal"` for a simulation of a 10MeV A'
- `run` (integer)
  - Unique number identifying the run 
  - For example: `9001`
  - Default is `0`
- `maxEvents` (integer)
   - Maximum number of events to run for
   - Required for Production Mode (no input files)
   - In Reconstruction Mode, the number of events that are run is the number of events in the input files unless this parameter is positive and less than the input number.
   - For example: `9000`
- `outputFiles` (list of strings)
   - List of files to output events to
   - Required to be exactly one for Production Mode, and either exactly one or exactly the number of input files in Reconstruction Mode.
   - For example: `[ "output.root" ]`
- `inputFiles` (list of strings)
   - List of files to read events in from
   - Required if no output files are given
   - For example: `[ "input.root" ]`
- `histogramFile` (string)
   - Name of file to put histograms and ntuples in
   - For example: `"myHistograms.root"`
- `sequence` (list of event processors)
   - Required to be non-empty
   - List of processors to run the events through (in the order given)
   - For example: `[ mySimulator, ecalDigis, ecalRecon ]`
- `keep` (list of strings)
   - List of drop/keep rules to help ldmx-sw know which collections to put into output file(s)
   - Slightly complicated, see the [documentation of EventFile](https://ldmx-software.github.io/ldmx-sw/classframework_1_1EventFile.html)
   - For example: `[ "drop .*SimHits.*" , "keep Ecal.*" ]`
- `skimDefaultIsKeep` (bool)
   - Should the process keep events unless told to drop by a processor?
   - Default is `True`: events will be kept unless processors use `setStorageHint`.
   - Use `skimDefaultIsDrop()` or `skimDefaultIsSave()` to modify
- `skimRules` (list of strings)
   - List of processors to use to decide whether an event should be stored in the output file (along with the default given above).
   - Has a very specific format, use `skimConsider( processorName )` to modify
     - `processorName` is the _instance name_ and not the class name
   - For example, the Ecal veto chooses whether an event should be kept or not depending on a lot of physics stuff. If you only want the events passing the veto to be saved, you would:
```python
p.skimDefaultIsDrop() #process should drop events unless specified otherwise
p.skimConsider('ecalVeto') #process should listen to storage hints from ecalVeto
```
- `logFrequency` (int)
   - How frequently should the processor tell you what event number it is on?
   - Default is `-1` which is never.
