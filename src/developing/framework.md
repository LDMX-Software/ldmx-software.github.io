# ldmx-sw Framework Structure

ldmx-sw is organized into "modules" that contain related code, the `Framework` module
is of particular importance since it defines the core processing interfaces and handles
reading/writing data from/to the ROOT files.

The overall flow of a successful execution of `fire` goees through two stages.

1. Configure - run the provided Python script and then extract the run configuration
    from the Python objects that were created when the script was run.
2. Run - execute the configured run. The `framework::Process` class is the main object
    that handles the execution.

~~~admonish question collapsible=true title="Where is the main?"
Many developers, especially those who are more familiar with C++, will want to know
where the `fire` executable is defined.
`fire` is defined within `Framework/app/fire.cxx` and this file reveals the overall
flow of the program.
~~~

~~~admonish question collapsible=true title="How does Python get run?"
We launch Python from within our C++ program by
[embedding Python](https://docs.python.org/3/extending/embedding.html).
In the configuration area of `Framework`, you'll see may of these calls to Python's
C interface (like `Py_InitializeEx()` for example).
~~~

~~~admonish question collapsible=true title="Why use Python for configuration?"
It's easier than maintaining our own language for configuration.

The sheer number of configuration parameters makes it necessary to organize
them based on which parts of the software they correspond to.
This then necessitates some kind of configuration language in order
to instruct the software of the values for the multitude of parameters.

Geant4 has a similar issue and chose to develop their own configuration
language -- search "Geant4 macro commands" online to see what it looks like.
Besides being a huge technical debt in order to maintain such a language,
we also then lose all of the helpful benefits of running Python.
Users can use Python libraries (like `sys`, `os`, and `argparse`) to
allow for their configuration to be "smarter" and inspect command line
arguments as well as environment variables.
We [can implement checks on the configuration in Python](https://github.com/LDMX-Software/ldmx-sw/issues/1303)
in order to catch any configuration issues as early as possible.
~~~

We require ldmx-sw to do a lot of different tasks and the Framework is present
to make sure those different tasks can be developed on top of a known structure.
The following pieces of Framework helps introduce the vocabulary as well as explain how they are used.

Each of these classes in C++ has a "mirror" Python class that is used to configure it.
While the Python configuration class is not strictly necessary for the configuration system
to function as intended, it is very helpful to keep parameters organized and have the
configuration understandable.

~~~admonish example
A C++ producer that is declared like
```cpp
class MyProducer : public framework::Producer {
```
would have a mirror python configuration class defined like
```python
class MyProducer(ldmxcfg.Producer):
```
This mirroring helps point out that all the configuration parameters
within the Python `MyProducer` are meant to be used by the C++ `MyProducer`.
~~~

#### Processor
A processor is the main object that developers of ldmx-sw interact with.
They are used to create the objects within an event ("Producer") and analyze
those objects ("Analyzer").
A processor is given access to the event where it can access the event objects
from an input file or produced by earlier producers.
They can also be used to fill histograms which are stored into the output
histogram file and provided "storage hints" that can be used to decide if
a specific event should be written into the output event file.

#### Conditions
A "condition" is an object that is the same for many events in sequence (like a table of
electrical gains or the "geometry" of the detector).
Conditions are provided by "Conditions Object Providers" that can be written by ldmx-sw
developers.
These providers only construct the conditions themselves when the condition is requested
by a processor. They take information from the current event to see how to configure
the condition that is being constructed and how long the constructed condition is valid
for ("interval of validity" or IOV).
The Framework then can come back to the provider to construct a new condition if the
condition that was previously provided is not valid anymore.
