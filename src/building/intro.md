# Building ldmx-sw

Each of the steps below is really short but more detail has been added in order to help users debug any issues they may encounter. If all goes well, you will be able to fly through these instructions within 5-10 minutes (depending on how long software installations take). Each of the sections has a "Comments" subsection for extra details and a "Test" subsection allowing you to verify that you completed that step successfully.

### Windows Comments
- If you are running on a Microsoft Windows system, it is _necessary_ for you to do all of the steps below within Windows Subsystem for Linux (WSL). The permissions system that docker relies on in order to effectively run the containers is not supported by Windoze. (While GitBash and the Command Prompt can look similar to other terminals, make sure to open a WSL terminal --- often labeled "Ubuntu").
- _As of this writing, you cannot use a VPN and connect to the internet from within WSL_
- The "docker daemon" needs to be running. On most systems, this program starts automatically when the computer is booted. You can check if the docker daemon is running by trying to run a simple docker container. If it is not running, you will need to start it manually. 
- Docker Desktop outside WSL needs to be running to be able to use docker inside WSL? (question mark because unsure)

## Install a Container Runner
Currently, ldmx-sw's environment script supports `docker` and `singularity`. On personal laptops, most users will find it easiest to [install the docker engine](https://docs.docker.com/engine/install/). [singularityCE](https://docs.sylabs.io/guides/latest/user-guide/) and [apptainer](https://apptainer.org/) both provide the program `singularity` with near-identical functionality in a way that is often desirable for shared computing environments (like university clusters), so you may not need to install anything if one of these packages are already installed.

~~~admonish note title="Comments"
- If you are on Windows, make sure to use the WSL2 backend for docker.
- On Linux systems, make sure to [manage docker as non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user)
  so that you can run that command without `sudo`.
~~~

~~~admonish success title="Test"
You can run a simple container in whichever runner is available.
```
docker run hello-world
```
_or_
```
singularity run docker://ghcr.io/apptainer/lolcow
```
~~~

This may be the first point where you enter into a terminal unless your installation was terminal-based.
If you are using Windows, remember to go into Windows Subsystem for Linux rather than other Windows terminals like GitBash or Command Prompt.

## Clone the Software Repository
In a terminal, go to the directory[^1] where you will keep all of your LDMX software and run the following command.
```
git clone --recursive https://github.com/LDMX-Software/ldmx-sw.git
```

[^1]: If you are unfamiliar with the terminal, a helpful resource is [linuxcommand.org](https://linuxcommand.org/lc3_learning_the_shell.php).

~~~admonish note title="Comments"
- The `--recursive` flag is _very important_ because there are several necessary parts of _ldmx-sw_ stored in separate git repositories.
- The above `clone` uses a HTTPS connection which will allow you to `git pull` updates but it won't allow you to `git push` any changes you
  make to GitHub. If you are going to write code for ldmx-sw and contribute, make sure to [create a GitHub account](https://github.com/signup) 
  and [connect to it with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh), then use the SSH link rather than
  the HTTPS link (`git@github.com:LDMX-Software/ldmx-sw.git`).
~~~

~~~admonish tip title="Changing the link after cloning" collapsible=true
If you find yourself with an already cloned copy of ldmx-sw and you wish to create a new branch and push,
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
```
~~~

## Setup the Environment
In order to simplify using the container runner installed earlier (and to have the same commands shared between different runners),
we have developed a `bash` environment script.
```
source ldmx-sw/scripts/ldmx-env.sh
```

~~~admonish note title="Comments"
- Must occur in a `bash` terminal (the default on many Linux systems and available on iOS).
  In some iOS versions, the default shell is `tcsh` instead of `bash`. You can read [this article](https://www.howtogeek.com/444596/how-to-change-the-default-shell-to-bash-in-macos-catalina/)
  to learn how to change the default shell to `bash` so the environment script works without
  any other fuss.
- This command downloads the latest development image, so it may take some time (a few minutes) on the first run.
- This command must be re-run whenever a new terminal is opened because a new terminal starts with a "clean" environment.
- On shared computing clusters, the specific filesystem configuration may not be well suited to downloading the image
  with the default configuration. _For singularity_, be aware that you can move the directory in-which images are stored 
  using the `SINGULARITY_CACHEDIR` environment variable and move the directory in-which the build takes place using the `TMPDIR`
  environment variable. This is specifically an issue for SLAC's SDF which has a very small `/tmp` directory (what singularity
  uses if `TMPDIR` is not defined).
~~~

~~~admonish success title="Test"
You can run the `ldmx` command. Running it without any arguments will print out a usage message.
```
ldmx
# a help message is printed
```
If you see something like "command not found", then something went wrong during the environment setup.
~~~

## Configure the Software Build
ldmx-sw uses CMake to configure how the software will be built.
You can do this configuration from within the `ldmx-sw` directory.
```
cd ldmx-sw
ldmx cmake -B build -S .
```
Since the container is specifically built for ldmx-sw, there should
be no warnings and no errors reported by CMake. Some information will
be printed about which versions of dependencies were found and what modules
are being built.

## Build and Install
After CMake writes all the makefiles for us, we use `make` to build the software.
Technically, this step both compiles the software and installs the software, but
often you want the software installed after compiling so that you can run it.
```
cd build
ldmx make install
```

~~~admonish note title="Comments"
- You can speed up the build (sometimes) by allowing `make` to use more cores on your computer.
  This can be done by using the `-j` flag, for example, `-j2` would inform `make` to use 2 cores.
~~~

~~~admonish success title="Test"
Similar to the CMake step, if there aren't any errors reported during compilation, you
are good to move on. If you wish, you could also run one or more of the pre-packaged
configuration scripts (a.k.a. "configs") to make sure the installation is functional.
```
cd .. # go back to ldmx-sw out of ldmx-sw/build
ldmx fire SimCore/test/basic.py
```
~~~

# Next Steps
Now that the software is built and installed, you can run a few more programs within the container.
Most likely, you will want to run some parts of ldmx-sw and in this case the program you will run
is called `fire`.
```
ldmx fire my-config.py
```
There are many configuration scripts shipped with ldmx-sw for various testing and sharing any
of which should be operational and could be helpful for you to get started on your own config.
- Biasing/test: configs running with a simulation where certain processes are biased and filtered for
- SimCore/test: basic simulation testing
- .github/validation_samples: longer configs with emulation and reconstruction used to do automatic validation of the code during development
