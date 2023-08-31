# Container-Software Compatibility

Often we need to introduce new dependencies in order to do new things
in our software. Occasionally we make mistakes with these dependencies
and need to fix how they are configured or installed. Both of these
reasons cause some compatibility issues where all versions of ldmx-sw
are not necessarily buildable by all versions of the container.

The "container image" is version controlled in its repository 
[LDMX-Software/docker](https://github.com/LDMX-Software/docker).
If you are interested in looking for which minimum version of the container 
has your desired dependency, you should look through the 
[releases](https://github.com/LDMX-Software/docker/releases) of the container.

The ldmx-sw versions are documented in the "releases" of the LDMX-Software/ldmx-sw repository,
but you should also read these versions as inclusive of branches that are based off of them.
For example, if you made a branch when ldmx-sw was version 3.0 you may not be able to use
a container that is incompatible with ldmx-sw version 3.0 (i.e. you might need to introduce
updates to later versions of ldmx-sw onto your branch to use a newer container).

The ordering of versions follows semantic versioning 
(i.e. order by major version, then minor version, then patch). 

**Warning** This compatibility table is manually written _and_ not everything has been
directly tested. Updates to this document from your personal experience are welcome
and encouraged.

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

[^1]: Currently in ldmx-sw, there isn't a command-line option to disable the
      testing so one must comment out the `build_test()` line in `ldmx-sw/CMakeLists.txt`.
      Using a version of software without any testing being built is not a good idea,
      unless you need to stay on an old version for a good reason it would be much 
      better to update your branch to a newer version of ldmx-sw and update the container
      to the newest version as well.

[^2]: Forcing legacy onnx is relatively simple and can be done by commenting out the
      `find_path` call within the `ldmx-sw/cmake/FindONNXRuntime.cmake` file. This
      prevents CMake from finding the system install in newer containers.

### Pre-v3.0.0
No containers have been studied for older versions of ldmx-sw.
Although, there was 
[a patch-release of v1.7.0](https://github.com/LDMX-Software/ldmx-sw/releases/tag/v1.7.1) 
so that it could run in a container image.

### >=v3.0.0 and < v3.1.1

build config | container version
---|---
default | < v4.0.0
patch cmake | >= v4.0.0

### >=v3.1.1 and < v3.1.12

build config | container version
---|---
default | < v4.0.0
patch cmake | >= v4.0.0
with sanitizers | > v3.2

### >= v3.1.12 and < v3.2.4

build config | container version
---|---
default | < v4.0.0
patch cmake | >= v4.0.0
with sanitizers | > v3.2
with detector id bindings | > v3.3

### >= v3.2.5
Since we are requiring an upgrade of the container
in order to support the testing we also switch the
detector ID bindings to be included in the default
build configuration which simply bumps the minimum
no-testing release by three.

build config | container version
---|---
default | >= v4.0.0
no det id bindings | >= v3.2
no det id bindings and no sanitizers | >= v3.0
