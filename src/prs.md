# PRs in ldmx-sw
This page goes through a little more detail on the workflow for handling PRs we have settled on.
Hopefully this page contains some helpful tips and tricks for folks who end up helping develop
and maintain ldmx-sw in the future.

## Reviewing a PR
Besides checking that the tests pass and the code is formatted well, one should also encourage
developers to add more documentation as they develop. The code we have is extremely complicated
and if everyone adds just a bit of documentation to the parts of the software they touch, we can
continuously improve our documentation while improving our software.

Oftentimes, changes will fail the PR Validation tests. This is a common occurrence because the
tests involve comparing distributions based on a very strict KS test - so strict that simply changing
the random numbers generated during the simulation will cause the test to fail. In the event of this
failure, we will want to look at these distributions to make sure they are failing for good reasons
(e.g. if we fixed a patch that should change the distributions, we should check that only the expected distributions change). Unfortunately, posting images directly to PRs in a programatic fashion is not supported by GitHub[^1]
and so you will need to go to the page for the "Action" that was run and download its "Artifacts".

[^1]: I should emphasize the _programatic_ part. If there are a few of the PR Validation plots that are pertinent to the PR and should be persisted, please upload them to the PR as a comment. This will mean they will last longer than the artifacts themselves which are removed after 90 days. The way other developers get around this restriction is by having some other server host their images for them and then they programatically post links to these images in the GitHub PR. I (Tom E) searched around for an easy-to-use and/or free service but could not find one - turns out hosting images is difficult due to their size and complexity.

### Action Page
If you click on "Details" for the PR Validation for one of the "PR Validation" steps you can see the running
log of that step (which may be helpful for debugging purposes). To get the Artifacts which contain the plots,
one must then go to the "Summary" - the Artifacts are below the diagram of the steps and below the "Annotations"
showing errors or warnings from the run.

### Artifacts
Each artifact is a `zip` package containing a `tar.gz` archive of all of the distributions that were tested.
Each distribution is plotted for both `trunk` and the developments in the PR and the plots are sorted into two
directories: `pass` which passed the KS test and `fail` which failed the KS test. Since the KS test is so strict,
it is generally safe to ignore the plots in the `pass` directory (unless you are expecting a specific distribution
to change and it doesn't).

### Failed PR Validation
If the PR Validation plots have failed and the reason for their failure is understood and desired, then the developer merging the PR should make a release of ldmx-sw. This triggers another GitHub action which will produce new distributions for the updated `trunk` that can be used to test future PRs. Unless the changes merged in are "major" (whatever that means), it is fair to default to just incrementing the patch number. This workflow means we are generating a lot of releases, but it is very helpful for keeping a very good record of what changed, why it changed, and how it changed.
