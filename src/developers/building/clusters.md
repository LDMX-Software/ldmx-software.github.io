# Shared Computing Clusters

Building, installing, and running ldmx-sw on shared computing clusters is largely
similar to how it is done on personal laptops; however, there are special considerations
to be made that can make it functional.

All of the clusters LDMX has access to are focused on using singularity (or its newer
brand apptainer), so these comments are focused on this runner.

## Image Cache and Build Directories
The `ldmx-env.sh` script moves the singularity cache directory to be within the `LDMX_BASE`
directory. This is done to avoid filling a user's home directory (the default cache location)
with large image layers. Besides the cache directory, singularity also uses a temporary
directory for constructing the final image file. On some clusters (notably SDF), the default
temporary directory is not large enough to fully construct this image file and so it may
need to be moved.

~~~admonish tip title="Environment Variables"
- `SINGULARITY_CACHEDIR` or `APPTAINER_CACHEDIR` can be used to change the location of
  the image layer cache for singularity/apptainer.
- `TMPDIR` is inspected by singularity/apptainer for the temporary build location.
  Change this variable if the build is failing due to disk space issues.
~~~

## Shared Images
We do not run containers that modify the original image, so shared computing clusters
could share a lot of space by have image files be centrally produced and then users all
share the same image files so they don't have to have their own copy.

Currently, there is not a mechanism within the `ldmx-env.sh` script to direct the `ldmx`
command to an area with shared images, but we can circumvent this issue easily with
symlinks. Below, I outline a method to keep all of the LDMX images within one shared
directory that users can use instead of their own copies.

~~~admonish info title="Future Developments"
If `ldmx-env.sh` evolves to support moving the image storage location
(for example by refactoring to use `denv` instead
[Issue #1232](https://github.com/LDMX-Software/ldmx-sw/issues/1232)
which does support this for singularity/apptainer runners),
we could [put the `ldmx/dev` repository onto the CVMFS unpacked.cern.ch
repository](https://cvmfs.readthedocs.io/en/stable/cpt-containers.html#using-unpacked-cern-ch)
which would make the images available via CVMFS saving disk space
and network bandwidth.
~~~

Let `LDMX_SHARED_IMAGES` be an environment variable storing the full path to a directory
that we want to share images in. A single person with access to the cluster and to this
directory should be _the builder_ of these images, everyone else on this cluster is called
a user.

### Builder Steps
Whenever there is a new release of the container image, build it and update the latest
symlink.
```shell
cd ${LDMX_SHARED_IMAGES}
apptainer build ldmx_dev_vX.X.X.sif docker://ldmx/dev:vX.X.X
ln -sf ldmx_dev_vX.X.X.sif ldmx_dev_latest.sif
```

~~~admonish note
This mimics the naming of the `*.sif` files that is done within the `ldmx` command
and avoids copying the latest image, preferring instead to just symlink from the `_latest.sif`
name to the copy of that tag.

Builders will need to be slightly more familiar with apptainer/singularity in
order to issue this command. They may need to change the cache directory with `APPTAINER_CACHEDIR`
or the build directory with `TMPDIR` depending on how much space is available to them
on their cluster.
~~~

### User Steps
In order to use a directory of shared images, one just needs to remember to symlink
the available images into their `LDMX_BASE` area _before sourcing the environment script_.
```shell
ln -sft . ${LDMX_SHARED_IMAGES}/*sif
. ldmx-sw/scripts/ldmx-env.sh
```
This informs `ldmx-env.sh` that the images are already available since they are in the
`LDMX_BASE` directory with the correct names and so `ldmx` will only pull down and make
a copy of an image if it wasn't in the shared images location.
Since the symlinking procedure is rather quick, you could probably just fold this into
every source you do to avoid any forgetfulness.
```shell
# in .bashrc
export LDMX_BASE=/full/path/to/ldmx/base
export LDMX_SHARED_IMAGES=/another/path/to/shared/images
ldmx-env() {
  # make sure list of already downloaded images is up-to-date
  ln -sft ${LDMX_BASE} ${LDMX_SHARED_IMAGES}/*.sif || return $?
  # setup ldmx environment
  . ${LDMX_BASE}/ldmx-sw/scripts/ldmx-env.sh || return $?
  # add a [ldmx] tag to the PS1
  export PS1="[ldmx] $PS1"
  # delete this function to avoid double-environment
  unset -f ldmx-env
}
```
