# Getting Started

This guide is focused on first-time users of ldmx-sw.
If you are interested in contributing to ldmx-sw, please look
at the [getting started developing guide](../developing/getting-started.md)
for help starting to develop ldmx-sw.

ldmx-sw is a large software project that builds on top of other
large and complicated software projects. For this reason, we have
chosen to use containers to share fixed software environments allowing
all of us to know exactly what version of ldmx-sw (and its underlying
packages) is being used.

Each of the steps below is really short but more detail has been added in order to help
users debug any issues they may encounter.
If all goes well, you will be able to fly through these instructions within 5-10 minutes
(depending on how long software installations take).
Each of the sections has a "Comments" subsection for extra details and a
"Test" subsection allowing you to verify that you completed that step successfully.

~~~admonish tip title="Terminal"
While many new ldmx-sw users may be unfamiliar with the terminal,
explaining its use is beyond the scope of this site.
If you are unfamiliar with the terminal,
a helpful resource is [linuxcommand.org](https://linuxcommand.org/lc3_learning_the_shell.php)
and there are many others available online since terminals are a
common tool utilized by software developers.
~~~

### Windows Comments
- If you are running on a Microsoft Windows system, it is _necessary_ for you to do all of the steps below within Windows Subsystem for Linux (WSL). The permissions system that docker relies on in order to effectively run the containers is not supported by Windoze. (While GitBash and the Command Prompt can look similar to other terminals, make sure to open a WSL terminal --- often labeled "Ubuntu").
- _As of this writing, you cannot use a VPN and connect to the internet from within WSL_
- The "docker daemon" needs to be running. On most systems, this program starts automatically when the computer is booted. You can check if the docker daemon is running by trying to run a simple docker container. If it is not running, you will need to start it manually. 
- Docker Desktop outside WSL needs to be running to be able to use docker inside WSL? (question mark because unsure)

## Install a Container Runner
Currently, we use `denv` to help shorten and unify container interaction across
a few different runners, so we only require [a container runner supported by `denv`](https://tomeichlersmith.github.io/denv/getting_started.html#requirements).
On personal laptops, most users will find it easiest to [install the docker engine](https://docs.docker.com/engine/install/).
[apptainer](https://apptainer.org/) should already be installed on shared computing clusters.[^1]

~~~admonish note title="Comments"
- If you are on Windows, make sure to use the WSL2 backend for docker.
- On Linux systems, make sure to [manage docker as non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
  so that you can run that command without `sudo`.
- If you choose to use `podman`, make sure to update the `registries.conf` configuration
  file in order to allow for `podman` to pull from DockerHub.
~~~

~~~admonish success title="Test"
You can run a simple container in whichever runner is available.
```
docker run hello-world
```
_or_
```
apptainer run docker://ghcr.io/apptainer/lolcow
```
~~~

This may be the first point where you enter into a terminal unless your installation was terminal-based.
If you are using Windows, remember to go into Windows Subsystem for Linux rather than other Windows terminals like GitBash or Command Prompt.

[^1]: For those who've been using containers (with or without LDMX) for awhile,
the program `singularity` may sound familiar.
`apptainer` is just a new brand name for `singularity` after it was adopted
by the Linux foundation.
Many `apptainer` installations also come with a wrapper program
called `singularity` for backwards compatibility.

## Install `denv`
Follow [these instructions](https://tomeichlersmith.github.io/denv/getting_started.html#installation) for installing `denv`.
They are short but require you to be in the terminal.

~~~admonish note title="Comments"
- Remember to install `denv` within WSL if you are using Windows.
- While `denv`'s install script tries to help you update your `PATH` variable,
  it may not be perfect. You may need to consult the documentation for your shell
  on how to add new directories to the `PATH` variable so that the `denv` command
  can be found by your shell.
~~~

~~~admonish tip title="Replicating the Legacy `ldmx` Command" collapsible=true
Some folks want to replicate the `ldmx` bash function which preceeded `denv`.
To do this, you can create a few symlinks.
The examples below are for the default installation prefix for `denv`
(`~/.local`), but you can replace this directory with whereever you chose
to install `denv` when running the `curl ... install` command.
```
# for the command
ln -s ~/.local/bin/denv ~/.local/bin/ldmx
# and for the tab completion
ln -s ~/.local/share/bash-completion/completions/denv \
  ~/.local/share/bash-completion/completions/ldmx
```
~~~

~~~admonish success title="Test"
You should be able to have `denv` run its self-check that also
ensures you have a supported container runner installed.
```
denv check
```
Example output would look like
```
Entrypoint found alongside denv
Looking for apptainer... not found
Looking for singularity... not found
Looking for podman... not found
Looking for docker... found 'Docker version 27.0.3, build 7d4bcd8' <- use without DENV_RUNNER defined
denv would run with 'docker'
```
~~~

## Set Up Workspace
Whatever your project is, it will be helpful to have a directory on your
computer that holds the files related to this project.
If you haven't already made a directory for this purpose,
now is the time!
This is also where we will choose the version of ldmx-sw to use.

```
# create a directory for the project
mkdir -p ldmx/my-project
# go into that directory
cd ldmx/my-project
# initialize a new denv, defining the ldmx-sw version
denv init ldmx/pro:v4.0.1
```

~~~admonish note title="Comments"
- The specific location of the `my-project` directory does not matter. (As long as its within WSL if you're on Windows of course!)
- The version of ldmx-sw listed here is just an example, changing the version later can be done with `denv config image ldmx/pro:<ldmx-sw-version>` if desired.
~~~

~~~admonish warning
The `denv init` command should not be run from within ldmx-sw.
This could lead to a confusing state where the fire being run
is not the one associated with the ldmx-sw that resides in that
directory.
~~~

~~~admonish success title="Test"
We can make sure you have access to ldmx-sw by trying to have ldmx-sw's core program `fire`
printout its help message.
```
denv fire
```
This should look something like
```
$ denv fire
Usage: fire {configuration_script.py} [arguments to configuration script]
     configuration_script.py  (required) python script to configure the processing
     arguments                (optional) passed to configuration script when run in python
```
~~~

~~~admonish tip title="Using Legacy Versions of ldmx-sw" collapsible=true
Versions of ldmx-sw that were built with a version of the development
image before [4.2.2](https://github.com/LDMX-Software/docker/releases/tag/4.2.2)
(generaly pre-v4 ldmx-sw) do not have some ease-of-use updates to enable
running ldmx-sw from within a denv.

One can still use a denv without much effort.
In short, you must update the denv shell's profile.
```
denv exit 0 # make sure a template .profile is created
```
Add the following lines to the end of `.profile` that is in your working
directory (**not** the `.profile` in your home directory if you have one).
```
# add ldmx-sw and ldmx-analysis installs to the various paths
# LDMX_SW_INSTALL is defined when building the production image or users
# can use it to specify a non-normal install location
if [ -z "${LDMX_SW_INSTALL+x}" ]; then
  if [ -z "${LDMX_BASE+x}" ]; then
    printf "[ldmx-env-init.sh] WARNING: %s\n" \
      "Neither LDMX_BASE nor LDMX_SW_INSTALL is defined." \
      "At least one needs to be defined to ensure a working installation."
  fi
  export LDMX_SW_INSTALL="${LDMX_BASE}/ldmx-sw/install"
fi
export LD_LIBRARY_PATH="${LDMX_SW_INSTALL}/lib:${LD_LIBRARY_PATH}"
export PYTHONPATH="${LDMX_SW_INSTALL}/python:${LDMX_SW_INSTALL}/lib:${PYTHONPATH}"
export PATH="${LDMX_SW_INSTALL}/bin:${PATH}"
```
This is just a short term solution and needs to be done _on every computer_.
Updating to more recent ldmx-sw is advised.
~~~

## Running a Configuration Script
The next step now that you have access to `fire` is to run a specific configuration
of ldmx-sw with it!
Configuration scripts are complicated in their own right and have
[been given their own chapter](config/intro.md).
The next chapter is focused on analyzing event files that have been shared with you
(or generated with a config shared with you) since, generally, analyzing events is
done before development of the configs that produce those events.

