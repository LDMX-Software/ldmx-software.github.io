---
layout: default
---

# Container

> _Note:_ This method is _highly_ recommended. The extra details below are not for the faint of heart.

- [Install the docker engine](https://docs.docker.com/engine/install/)
  - [singularity](https://sylabs.io/guides/3.5/user-guide/) is also supported if you can't install and/or don't want to install docker.
- (on Linux systems) [Manage docker as non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
- Clone the repo: `git clone --recursive https://github.com/LDMX-Software/ldmx-sw.git`
  - The `--recursive` flag is _very important_ because there are several necessary parts of _ldmx-sw_ stored in separate git repositories.
- Setup the environment: `source ldmx-sw/scripts/ldmx-env.sh`
  - Must occur in a `bash` terminal (the default on Ubuntu systems and available on iOS)
  - Downloads the latest development docker image, so it may take some time (a few minutes) on the first run
  - Must be re-run whenever a new terminal is opened
- Make a build directory: `cd ldmx-sw; mkdir build; cd build;`
- Configure the build: `ldmx cmake ..`
- Build and Install: `ldmx make install -j2`
- Now you can run any processor in _ldmx-sw_ through `ldmx fire`

---

Building ldmx-sw will require the installation of several dependencies. The following guide will walk you through the installation of those dependencies as well as ldmx-sw. **This is your final warning.**

## Supported Platforms
* Linux 
    * __Tested on__: RedHat6 and CentOS7 with devtoolset-6/8, OpenSuse > 42.1, Ubuntu > 18.0)
* Building on MacOS outside the container is not supported.
* Building on Windows outside the container is not even close to supported.

## Required Tools

* __Git__ 
    * Used for version control
    * __Download__: https://git-scm.com/download or simply use your package manager
    * __Notes__: Make sure `git` is added to your `PATH` environment variable before running CMake

* __CMake > v3.0__ 
    * Used to generate a build configuration for your build system
    * __Download__: https://cmake.org/download
    * __Installation__: https://cmake.org/install/

* __GCC > 7.0__
    * Need a modern compiler that supports the C++17 standard.
    * __Download__: https://gcc.gnu.org/git.html or use your package manager
    * __Installation__: https://gcc.gnu.org/install/ or use your package manager

## Required dependencies

* __Boost > 1.60__
    * Used for logging and provides additional C++ tools
    * __Download__: https://www.boost.org/users/history/
    * __Installation__: https://www.boost.org/doc/libs/1_61_0/more/getting_started/unix-variants.html or use your package manager.

* __Xerces C++ > 3.2__
    * Framework is required for GDML support in Geant4 so it must be installed first.
    * __Download__: http://xerces.apache.org/xerces-c/download.cgi
    * __Building on Linux__:
        ``` bash
        wget http://archive.apache.org/dist/xerces/c/3/sources/xerces-c-3.2.0.tar.gz
        tar -zxvf xerces-c-3.2.0.tar.gz
        cd xerces-c-3.2.0
        mkdir build; mkdir install; cd build;
        cmake -DCMAKE_INSTALL_PREFIX=../install ..
        make -j16 install
        cd ../install
       export XercesC_DIR=$PWD 
       ```
    * __Notes__:  The `XercesC_DIR` environment variable is optional and for convenience.  The option `-j16` after the make command is used to specify the number of cores the build should use and should be set to a value appropriate to your system.

* __Geant4 > 10.2.p03__
    * Geant4 is the simulation engine used by LDMX.  LDMX uses a custom version of
      Geant4 10.02.p03 that includes modifications to the Bertini Cascade model
      and fixes to the calculation of the Gamma to mu+mu- matrix element. 
    * __Building on Linux__: 
        ``` bash
        git clone -b LDMX.10.2.3_v0.4 --single-branch https://github.com/LDMXAnalysis/geant4.git 
        cd geant4
        mkdir build; cd build
        cmake -DGEANT4_USE_GDML=ON -DGEANT4_INSTALL_DATA=ON -DXERCESC_ROOT_DIR=$XercesC_DIR \
              -DGEANT4_USE_OPENGL_X11=ON -DCMAKE_INSTALL_PREFIX=../install ..
        cmake --build . --target install
        cd ../install
        source bin/geant4.sh
        export G4DIR=$PWD
        ```
     * __Notes__: Installing on Ubuntu variants can require a couple of dependencies
       to fix the errors: EXPAT error, Could not find X11, Could not find X11 
       headers, Could not find OpenGL. Add `-DGEANT4_USE_SYSTEM_EXPAT=OFF'` to
       the CMake argument, before the last `..`, and install these dependencies
       before the CMake step:  After it is installed, you can source `geant4.sh`
       in the `bin` directory. This script defines the environment variable
      `G4DIR` which points to the installation.

* __ROOT > 6.0__
    * The ROOT data structure is used for persistency of simulated and reconstructed objects and for creation of histograms.
    * __Download__: https://root.cern.ch/downloading-root
    * __Building on Linux__: 
        ``` bash
        wget https://root.cern.ch/download/root_v6.16.00.source.tar.gz
        tar -zxvf root_v6.16.00.source.tar.gz
        mkdir root-6.16.00-build
        cd root-6.16.00-build
        cmake -DCMAKE_INSTALL_PREFIX=../root-6.16.00-install -Dgdml=ON -Dcxx17=ON -DPYTHON_EXECUTABLE=$(which python3) ..
        make -j16 install
        cd ../root-6.16.00-install
        source bin/thisroot.sh
        ``` 
     * __Notes__: ROOT has many installation options and optional dependencies, and the [building ROOT documentation](https://root.cern.ch/building-root) covers this in full detail. When you source `thisroot.sh`, it defines the bash environment variable `ROOTSYS` to be the locations of the install.

## Optional Dependencies

* __ONNXRuntime > 1.2__
    * Scoring engine for machine learning models.  Used to load BDT and DNN models into ECal veto processors. 
    * __Download__: https://github.com/microsoft/onnxruntime/releases/tag/v1.2.0
    * __Notes__: Building from source requires a modern CMake version (> 3.14) and Python 3.0 and is not recommended.  Use the binaries if possible.

# Building ldmx-sw

Start by cloning the `ldmx-sw` repository and make a build directory.
```bash
git clone https://github.com/LDMX-Software/ldmx-sw.git
cd ldmx-sw; mkdir build; cd build;
```
Configuring the build via CMake can be done as follows

```bash
cmake -DGeant4_DIR=$G4DIR -DROOT_DIR=$ROOTDIR -DXercesC_DIR=$XercesC_DIR -DCMAKE_INSTALL_PREFIX=../install ..  
```
In some instances, a non-system installation of python will be needed.  In this case, the environmental variable `$PYTHONHOME` needs to be set to point to your python build. The above `cmake` command should then be modified as follows:
``` bash
 -DPYTHON_EXECUTABLE=`which python` -DPYTHON_INCLUDE_DIR=$PYTHONHOME/include/python2.7 -DPYTHON_LIBRARY=$PYTHONHOME/lib/libpython2.7.so 
```

After the `cmake` step exits without any errors, you can build and install `ldmx-sw` with the following command
```bash
cmake --build . --target install -- -j16
```
Now you have an installation of *ldmx-sw* in the *../install* directory. _Note:_ The number after the `-j` should be changed to reflect the number of processors you want to allow the build to use.

## Setting Up the Environment 

Now you need to tell your computer where the _ldmx-sw_ install is. This can be done by running the following lines (it might make things easier if you put these lines in your `.bash_profile` so that they are automatically run when you open a new terminal).

``` bash
export LDMX_INSTALL_PREFIX=/full/path/to/ldmx/install #need to change this line
source <path-to-root-install>/bin/thisroot.sh #need to change this line
source <path-to-geant4-install>/bin/geant4.sh #need to change this line
export LD_LIBRARY_PATH=$LDMX_INSTALL_PREFIX/lib:$LD_LIBRARY_PATH
export PATH=$LDMX_INSTALL_PREFIX/bin:$PATH
export PYTHONPATH=$LDMX_INSTALL_PREFIX/lib/python:$PYTHONPATH
```
Once you have executed the above commands in your shell, you should be able to execute programs like `ldmx-app` without any additional setup.

## Next Steps

Now that you have an installation of ldmx-sw, you can start writing your own processors to start studying physics! Fork the [kickstart repository](https://github.com/LDMX-Software/ldmx-analysis) and you can start writing your own processors in there. You can also check out some [Startup Excercises](https://github.com/LDMX-Software/ldmx-sw/wiki/Startup-Exercises) (practice makes perfect!).

## Help

Comments, suggestions or cries for help can be sent to [Omar Moreno](mailto:omoreno@slac.stanford.edu) or posted in the #getting_started channel of the [LDMX Software Slack](https://ldmxsoftware.slack.com/).  


