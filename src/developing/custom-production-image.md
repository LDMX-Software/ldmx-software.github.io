# Building a Custom Production Image

Using a container has many advantages and one of them is the ability to develop code on one machine (e.g. your personal laptop), 
but the deploy the _exact same code_ to run on several other computers (e.g. SLAC batch computing).
This page details a process you can follow to generate your own production image that has your developments of ldmx-sw inside of it.
Refer to the [Batch Computing](../using/batch.md) for how to use these production images.

Building a docker image is complicated, but hopefully you can get one of the two methods listed below to work for your specific case.
The common denominator in these methods is that you *need* to have a DockerHub repository that you have administrator access to.

0. Make an account on [Docker Hub](https://hub.docker.com/)
1. Make a repository in your account for your production image (name it something related to your project)

### Method 1: Use GitHub Actions
With the validation of v3.0.0 of ldmx-sw, a new GitHub actions and workflow ecosystem was developed.
This included the ability for users of ldmx-sw to manually launch the workflow that builds a production image.

#### Requirements
- Your development branch must be able to be compiled in the same manner as `trunk` (same cmake and make commands)

#### Steps
2. Add `omarmoreno` as a [collaborator](https://docs.docker.com/docker-hub/repos/#collaborators-and-their-role) on the new repository you created 
   (This is the username that will be pushing any generated production images to DockerHub).
3. Go to the [Build Production Image](https://github.com/LDMX-Software/ldmx-sw/actions/workflows/build_production_image.yml) workflow on the "Actions" page.
4. Select "Run Workflow" and input your values for the three parameters. Leave the drop down menu to the value `trunk` - that is the branch on which the workflow is run.
   - `repo`: **required** DockerHub repository that you want the image to be pushed to (same as repo you created earlier - e.g. `tomeichlersmith/eat`)
   - `branch`: (optional) name of branch you want to be compiled into the production image (e.g. `iss420-my-cool-devs`, default is `trunk`)
   - `tag`: (optional) helpful name to call this version of your production image (e.g. `post-bug-fix`, default is `edge`)

Using this method, the production image will be built on your input branch **only** when you "dispatch" the workflow manually.
The new version of the production image will be tagged with the input tag you give it as well as the GitHub commit SHA of the branch you are building.

### Method 2: Manually on your Own Computer

This method is helpful for users who want to have more control over what is pushed to DockerHub.
For example, you may wish to include other code in the production image (not just what is inside ldmx-sw).

#### Requirements
- `docker` installed on a computer (call this the local computer)
- Time : it takes anywhere from 20min to an hour to build an image

#### Steps
2. Double check your developments are all good. Make sure you can compile, install, and run _ldmx-sw_ the way that you want to using a development container.
3. Build the production container. (Fill in the last part with the appropriate details).
```
cd ldmx-sw
docker build . -t docker-user-name/docker-repo-name:some-tag
```
4. (Optional) You can also build ldmx-analysis into your production image if you have analyses you want to include. Notice that the `BASE_IMG` is the image you just built with ldmx-sw. If you only have analyses and you no changes to ldmx-sw, you could substitute a standard production image build for the `BASE_IMG` (e.g. `ldmx/pro:latest`).
```
cd ldmx-analysis
docker build . --build-arg BASE_IMG=docker-user-name/docker-repo-name:some-tag \
  -t docker-user-name/docker-repo-name:som-tag-with-ana
```
5. If the build finishes without any glaring errors, push it to your repository on Docker Hub.
_Note: If you haven't yet, you may need to `docker login` on your computer for this to work._
```
docker push docker-user-name/docker-repo-name:some-tag
```
