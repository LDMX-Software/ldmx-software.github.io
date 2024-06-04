# Using ldmx-sw Directly

As you may be able to pick up based on my tone, I prefer the (efficient) python analysis
method given before using `uproot`, `awkward`, and `hist`. Nevertheless, there are two
main reasons I've had for putting an analysis into the ldmx-sw C++.
1. **Longevity**: While the python ecosystem evolving quickly is helpful for obtaining
  new features, it can also cause long-running projects to "break" -- forcing a refactor
  that is purely due to upstream code changes.[^1] Writing an analysis into C++, with its
  more rigid view on backwards compatibility, essentially solidifies it so that it can
  be run in the same way for a long time into the future.
2. **Non-Vectorization**: In the previous chapter, I made a big deal about how most
  analyses can be vectorizable and written in terms of these pre-compiled and fast
  functions. That being said, sometimes its difficult to figure out _how_ to write
  an analysis in a vectorizable form. Dropping down into the C++ allows analyzers
  to write the `for` loop themselves which may be necessary for an analysis to
  be understandable (or even functional).

[^1]: This longevity issue can be resolved within python by "pinning" package versions
so that all developers of the analysis code use the same version of python and the
necessary packages. Nevertheless, this "pinning" also prevents analyzers from obtaining
new features or bug fixes brought into newer versions of the packages.

The following example is **stand-alone** in the same sense as the prior chapter's
jupyter notebook. It can be run from outside of the ldmx-sw repository; however,
this directly contradicts the first reason for writing an analysis like this
in the first place. I would recommend that you store your analyzer source code
in ldmx-sw or the private ldmx-analysis. These repos also contain CMake infrastructure
so you can avoid having to write the long `g++` command necessary to compile
and link the source code.

## Set Up
I am going to use the same version of ldmx-sw that was used to generate
the input `events.root` file. This isn't strictly necessary - more often
than not, newer ldmx-sw versions are able to read files from prior ldmx-sw
versions.

This tutorial uses a feature introduced into ldmx-sw in v4.0.1.
One can follow the same general workflow with [some additional changes
to the config script](#pre-401-standalone-analyzers) described below.
```
cd work-area
denv init ldmx/pro:v4.0.1
```
The following code block shows the necessary boilerplate for starting
a C++ analyzer running with ldmx-sw.
```cpp
{{#include analyzer-boilerplate.cxx}}
```
And below is an example python config call `ana-cfg.py` that I will
use to run this analyzer with `fire`. It assumes to be in the same
place as the source file so that it knows where the library it needs
to load is.
```python
{{#include ana-cfg.py}}
```
A quick test can show that the code is compiling and running
(although it will not print out anything or create any files).
```
$ denv 'g++ -fPIC -shared -o libMyAnalysis.so -lFramework -I$(root-config --incdir) MyAnalysis.cxx'
$ denv time fire ana-cfg.py
---- LDMXSW: Loading configuration --------
---- LDMXSW: Configuration load complete  --------
---- LDMXSW: Starting event processing --------
---- LDMXSW: Event processing complete  --------
1.99user 0.11system 0:02.10elapsed 100%CPU (0avgtext+0avgdata 320716maxresident)k
0inputs+0outputs (0major+58469minor)pagefaults 0swaps
```
Notice that we still took about 2s to run. This is because, even though `MyAnalyzer` isn't
doing anything with the data, `fire` is still looping through all of the events.

## Load Data, Manipulate Data, and Fill Histograms
While these steps were separate in the previous workflow, they all share the same process
in this workflow. The data loading is handled by `fire` and we are expected to write the
code that manipulates the data and fills the histograms.

I'm going to look at the total reconstructed energy in the ECal again. Below is the updated
code file. Notice that, besides the additional `#include` at the top, all of the changes were
made within the function definitions.
```cpp
{{#include analyzer-total-rec-energy.cxx}}
```

In order to run this code on the data, we need to compile and run the program.
Again, putting your analyzer within ldmx-sw or ldmx-analysis gives you infrastructure that
shortens how much you type during this compilation step.

```
$ denv 'g++ -fPIC -shared -o libMyAnalysis.so -lFramework -I$(root-config --incdir) MyAnalysis.cxx'
$ denv time fire ana-cfg.py
---- LDMXSW: Loading configuration --------
---- LDMXSW: Configuration load complete  --------
---- LDMXSW: Starting event processing --------
---- LDMXSW: Event processing complete  --------
2.03user 0.12system 0:02.20elapsed 97%CPU (0avgtext+0avgdata 321300maxresident)k
0inputs+40outputs (0major+57977minor)pagefaults 0swaps
```

Now there is a new file `hist.root` in this directory which has the histogram we filled stored within it.

```
$ denv rootls -l hist.root
TDirectoryFile  Apr 30 22:30 2024 my-ana  "my-ana"
$ denv rootls -l hist.root:*
TH1F  Apr 30 22:30 2024 my-ana_total_ecal_rec_energy  ""
```

## Plotting Histograms
Viewing the histogram with the filled data is another fork in the road.
I often switch back to the Jupyter Lab approach using `uproot` to load histograms from `hist.root`
into `hist` objects that I can then manipulate and plot with `hist` and `matplotlib`.

~~~admonish tip title='Accessing Histograms in Jupyter Lab' collapsible=true
I usually hold the histogram file handle created by `uproot` and then use the `to_hist()` function
once I find the histogram I want to plot in order to pull the histogram into an object I am
familiar with. For example
```python
f = uproot.open('hist.root')
h = f['my-ana/my-ana_total_ecal_rec_energy'].to_hist()
h.plot()
```
~~~

But it is also very common to view these histograms with one of ROOT's browsers.
There is a root browser within the dev images (via `denv rootbrowse` or `ldmx rootbrowse`),
but I also like to view the histogram [with the online ROOT browser](https://root.cern.ch/js/latest/).
Below is a screenshot of my browser window after opening the `hist.root` file and then
selecting the histogram we filled.

![screenshot of JSROOT](jsroot-screenshot.png)

## Pre-4.0.1 Standalone Analyzers
[PR #1310](https://github.com/LDMX-Software/ldmx-sw/pull/1310) goes into detail on
the necessary changes, but - in large part -  we can mimic the feature introduced in v4.0.1
with some additional python added into the config file.

```python
{{#include pre-4.0.1-cfg.py}}
```
