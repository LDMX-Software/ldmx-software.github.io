# Updating ldmx-sw

This page is helpful for those coming back to ldmx-sw and wishing to update there local copy of it.
It can also be a helpful guide for anyone interesting in debugging ldmx-sw since often it is
helpful to start with the most recent ldmx-sw.

We can update ldmx-sw through three main stages. These stages are not necessarily connected (i.e.
you could update the code and re-build without changing the environment if desired).

### Update Environment
The `ldmx` command includes a method for updating the environment on your machine.
```
ldmx pull dev latest
```
The `pull` command informs `ldmx` to download the latest image no matter what
(The more common `use` command will only spend time downloading if the image is
not available.)

The `latest` tag is one tag that evolves with the image as new versions are built.
If you wish to avoid accidentally upgrading your environment, you are encouraged
to use specific versions of the image (e.g. `ldmx use dev 4.2.0`).

### Update Source Code
Updating the source code of ldmx-sw mostly amounts to using various `git` comands
to download the updates other developers have uploaded to GitHub.

First, we `switch` to the main branch of ldmx-sw `trunk`.
Even if you are on a different branch, it will be best to first update your local
`trunk` before trying to update your different branch.
```
git switch trunk
```

Now pull down the updates from GitHub.
```
git pull origin trunk
```

Finally, make sure any submodules that were updated or newly introduced
are also updated along with the change in source code.
```
git submodule update --init --recursive
```

~~~admonish tip title="automatically update git submodules"
You can avoid this last step by updating your local `git` configuration
to (effectively) call this command after other commands like `git pull`.
```
git config submodule.recurse true
```
This is available in Git versions >= 2.14
~~~

If you are on a different branch (and want to carry your changes with you),
you can now go back to that branch and re-apply your updates _on top_ of the
new trunk. This process is called "rebasing" and can lead to conflicts if the
files you changed are the same as ones changed on `trunk`. For small changes
or additions (e.g. adding a new processor for an analysis), this can be done
with ease and it will make comparing your developments to what is on `trunk`
easier.
```
git switch my-branch
git rebase trunk
```

### Fully Clean Re-Build
Cleaning the source tree is necessary to remove any files generated during the building
process. The programs we use to configure (CMake) and build (make) our software do a pretty
good job of automatically re-building files if the source files change, but we have some
custom configuration that does not follow this protocol and sometimes leads to errors.
To avoid these errors, it is helpful to remove _all_ generated files and start a new
build "clean" (or from scratch). The following `git` commands remove _all_ files that
are not being tracked by `git` (and thus we assume are generated files).
```
git clean -xfd
git submodule foreach --recursive git clean -xfd
```
If you want to persist some files that are within the ldmx-sw directory and are not
being tracked by `git` (for example, some data files), then you will need to at minimum
delete the build and install directories and clean out the generated files from the Framework
directory.
```
rm -r build install
git -C Framework clean -xfd
```
~~~admonish tip title="Shorter Path for Future Updates"
If you are updating *from* a version of ldmx-sw newer that v3.3.4,
then the generated files that used to be written outside of the build directory
are being written inside now. This means you can remove all generated files simply by
```
rm -r build install
```
and without any `git clean` commands.
~~~

The final build and install steps are similar to the past ones. Just note
that they will take longer since the build is starting from scratch.
```
ldmx cmake -B build -S .
ldmx cmake --build build --target install
```

