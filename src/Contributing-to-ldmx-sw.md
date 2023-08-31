To contribute code to the project, you will need to create an account on [github](https://github.com/) if you don't have one already, and then request to be added to the [LDMX-Software](https://github.com/orgs/LDMX-Software/) organization.

When adding new code, you should do this on a branch created by a command like `git checkout -b johndoe-dev` in order to make sure you don't apply changes directly to the master (replace "johndoe" with your user name).  We typically create branches based on issue names in the github bug tracker, so "Issue 1234" turns into the branch name `iss1234`.

Then you would `git add` and `git commit` your changes to this branch.

You can then merge in these changes to the local master by doing `git checkout master` and then `git merge johndoe-dev` which will apply your branch updates.

If you don't already have SSH keys configured, look at the [GitHub directions](https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent). This makes it easier to push/pull to/from branches on GitHub!

## Pull Requests

We prefer that any major code contributions are submitted via [pull requests](https://help.github.com/articles/creating-a-pull-request/) so that they can be reviewed before changes are merged into the master.

Before you start, an [issue should be added to the ldmx-sw issue tracker](https://github.com/LDMXAnalysis/ldmx-sw/issues/new).

Then you should make a local branch from the master using a command like `git checkout -b iss1234` where _1234_ is the issue number from the issue tracker.

Once you have committed your local changes to this branch using the `git add` and `git commit` commands, then push your branch to github using a command like `git push -u origin iss1234`.

Finally, [submit a pull request](https://github.com/LDMX-Software/ldmx-sw/compare) to integrate your changes by selecting your branch in the _compare_ dropdown box and clicking the green buttons to make the PR.  This should be reviewed and merged or changes may be requested before the code can be integrated into the master.

If you plan on starting a major (sub)project within the repository like adding a new code module, you should give advance notice and explain your plains beforehand. :) A good way to do this is to create a new issue. This allows the rest of the code development team to see what your plan is and offer comments/questions.

### After Opening a PR
After opening a PR, several different tests are run using [our GitHub Actions](https://github.com/LDMX-Software/ldmx-sw/actions). One of these tests, the "Recon Validation" takes about three hours to run, so it shouldn't be run on every commit pushed to a pull request. Instead, it is run when the PR is created or when marked "Ready for Review". This enables the following workflow for validating PRs.

1. Check if any of the tests failed. If no tests failed, you are all set to [request another developer to review it](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/requesting-a-pull-request-review)!
2. If any of the tests failed, click on that test to look at what happened.
3. You may need to download some "artifacts" to look at any validation plots that were generated to help with your debugging.
4. If the tests show a bug that you need to fix, [convert your PR to a draft](https://docs.github.com/en/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/changing-the-stage-of-a-pull-request#converting-a-pull-request-to-a-draft) (if it isn't already). If the tests fail but you are confident your changes are the correct version (perhaps you fixed a bug that shows up in the reference histograms), then request another developer's review.
5. Make changes and locally test them to see fix the bugs the test revealed.
6. Pushing these changes will trigger some basic tests on GitHub, but to trigger the more in-depth validation, mark your PR as "Ready for Review".
7. Go back to step 1.

## Code Style
In ldmx-sw we follow the [Google Style Guide](https://google.github.io/styleguide/cppguide.html). Some helpful configurations for popular text editors are listed below.

- [emacs](https://raw.githubusercontent.com/google/styleguide/gh-pages/google-c-style.el)
- [google/vim-codefmt](https://github.com/google/vim-codefmt)
- [rhysd/vim-clang-format](https://github.com/rhysd/vim-clang-format)

## Pull Requests with Submodule Updates
LDMX organizes some of its code in ldmx-sw into 
[git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules) so that they
can be developed somewhat independently from the central ldmx-sw repository.
From a `git` point of view, these git submodules are separate entitites from
ldmx-sw and ldmx-sw only knows the specific commit that it should load when
`git submodules update` is called. For this reason, updates that require changes
to submodules as well as ldmx-sw should have two PRs: one for the updates within
the submodule and one for updating the commit reference of the submodule in 
ldmx-sw.

In order to avoid confusion from commit references that are pseudo-random, it
is **highly encouraged** that a new release and tag are made for the submodule
when updating ldmx-sw to a new submodule version.
