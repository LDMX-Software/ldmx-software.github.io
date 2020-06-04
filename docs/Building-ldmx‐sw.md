Building ldmx-sw will require the installation of several dependencies. The following guide will walk you through the installation of those dependencies as well as ldmx-sw.

## Supported Platforms
* Linux 
    * __Tested on__: RedHat6 and CentOS7 with devtoolset-6/8, OpenSuse > 42.1, Ubuntu > 18.0)
* Building on MacOS is not currently supported.

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
        git clone -b LDMX.10.2.3_v0.3 --single-branch https://github.com/LDMXAnalysis/geant4.git 
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
        cmake -DCMAKE_INSTALL_PREFIX=../root-6.16.00-install -Dgdml=ON -Dcxx17=ON ..
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

## References

* [LDMX-SW Doxygen Documentation](https://ldmxanalysis.github.io/ldmx-sw/html/index.html)

# Custom OS

> _Note:_ This method of using ldmx-sw is new and not very well tested. If you run into issues, please send questions to [Tom Eichlersmith](mailto:eichl008@umn.edu) or contact him on the LDMX Slack.

Currently, the ldmx-sw custom development operating system is stored on [Tom's homepage](http://homepages.spa.umn.edu/~eichl008/ldmx-dev-vm/) (hopefully this is temporary!). You can go there and click on the files to download them, or you could use `wget`:
```bash
wget --no-parent http://homepages.spa.umn.edu/~eichl008/ldmx-dev-vm/ldmx-dev.{iso,md5}
```
No matter how you download the `iso` image, you should check that the download completed correctly:
```bash
# make sure ldmx-dev.iso is in this directory too
md5sum --check ldmx-dev.md5
```
Now you can either install this `iso` on a computer you have or use it as the file to run a virtual machine with. Either way, after you start up this OS, you should try the following commands to compile and build ldmx-sw.
```bash
git clone --recursive https://github.com/LDMX-Software/ldmx-sw.git #get ldmx-sw from githug
cd ldmx-sw
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=../install/ ../
make install
```
Again, this method of using ldmx-sw is still in development, so you may run into lots of issues. Whether or not you solve any issues you run into, _please_ send the issue, your build system (i.e. virtual machine manager like VirtualBox), and (if you solved it) how you solved it to [Tom Eichlersmith](mailto:eichl008@umn.edu). It has been tested on the following build systems successfully.
- Bare metal (i.e. installed as primary OS on an HP laptop) (Tom E)

> If you try this and get frustrated, feel free to abandon this method and continue to the (more manual) method below.

---
