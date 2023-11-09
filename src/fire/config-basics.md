# Configuration File Basics
Often times, the script that is passed to `fire` to configure how _ldmx-sw_ runs and processes data is called a "config script" or even simply "config". This helps distinguish these python files from other python files who have different purposes (like filling histograms or creating plots).

There are many configs stored within _ldmx-sw_ itself which mostly exist to help developers quickly test any code developments they write. These examples, while often complicated at first look, can be helpful for a new user wishing to learn more about how to write their own config for _ldmx-sw_.

- `.github/validation_samples/<name>/config.py`: configs used in automatic PR validation tests, these have a variety of simulations as well as the full suite of emulation and reconstruction processors with _ldmx-sw_
- `Biasing/test/` : configs used to help manually test developments in the Biasing and Simulation code, these mostly just have simulations and do not contain emulation and reconstruction processors
- `exampleConfigs` directory within modules: configs written by module developers to help describe how to use the processors they are developing

In order to help guide your browsing, below I've written two example configs that _will not run_ but they do show code snippets that are similar across a wide variety of configs.
In all configs, there will be the creation of the `Process` object where the name of that pass is defined and there will be some lines defining the `p.sequence` of processors
that will be run to process the data.

Additional notes:
- Using the variable name `p` for the `Process` object is just convention and is not strictly necessary; however, it does lend itself nicely to sharing bits of code between configs.
- Most of the time, especially for processors that are already written into _ldmx-sw_, the construction of a processor is put into its own
  python module so that the C++ class name, the module name, and any other parameters can be properly spelled once and used everywhere.

## Minimal Production Config
In Production Mode, there won't be a `p.inputFiles` line but there will be a line setting `p.run` to some value.

```python
from LDMX.Framework import ldmxcfg
p = ldmxcfg.Process('mypass')
p.outputFiles = ['output_events.root']
p.run = 1
p.sequence = [
  ldmxcfg.Producer('my_producer','some::cpp::MyProducer','Module')
]
```

## Minimal Reconstruction Config
In Reconstruction Mode, there will be a `p.inputFiles` line but since `p.run` will be ignored it is often omitted.

```python
from LDMX.Framework import ldmxcfg
p = ldmxcfg.Process('myreco')
p.inputFiles = ['input_events.root']
p.outputFiles = ['rereco_input_events.root']
p.sequence = [
  ldmxcfg.Producer('my_reco', 'some::cpp::MyReco', 'Module')
]
```
