# Getting Started at SLAC

> Note: This page is old and refers to a now-deprecated cluster at SLAC as well as ldmx-sw programs that have been removed. We are keeping it around "just in case" but unless it goes through a significant re-write, it is probably best to be ignored.

The following is a summary of [Overview of ldmx-sw with examples specific to running at SLAC](https://tinyurl.com/y9lzvzwv)

Note: The recipe that follows only works on the centos 7 machines.

### Logging in & basic setup

Begin by login into one of the centos7 public login hosts as follows
```bash
ssh -XY centos7.slac.stanford.edu
```
Once logged in, create your own directory within the `users` in the LDMX group area as follows: 
```bash
cd /nfs/slac/g/ldmx/users/
mkdir $USER
```

### Setting Up the Environment to use the group installation
NB this section is under construction

The group installation can be setup by using issuing the following commands:

```bash
cd /nfs/slac/g/ldmx/users/$USER
scl enable devtoolset-8 bash  
cp /nfs/slac/g/ldmx/software/setup_gcc8.3.1_cos7.sh .
source /nfs/slac/g/ldmx/users/$USER/setup_gcc8.3.1_cos7.sh
```

You can test that the installation is correctly setup by running
```
ldmx-test 
```
And you should see the following if the paths are successfully set: 
```
===============================================================================
All tests passed (6 assertions in 1 test case)
```

### Setting Up the Environment for local development


The development environment can be setup by issuing the following command
```bash
cd /nfs/slac/g/ldmx/users/$USER
scl enable devtoolset-8 bash  
cp /nfs/slac/g/ldmx/software/local_setup_gcc8.3.1_cos7.sh .
source /nfs/slac/g/ldmx/users/$USER/local_setup_gcc8.3.1_cos7.sh
```
#### Bonus Tip:

Put the following into your `.bash_profile` so that it is easier to setup the ldmx working environment.
```bash
alias ldmxstable='source scl_source enable devtoolset-8; source /nfs/slac/g/ldmx/software/setup_gcc8.3.1_cos7.sh'
```
Then you can setup the ldmx environment by just running `ldmxstable`. This "stable" environment uses the group installation of ldmx-sw, so it is helpful for running longer jobs.

### Building `ldmx-sw`

Clone the ldmx-sw git repository into your personal directory 

```bash 
git clone git@github.com:LDMX-Software/ldmx-sw.git
```

or

```bash 
git clone https://github.com/LDMX-Software/ldmx-sw.git
```

This requires you to have already [set-up a git configuration file](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration). 

Configuring the build via CMake can be done as follows: 

```bash
cd ldmx-sw; mkdir build; cd build
cmake -DGeant4_DIR=$G4DIR -DROOT_DIR=$ROOTDIR -DXercesC_DIR=$XercesC_DIR -DPYTHON_EXECUTABLE=`which python` -DPYTHON_INCLUDE_DIR=$PYTHONHOME/include/python2.7 -DPYTHON_LIBRARY=$PYTHONHOME/lib/libpython2.7.so -DCMAKE_INSTALL_PREFIX=../install ..
```

Issuing the `make` command then builds `ldmx-sw`
```bash
make -j16 install
```

Finally, the `ldmx-sw` build path can be added by editing `local_setup_gcc8.3.1_cos7.sh` i.e. uncommenting the following lines

```bash
###############
#   ldmx-sw   #
###############
export LDMXSW_DIR=/nfs/slac/g/ldmx/users/$USER/ldmx-sw/install
export PATH=$LDMXSW_DIR/bin:$PATH
export LD_LIBRARY_PATH=$LDMXSW_DIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$LDMXSW_DIR/lib/python:$LD_LIBRARY_PATH
```

and re-sourcing `local_setup_gcc8.3.1_cos7.sh`

```bash
source /nfs/slac/g/ldmx/users/$USER/local_setup_gcc8.3.1_cos7.sh
```
