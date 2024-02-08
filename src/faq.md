# What the F.A.Q.?
Frequent issues and potholes that new collaborators run into while starting their work with LDMX software.

~~~admonish question collapsible=true title="CMake error: does not contain a CMakeLists.txt file."
The full text of this error looks like (for example)
```
CMake Error at Tracking/CMakeLists.txt:61 (add_subdirectory):
  The source directory

    /full/path/to/ldmx/ldmx-sw/Tracking/acts

  does not contain a CMakeLists.txt file. 
```

We make wide use of [submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) in `git` so that
our software can be separated into packages that evolve and are developed at different rates.
The error summarized in this title is most often shown when a submodule has not been properly initialized
and thus is missing its source code (the first file that is used is the `CMakeLists.txt` file during the `cmake`
step). Resolving this can be done with
```
git submodule update --init --recursive
```
This command does the following
- `submodule update` instructs `git` to switch the submodules to the commits stored in the parent repository
- The `--init` flag tells `git` to do an initial `clone` of a submodule if it hasn't yet.
- The `--recursive` flag tells `git` to recursively apply these submodule updates in case submodule repos have
  their own submodules (which they do in our case).

You can avoid running this submodule update command if you use `--recurse-submodules` during your initial
clone and any pulls you do.
```
# --recursive is the flag used with older git versions
git clone --recurse-submodules git@github.com:LDMX-Software/ldmx-sw.git
git pull --recurse-submodules
```
I **highly recommend** reading the linked page about git submodules. It is very helpful for understanding
how to interact with them efficiently.
~~~

~~~admonish question collapsible=true title="How can I find the version of the image I'm using?"
Often it is helpful to determine an image's version.
Sometimes, this is as easy as looking at the tag provided by `docker image ls` or written into the SIF file name,
but sometimes this information is lost.
Since v4 of the container image, we've been more generous with adding labels to the image and a standard one is included
`org.opencontainers.image.version` which (for our purposes) stores the release that built the image.

We can use `inspect` to find the labels stored within an image.
```
# docker inspect returns JSON with all the image manifest details
# jq just helps us parse this JSON for the specific thing we are looking for,
# but you could just scroll through the output of docker inspect
docker inspect ldmx/dev:latest | jq 'map(.Config.Labels["org.opencontainers.image.version"])[]'
# apptainer inspect (by default) returns just the list of labels
# so we can just use grep to select the line with the label we care about
apptainer inspect ldmx_dev_latest | grep org.opencontainers.image.version
```

If the `org.opencontainers.image.version` is not an available label, then the image being used was
built prior to v4 and a more complicated, investigative procedure will need to be done. In this case,
you should be trying to find the "digest" of the image you are running and then looking for that "digest"
on the images availabe on DockerHub.

With `docker` (and `podman`), this is easy
```
docker images --digests
```
It is more difficult (impossible in general?) with `apptainer` (and `singularity`) since
some information is discarded while creating the SIF.
~~~

~~~admonish question collapsible=true title="Running ROOT Macros from the Command Line"
ROOT uses shell-reserved characters in order to mark command line arguments as specific inputs to the function it is parsing and running as a macro.
This makes passing these arguments through our shell infrastructure difficult and one needs a hack to get around this.
Outside of the container, one might execute a ROOT macro like
```
root 'my-macro.C("/path/to/input/file.root",72,42.0)'
```
Using the `ldmx` command to run this in the container would look like
```
ldmx root <<EOF
.x my-macro.C("/path/to/input/file.root",72,42.0)
EOF
```
The context for this can be found on [GitHub Issue #1169](https://github.com/LDMX-Software/ldmx-sw/issues/1169).
~~~

~~~admonish question collapsible=true title="Installing on SDF: No space left on the device"
On SLAC SDF (and S3DF, I use the same name for both here) we will be using singularity which is already installed. 
This is a frustrating interaction between SDF's filesystem design and singularity. Long story short, singularity needs O(5GB) of disk space for intermediate files while it is downloading and building container images and by default it uses `/tmp/` to do that. `/tmp/` on SDF is highly restricted. The solution is to set a few environment variables to tell singularity where to write its intermediate files.
```
# on SDF
export TMPDIR=/scratch/$USER
# on S3DF
export TMPDIR=${SCRATCH}
```
The ldmx-env.sh script is able to iterface with both docker and singularity so you should be able to use it after resolving this disk space issue.
~~~

~~~admonish question collapsible=true title="How do I update the version of the container I am using?"
We've added this command to the `ldmx` command line program.
In general, it is safe to just update to the latest version.
```
ldmx pull dev latest
```
This explicitly pulls the latest version no matter what,
so it will download the image even if it is the same as
one already on your computer.
~~~

~~~admonish question collapsible=true title="My display isn't working when using Windoze and WSL!"

You probably are seeing an error that looks like:

```
$ ldmx rootbrowse
Error in <TGClient::TGClient>: can't open display ":0", switching to batch mode...
In case you run from a remote ssh session, reconnect with ssh -Y
Press enter to exit.
```

The solution to this is two-fold.

1. Install an X11-server on Windoze (_outside_ WSL) so that the display programs inside WSL have something to send their information to. [X410](https://x410.dev/) is a common one, but there are many options.
2. Make sure your environment script (`scripts/ldmx-env.sh`) has updates to the environment allowing you to connect directly to the server. These updates are on [PR #997](https://github.com/LDMX-Software/ldmx-sw/pull/997) and could be manually copied if you aren't yet comfortable with `git`.
~~~

~~~admonish question collapsible=true title="Is it okay for me to use tools outside the container? I have been informed to only use the container when working on LDMX."
The container is focused on being a well-defined and well-tested environment for ldmx-sw, but it may not be able to accomodate every aspect of your workflow. For example, my specific workflow can be outlined with the following commands (not a tutorial, just an outline for explanatory purposes):

```
ldmx cmake .. # configure ldmx-sw build
ldmx make install # build and install ldmx-sw
ldmx fire sim.py # run a simulation
rootbrowse sim_output.root #look at simulation file with local ROOT build **outside the container**
ldmx fire analysis.py sim_output.root #analyze the simulation file
python pretty_plotter.py histogram.root #make PDFs from ROOT histograms generated by analysis.py
```

As you can see, I switch between inside the container and outside the container and I can do this because I have an install of ROOT outside the container. Key point: For what I am doing which is simply looking at ROOT files and plotting ROOT histograms, my ROOT install does not need to match the ROOT inside the container.
I think using both the container and a local installation of ROOT is a very powerful combination. This allows for you to use ROOT's TBrowser or TTreeViewer to debug files while using the container to actually build and run ldmx-sw.
Another workflow that follows a similar protocol is a python-based analysis.

```
ldmx cmake .. # configure ldmx-sw build
ldmx make install # build and install ldmx-sw
ldmx fire sim.py # run a simulation
rootbrowse sim_output.root #look at simulation file with local ROOT build **outside the container**
ldmx python analysis.py sim_output.root #analyze the simulation file and produce PDF/PNG images of histograms
```

Notice that the `analysis.py` script, _even though it is not being run through fire_, is still run inside of the container. This is because the python-based analysis needs access to the ROOT dictionary for ldmx-sw which was generated by the container. _This is the only reason for analysis.py to be run inside the container._ If the `sim_output.root` file only has (for example) ntuples in it, then you could run your analysis outside the container because you don't need access to the ldmx-sw dictionary.

```
python analysis.py sim_output.root #this analysis uses the local ROOT install and does not need the ldmx-sw ROOT dictionary
```

*Conclusion:* The absolutely general protocol still uses an installation of ROOT that is outside of the container. You do not need installations of the other ldmx-sw dependencies and your installation of ROOT does not need to match the one inside of the container. 
~~~

~~~admonish question collapsible=true title="On macOS, I get a 'invalid developer path' error when trying to use `git`."
On recent versions of the mac operating system, you need to re-install command line tools.
[This stackexchange question](https://stackoverflow.com/questions/58280652/git-doesnt-work-on-macos-catalina-xcrun-error-invalid-active-developer-path) outlines a simple solution.
~~~

~~~admonish question collapsible=true title="On macOS, I get a failure when I try to run the docker containers."
The default terminal on macOS is `tcsh`, but the environment setup script assumes that you are using `bash`. You should look at [this article](https://www.howtogeek.com/444596/how-to-change-the-default-shell-to-bash-in-macos-catalina/) for how to change your default shell to `bash` so that the ldmx environment script works.
~~~

~~~admonish question collapsible=true title="On macOS, I get a error when trying to use tab completion."
This error looks like
```
ldmx <tab>-bash: compopt: command not found
```
where `<tab>` stands for you pressing the tab key.
This error arises because the default version of `bash` shipped with MacOS is pretty old,
for example, MacOS Monterey ships with bash version 3.2 (the current is 5+!).

You can get around this issue by simply updating the version of `bash` you are using.
Since the terminal is pretty low-level, you will unfortunately need to also manually override the default bash.

1. Install a newer version of bash. This command uses [homebrew](https://brew.sh/) to install `bash`.
```
brew install bash
```
2. Add the newer bash to the list of shells you can use.
```
sudo echo /usr/local/bin/bash >> /etc/shells
```
3. Change your default shell to the newer version
```
chsh -s /usr/local/bin/bash $USER
```

You can double check your current shell's bash version by running `echo $BASH_VERSION`.

This answer was based on a helpful [stackexchange answer](https://apple.stackexchange.com/questions/224511/how-to-use-bash-as-default-shell).
~~~

~~~admonish question collapsible=true title="I can't compile and I get a 'No such file or directory' error."
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
~~~

~~~admonish question collapsible=true title="Software complains about not being able to create a processor. (UnableToCreate)"
This is almost always due to the library that contains that processor not being loaded.
We are trying to have the libraries automatically included by the python templates, 
but if you have found a python template that doesn't include the library you can do the following in the meantime.
```
# in your python configuration script
# p is a ldmxcfg.Process object you created earlier
p.libraries.append( 'libMODULE.so' )
# MODULE is the module that your processor is in (for example: Ecal, EventProc, or Analysis)
```
~~~

~~~admonish question collapsible=true title="Software complains about linking a library. (LibraryLoadFailure)"
Most of the time, this is caused by the library not being found in the common search paths.
In order to make sure that the library can be found, you should give the full path to it.
```
# in your python configuration script
# p is a ldmxcfg.Process object you created earlier
p.libraries.append( '<full-path-to-ldmx-sw-install>/lib/libMODULE.so' )
# MODULE is the module that your processor is in (for example: Ecal, EventProc, or Analysis)
```
~~~

~~~admonish question collapsible=true title="ROOT version mismatch error."
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
~~~

~~~admonish question collapsible=true title="Parameter 'className' does not exist in list of parameters."
This error usually occurs when you pass an object that isn't an EventProcessor as an EventProcessor to the Process sequence.
A feature that is helpful for debugging your configuration file is the `Process.pause` function:
```
# at the end of your config.py
p.pause() #prints your Process configuration and waits for you to press enter before continuing
```
~~~

~~~admonish question collapsible=true title="ldmx-sw cannot find the contents of a file when I _know_ that the file exists"
Remember that you are running inside of the container, so the file you want to give to the software must be accessible by the container.
Some python features that are helpful for making sure the container can find your file are `os.path.fullpath` to get the full path to a file and
`os.path.isfile` to check that the file exists.
~~~
