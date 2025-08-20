# Container-Software Compatibility

Often we need to introduce new dependencies in order to do new things
in our software. Occasionally we make mistakes with these dependencies
and need to fix how they are configured or installed. Both of these
reasons cause some compatibility issues where all versions of ldmx-sw
are not necessarily buildable by all versions of the container.

The "container image" is version controlled in its repository 
[LDMX-Software/dev-build-context](https://github.com/LDMX-Software/dev-build-context).
If you are interested in looking for which minimum version of the container 
has your desired dependency, you should look through the 
[releases](https://github.com/LDMX-Software/dev-build-context/releases) of the container.

The ldmx-sw versions are documented in the "releases" of the LDMX-Software/ldmx-sw repository,
but you should also read these versions as inclusive of branches that are based off of them.
For example, if you made a branch when ldmx-sw was version 3.0 you may not be able to use
a container that is incompatible with ldmx-sw version 3.0 (i.e. you might need to introduce
updates to later versions of ldmx-sw onto your branch to use a newer container).

The ordering of versions follows semantic versioning 
(i.e. order by major version, then minor version, then patch). 

```admonish warning
This compatibility table is manually written _and_ not everything has been
directly tested. Updates to this document from your personal experience are welcome
and encouraged.
```

For each range of versions of compatibility, we've written a table corresponding
to different container versions required for different build configurations of
ldmx-sw. This was done since many new features that require new dependencies
are first introduced as opt-in features. Below, I've written a table
allowing you to know what I mean by certain build configurations.

build config | meaning
-------------|---------
default      | No parameters given to `cmake` besides necessary ones
no testing   | disable testing which is enabled by default[^1]
force legacy onnx | ldmx-sw's CMake code for finding ONNX didn't work well and so it needs to be modified slightly[^2]
sanitizers | enable one or more of the sanitizers, cmake: `-DENABLE_SANITIZER_*=ON`
detector id bindings | enable detector ID python bindings, cmake: `-DBUILD_DETECTORID_BINDINGS=ON`
patch cmake | need to do both `no testing` and `force legacy onnx`
header patch | transitioning to a newer compiler then required a few more headers to be included[^3]
include lorentz vector | add `Math/GenVector/LorentzVector.h` and `Math/Vector4Dfwd.h` to inclusions in `Ecal/IntermediateCluster.h`

[^1]: Currently in ldmx-sw, there isn't a command-line option to disable the
      testing so one must comment out the `build_test()` line in `ldmx-sw/CMakeLists.txt`.
      Using a version of software without any testing being built is not a good idea,
      unless you need to stay on an old version for a good reason it would be much 
      better to update your branch to a newer version of ldmx-sw and update the container
      to the newest version as well.

[^2]: Forcing legacy onnx is relatively simple and can be done by commenting out the
      `find_path` call within the `ldmx-sw/cmake/FindONNXRuntime.cmake` file. This
      prevents CMake from finding the system install in newer containers.

[^3]: The specific headers needed vary depending on the version you are attempting to build.
      You can either look at [the patch files for different versions](https://github.com/LDMX-Software/dev-build-context/tree/main/ci/interop)
      or simply follow the compiler's instructions for including the appropriate headers.

### Pre-v3.0.0
No containers have been studied for older versions of ldmx-sw.
Although, there was 
[a patch-release of v1.7.0](https://github.com/LDMX-Software/ldmx-sw/releases/tag/v1.7.1) 
so that it could run in an image.

### >=v3.0.0 and < v3.1.1

build config | image version
---|---
default | < v4.0.0
patch cmake | >= v4.0.0, < v5.0.0

### >=v3.1.1 and < v3.1.12

build config | image version
---|---
default | < v4.0.0
patch cmake | >= v4.0.0, < v5.0.0
with sanitizers | > v3.2, < v5.0.0

### >= v3.1.12 and < v3.2.4

build config | image version
---|---
default | < v4.0.0
patch cmake | >= v4.0.0, < v5.0.0
with sanitizers | > v3.2, < v5.0.0
with detector id bindings | > v3.3, < v5.0.0

### >= v3.2.5 and < v3.3.4
Since we are requiring an upgrade of the container
in order to support the testing we also switch the
detector ID bindings to be included in the default
build configuration which simply bumps the minimum
no-testing release by three.

build config | image version
---|---
default | >= v4.0.0, < v5.0.0
no det id bindings | >= v3.2, < v5.0.0
no det id bindings and no sanitizers | >= v3.0, < v5.0.0
header patch | >= v5.0.0

### >= v3.3.5, < v4.3.0
Updates to the ROOT dictionary generation procedure inadvertently
broke compatibility with older container images.
Users of older container images will see issues during dictionary building
related to the `std::string_view` feature of C++17.
If - for some reason - you require to use a pre-v4 container image with
a version of ldmx-sw newer than v3.3.5, then you will need to manually
undo the ROOT dictionary generation changes that were done in
[Framework PR #73](https://github.com/LDMX-Software/Framework/pull/73).
This is highly technical and I would recommend avoiding it at all costs.

build config | image version
---|---
default | >= v4.0.0, < v5.0.0
header patch | >= v5.0.0

Compiler patches necessary to work well with ldmx/dev:5.0.0 were initially
introduced in ldmx-sw:v4.2.15; however, ongoing development required other
patches to be included as well.
It is encouraged to rebase and/or merge ldmx-sw:v4.3.0 into your branch in
order for the main CI tests to work now that they use ldmx/dev:5.0.0.

### = v4.3.0
Patches for the newer compiler have been included and so the default build
configuration can be handled by the new image version.
Not all of the _warnings_ from the newer compiler have been patched,
but a regular build that doesn't force the warnings to be errors completes
and runs as expected.

build config | image version
---|---
default | >= v4.0.0

### >= 4.3.1, < v4.4.13
One release after getting development to function with ldmx/dev:v5,
I (Tom) accidentally introduced a change that breaks compatibility with ldmx/dev:4.2.2
which uses an older version of ROOT.

The error you see is with using `XYZTVector` which is not present in the `ROOT::Math` namespace
without including a couple more headers.

~~~admonish example title="Example Compile Error Message", collapsible=true
I've removed the other errors generated by the compiler, mainly focused on how the `centroid` function
is not defined anymore since its return type is not defined.
```
/home/tom/code/ldmx/ldmx-sw/Ecal/include/Ecal/IntermediateCluster.h:24:21: error: 'XYZTVector' in namespace 'ROOT::Math' does not name a type
   24 |   const ROOT::Math::XYZTVector& centroid() const { return centroid_; }
      |                     ^~~~~~~~~~
```
~~~

build config | image version
---|---
default | >= v5.0.0
include lorentz vector | >= v4.0.0

### >= v4.4.13
Some changes were made to how the environment in the development container is configured so
that the denv workspace can be moved into ldmx-sw [ldmx-sw #1472](https://github.com/LDMX-Software/ldmx-sw/issues/1472).
This leads to a set of confusing warnings and errors that are difficult for a non-expert to understand.

The main source of this is that `denv` relies on copying a shell configuration file called `.profile` into your workspace and then reading that configuration file when launching the container.
This `.profile` allows you to [customize your container environment](https://tomeichlersmith.github.io/denv/tune.html#rc-files), but it also is _never_ overwritten by `denv` in order to avoid undoing any changes you want to make.

If you don't care about customizing your local container environment (e.g. you've never looked at the `.profile` before), then you can just remove it and have `denv` make a new copy whenever you switch images.
```
rm .denv/skel-init .bashrc .bash_logout .profile
denv config image <pull-or-different-tag>
```

If you do care about keeping your local customizations,
I've written some notes on changes that I suspect you need to make to `.profile` depending on
the error message you are seeing.

You can find the `.profile` that `denv` is using within your denv workspace by running `denv printenv HOME`
which will print the directory in which the `.profile` will be.

~~~admonish note title="Neither `LDMX_BASE` nor `LDMX_SW_INSTALL` is defined." collapsible=true
This comes from having a `.profile` file from an image >= v5.1.1 being used with an older image <= v5.1.0
that expects a different `.profile`.

Inside the `.profile`, make sure to define `LDMX_SW_INSTALL` _before_ the `. /etc/ldmx-env-init.sh` line.

If ldmx-sw is the denv workspace, then you should define
```
export LDMX_SW_INSTALL=${HOME}/install
```
or if the parent directory of ldmx-sw is the denv workspace, then
```
export LDMX_SW_INSTALL=${HOME}/ldmx-sw/install
```
or you can set it to some other path that you are installing ldmx-sw to.
~~~

~~~admonish note title="fire: command not found" collapsible=true
This arises from a lot of different combinations of `.profile` files and image versions,
but it simplifies once you know a little of the background.
Most of the time it comes up because you have an old (<= v5.1.0) `.profile` being used
with a new (>= v5.1.1) image.

The shell within the container looks through the directories in a `:`-separated list
stored in the `PATH` environment variable, so this error crops up if the `PATH` variable
is not configured properly.

You can use `denv printenv PATH` to see where the shell is looking for executables.
You want to leave the `/usr/...` ones as written (those are the ones for stuff in the image),
but the other one refers to a directory that is supposed to be on your system and point to
where ldmx-sw is installed.

For example, you may need to remove the `LDMX_BASE` lines from within the `.profile` file in your denv
workspace. Notice that before I edited `.profile` with `vim`, there is an extra "ldmx-sw" in the path to its
install.
```
tom@appa:~/code/ldmx/ldmx-sw$ denv printenv PATH
/home/tom/code/ldmx/ldmx-sw/ldmx-sw/install/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/src/GENIE/Generator/bin:/usr/local/src/GENIE/Reweight/bin
tom@appa:~/code/ldmx/ldmx-sw$ tail .profile 

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
# make sure LDMX_BASE is defined for ldmx-env-init.sh
if [ -z "${LDMX_BASE+x}" ]; then
  export LDMX_BASE="${HOME}"
fi
. /etc/ldmx-env-init.sh
tom@appa:~/code/ldmx/ldmx-sw$ vim .profile 
tom@appa:~/code/ldmx/ldmx-sw$ tail .profile 
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
. /etc/ldmx-env-init.sh
tom@appa:~/code/ldmx/ldmx-sw$ denv printenv PATH
/home/tom/code/ldmx/ldmx-sw/install/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/src/GENIE/Generator/bin:/usr/local/src/GENIE/Reweight/bin
```
~~~
