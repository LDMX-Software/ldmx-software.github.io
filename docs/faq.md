---
layout: default
---

# What the F.A.Q.?
Frequent issues and potholes that new collaborators run into while starting their work with LDMX software.

### On macOS, I get a "invalid developer path" error when trying to use `git`.
On recent versions of the mac operating system, you need to re-install command line tools.
[This stackexchange question](https://stackoverflow.com/questions/58280652/git-doesnt-work-on-macos-catalina-xcrun-error-invalid-active-developer-path) outlines a simple solution.

### I can't compile and I get a "No such file or directory" error.
LDMX software is broken up into several different `git` repositories that are then pulled into a central repository _ldmx-sw_ as "submodules".
In order for you to get the code in the submodules, you need to tell `git` that you want it. There are two simple ways to do this.
1. You can re-clone the repository, but this time using the `--recursive` flag.
```bash
git clone --recursive https://github.com/LDMX-Software/Framework.git
```
2. You can download the submodules after cloning _ldmx-sw_.
```bash
git submodule update --init --recursive
```

### Software complains about not being able to create a processor. (UnableToCreate)
This is almost always due to the library that contains that processor not being loaded.
We are trying to have the libraries automatically included by the python templates, 
but if you have found a python template that doesn't include the library you can do the following in the meantime.
```
# in your python configuration script
# p is a ldmxcfg.Process object you created earlier
p.libraries.append( 'libMODULE.so' )
# MODULE is the module that your processor is in (for example: Ecal, EventProc, or Analysis)
```

### Software complains about linking a library. (LibraryLoadFailure)
Most of the time, this is caused by the library not being found in the common search paths.
In order to make sure that the library can be found, you should give the full path to it.
```
# in your python configuration script
# p is a ldmxcfg.Process object you created earlier
p.libraries.append( '<full-path-to-ldmx-sw-install>/lib/libMODULE.so' )
# MODULE is the module that your processor is in (for example: Ecal, EventProc, or Analysis)
```

### ROOT version mismatch error.
This error looks something like this:
```
Error in <TUnixSystem::Load>: version mismatch, <full-path>/ldmx-sw/install/lib/libEvent.so = 62000, ROOT = 62004
```
This is caused by using one version of ROOT to compile _ldmx-sw_ and another one to use _ldmx-sw_,
and most people run into this issue when compiling _ldmx-sw_ inside of the container and then using _ldmx-sw_ outside of the container.
The fix to this is simple: **always compile and use _ldmx-sw_ inside of the container**. 
This makes sure that the dependencies never change.

If you need some dependency that isn't in your version of the container,
please file an [issue with the docker repository](https://github.com/LDMX-Software/docker/issues/new/choose) to request what's called a "derivative" container.
