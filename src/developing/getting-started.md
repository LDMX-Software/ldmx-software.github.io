# Getting Started Developing ldmx-sw

~~~admonish warning title="Warning"
This guide assumes familiarity with the [first-time using guide](../using/getting-started.md)
and with the terminal.
~~~

~~~admonish tip title="Coming From Using ldmx-sw"
Moving from using ldmx-sw to developing ldmx-sw is a common occurrence
as issues or missing features are discovered in the course of analyzing
the physical results.

Do not fear! We still use containers to share the software and thus
the container runner and `denv` which you installed to use ldmx-sw
will still be used when developing ldmx-sw.

In fact, after building ldmx-sw yourself, you will still be able
to run `denv fire` (and similar) commands like before - it will
just use your local, custom build of ldmx-sw rather than the
released version you chose before.
~~~

We need a few more tools to help track our changes and share commands
that we use regularly.

## Make sure `git` is installed
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

~~~admonish success title="Test"
Both of the commands below should printout a help message rather than a
`Command not found` error.
```
git
git lfs
```
~~~

## Install `just`
`just` has a myriad of ways to be installed, but - like `denv` - it has
a simple download method that allows
you to get the most recent version on most systems.

For example, we can install `just` into the same directory where `denv` is
installed by default.
```
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh |\
  bash -s -- --to ~/.local/bin
```

If the above does not work on your operating system, you can see system specific instructions [on the just website]( https://just.systems/man/en/packages.html)

You probably want to enable [shell tab-completion](https://just.systems/man/en/shell-completion-scripts.html) with `just`
  which only needs to be done once per installation but will help save typing.
And then you can enable `just`'s tab completion in `bash` by putting
```
eval "$(just --completions bash)"
```
in your `~/.bashrc` file. If you are using other shells, make sure to
check which file to write to and what the syntax should be.

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

~~~admonish note title="Comments"

- `just` is not technically required in order to develop ldmx-sw.
  The recipes within the `justfile` can be read with any text editor and you can
  manually type them into the terminal yourself; nevertheless, that would be a lot more
  typing and error prone.
~~~
