---
layout: default
---

# Using a Custom Production Image

Using a container has many advantages and one of them is the ability to develop code on one machine (e.g. your personal laptop), 
but the deploy the _exact same code_ to run on several other computers (e.g. SLAC batch computing).
This page details a process you can follow to generate your own production image that has your developments of ldmx-sw inside of it and has two big parts.

1. Building a custom production image with your developments
2. Running any production image (with specific focus on using `singularity`).

## 1. Building a Custom Production Image

Building a docker image is complicated, but hopefully you can get one of the two methods listed below to work for your specific case.
The common denominator in these methods is that you *need* to have a DockerHub repository that you have administrator access to.

0. Make an account on [Docker Hub](https://hub.docker.com/)
1. Make a repository in your account for your production image (name it something related to your project)

### Method 1: Use GitHub Actions
With version v3.0.0 of ldmx-sw, whenever a commit is pushed to the GitHub repository of ldmx-sw, certain actions are run that check if the code can compile and run ldmx-sw.
Part of these actions include compiling the code into a production image, so all that's left for you to do is to tell the action where to push the constructed image to.
This first method is convenient for users who don't have access to a computer with docker installed.

#### Requirements
- Your development branch must be based off of the v3.0.0 (or later) release. _At minimum_, you need to have the same `.github/workflows/build_test_docs.yml` action file.

#### Steps
2. Add `omarmoreno` as a [collaborator](https://docs.docker.com/docker-hub/repos/#collaborators-and-their-role) on the new repository you created (This is the username that will be pushing any generated production images to DockerHub).
3. Create the file `.github/workflows/production_image_repo` in _ldmx-sw_ and put your repository name in it. The full repository name should look like `username/repo_name`.
```
# helpful bash command for doing this
echo username/repo_name > .github/workflows/production_image_repo
```

4. Commit the new file to your branch and push it to GitHub. You should see your production image appear on your DockerHub after about 20 min. You can look at the [Actions page of ldmx-sw](https://github.com/LDMX-Software/ldmx-sw/actions) to see how it is progressing.
```
git add .github/workflows/production_image_repo
git commit -m "attaching my produciton image repo to this branch"
```

Using this method, each commit that you push to this branch will push a new version of the production container with your developments to DockerHub. This new version will be named `edge` as well as have a name corresponding to the git SHA of the commit.

### Method 2: Manually on your Own Computer

This method is helpful for users who want to have more control over what is pushed to DockerHub.
For example, you may wish to include other code in the production image (not just what is inside ldmx-sw).

#### Requirements
- `docker` installed on a computer (call this the local computer)

#### Steps
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

## 2. Running the Production Image on the Batch Computer
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

_Note: On SLAC computers, the default singularity cache directory is $HOME, but SLAC users are not given very much space in $HOME. It may help your singularity build and run commands if you change the cache directory 'SINGULARITY_CACHEDIR' to somewhere with more space._

## 3. Submission Script
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
