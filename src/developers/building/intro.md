# Building ldmx-sw

~~~admonish warning title="Warning"
This guide assumes familiarity with the [user's guide](users/getting-started.md)
and with the terminal.
~~~

We need a few more tools to help track our changes and share commands
that we use regularly.

## Make sure `git` is Installed
`git` is a very common tool used by software developers and so it may already be
available on the system you are using for development.
Even if not (the test below fails), a simple internet search for
`install git <your-operating-system>` will give you guidance.

~~~admonish note title="Comments"
- Make sure `git` is installed **within WSL** on Windows.
  There are other ways to interact with `git` on Windows (e.g. GitBash),
  but that is **not** what we want.
- On MacOS, the default installation of `git` that comes with Apple's developer tools
  does not include the `lfs` sub-command which is required by one of ldmx-sw's
  dependencies (acts to be specific). Luckily, [GitHub has a nice tutorial](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage?platform=mac) on how to install `git lfs` on MacOS.
~~~

~~~admonish note title="Test"
Both of the commands below should printout a help message rather than a
`Command not found` error.
```
git
git lfs
```
~~~

## Install `just`
`just` has a myriad of ways to be installed, but - like `denv` - it has
[a simple download method](https://just.systems/man/en/chapter_5.html) that allows
you to get the most recent version on most systems.

~~~admonish note title="Comments"
- You probably want to enable [shell tab-completion](https://just.systems/man/en/chapter_70.html) with `just` which only needs to be done once per installation but will help save typing.
- `just` is not technically required in order to develop ldmx-sw.
  The recipes within the `justfile` can be read with any text editor and you can
  manually type them into the terminal yourself; nevertheless, that would be a lot more
  typing and error prone.
~~~

~~~admonish success title="Test"
You can run the command `just` within your terminal.
```
just
```
Without a `justfile` already residing within your current directory,
`just` will printout an error. For example:
```
$ just
error: No justfile found
```
~~~

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
just configure build
```
You can pass CMake variables to the configure command (sanitizer is just an example)
and then `build` the updated configuration.
```
just configure -DENABLE_SANITIZER_ADDRESS=ON build
```
Often you will want to recompile and run a config script.
```
just build fire my-config.py [config args ...]
```
Running the test suite is done with
```
just test
```
