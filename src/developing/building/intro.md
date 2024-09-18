# Build and Installing ldmx-sw

There are many intricasies that come with building such a large software project.
This chapter is focused on providing guides on how to accomplish this build
and more detailes related to it.

This chapter assumes you already finished with everything under "[Getting started](../developing/getting-started.md)"

## Clone the Software Repository
In a terminal, go to the directory where you will keep all of your LDMX software and run the following command.
```
git clone --recursive git@github.com:LDMX-Software/ldmx-sw.git
```

~~~admonish note title="Comments"
- The `--recursive` flag is _very important_ because there are several necessary parts of _ldmx-sw_ stored in separate git repositories.
- The above `clone` uses an SSH connection which requires you to [create a GitHub account](https://github.com/signup) and [connect to it with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).
~~~

~~~admonish tip title="Changing the link after cloning" collapsible=true
If you find yourself with an already cloned copy of ldmx-sw that was cloned with the HTTPS link and you wish to create a new branch and push,
you can switch the link of the remote to the SSH version on your machine without having to re-clone.
```
git remote set-url origin git@github.com:LDMX-Software/ldmx-sw.git
```
This is especially helpful if you've already made some changes you do not want to lose.
~~~

~~~admonish success title="Test"
You can see the ldmx-sw software directory in your terminal.
```
ls
# 'ldmx-sw' is one of the entries printed
cd ldmx-sw
just
# our justfile's default recipe is to printout all the possible commands
```
~~~

## Setup the Environment
One of the recipes within our `justfile` handles initializing a default environment.
```
just init
```

~~~admonish note title="Comments"
- This command downloads the latest development image, so it may take some time (a few minutes) on the first run.
- This command only needs to be done once per clone of ldmx-sw. Look at the other commands available from `just` for changing the environment.
- On shared computing clusters, the specific filesystem configuration may not be well suited to downloading the image with the default configuration. _For apptainer_, be aware that you can move the directory in-which images are stored using the `APPTAINER_CACHEDIR` environment variable and move the directory in-which the build takes place using the `TMPDIR` environment variable. This is specifically an issue for SLAC's SDF and S3DF which have very small `/tmp` directories (what apptainer uses if `TMPDIR` is not defined).
  - The `justfile` updates the default definition of `APPTAINER_CACHEDIR` to be the parent directory of ldmx-sw, but this may still not be the best location.
~~~

~~~admonish success title="Test"
You can view the environment configuration from `denv`.
```
denv config print
# detail of how the environment is configured
```
If you see something like "no workspace found", then something went wrong during the environment setup.
~~~

## Development Cycle
The `justfile` contains many recipes that are helpful so inspect the output
printed when `just` is run with no arguments to view some of them.
The default build can be created with
```
just compile
```
You can pass CMake variables to the configure command (sanitizer is just an example)
and then `build` the updated configuration.
```
just configure -DENABLE_SANITIZER_ADDRESS=ON 
just build
```
For the CLANG compiler with LTO please run
```
just configure-clang-lto
just build
```

Often you will want to recompile and run a config script.
```
just recompFire my-config.py [config args ...]
```
Running the test suite is done with
```
just test
```
