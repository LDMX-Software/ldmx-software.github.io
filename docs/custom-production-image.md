---
layout: default
---

# Make your own Production Image

Using a container has many advantages and one of them is the ability to develop code on one machine (e.g. your personal laptop), 
but the deploy the _exact same code_ to run on several other computers (e.g. SLAC batch computing).
This page details a process you can follow to generate your own production image that has your developments of ldmx-sw inside of it.

### Requirements
- `docker` installed on a computer (call this the local computer)
- Your developments built, compiled, and verified on the same computer
- Access to a batch system that uses `singularity` (e.g. SLAC, call this the batch computer)

### Local Computer
0. Make an account on [Docker Hub](https://hub.docker.com/)
1. Make a repository in your account for your production image (name it something related to your project)
2. Double check your developments are all good. Make sure you can compile, install, and run _ldmx-sw_ the way that you want to using a development container.
3. Build the production container. (Fill in the last part with the appropriate details).
```
cd ldmx-sw
docker build . -t docker-user-name/docker-repo-name:some-tag
```
4. If the build finishes without any glaring errors, push it to your repository on Docker Hub.
_Note: If you haven't yet, you may need to `docker login` on your computer for this to work._
```
docker push docker-user-name/docker-repo-name:some-tag
```

### Batch Computer
0. Decide where you want to save the production image: `export LDMX_PRODUCTION_IMG=$(pwd -P)/ldmx_my_production_image_some_tag.sif`
1. Pull the docker container down from Docker Hub and build it into a `.sif` image file. _Note: This step requires your Docker Hub repository to be public._
```
singularity build ${LDMX_PRODUCTION_IMG} docker://docker-user-name/docker-repo-name:some-tag
```
2. Now you can run a configuration script with your developments in the container using
```
singularity run --no-home ${LDMX_PRODUCTION_IMG} . config.py
```
This is the command you want to be giving to `bsub` or some other submission program.
The only files it needs access to are the configuration script that you want to run and the `.sif` image file;
both of which are only used at the start-up of the container.

#### Submission Script
It is best practice to write a "submission script" that handles the running of this command _and_ any pre- or post- run actions.
A lot of different submission scripts have been written in `bash` and `python`, but they all have a similar structure:
1. Setup the batch environment (e.g. Find singularity image file and turn off email notifications)
2. Configure or write a job script which does all the pre- and post- run actions as well as the `singularity run` command.
   - Go to a scratch or temporary directory to work
   - Pre-Run Actions: copying over input file, inserting parameters into configuration script, etc...
   - Run `singularity run` command
   - Post-Run Actions: copying output files to output directory cleaning up scractch directory
3. Submit the job script using the submission program (e.g. `bsub` or `condor`) however many times

Some examples of submission scripts:
- [ldmx-workflow/batch](https://github.com/LDMX-Software/ldmx-workflow/tree/master/batch)
- [ldmx-sw-scripts/batch](https://github.com/LDMX-Software/ldmx-sw-scripts/tree/master/batch)
