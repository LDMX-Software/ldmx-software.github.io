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

### >= v4.3.0
Patches for the newer compiler have been included and so the default build
configuration can be handled by the new image version.
Not all of the _warnings_ from the newer compiler have been patched,
but a regular build that doesn't force the warnings to be errors completes
and runs as expected.

build config | image version
---|---
default | >= v4.0.0
