# Contributing

```admonish success title="All contributions are welcome."
From fixing typos in these documentation pages to patching a bug in the event reconstruction code to adding a new simulation process. Please reach out via GitHub issues or on the LDMX slack to get started.
```

To contribute code to the project, you will need to create an account on [github](https://github.com/) if you don't have one already, and then request to be added to the [LDMX-Software](https://github.com/orgs/LDMX-Software/) organization.

When adding new code, you should do this on a branch created by a command like `git checkout -b johndoe-dev` in order to make sure you don't apply changes directly to the master (replace "johndoe" with your user name).  We typically create branches based on issue names in the github bug tracker, so "Issue 1234: Short Description in Title" turns into the branch name `1234-short-desc`.

Then you would `git add` and `git commit` your changes to this branch.

If you don't already have SSH keys configured, look at the [GitHub directions](https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent). This makes it easier to push/pull to/from branches on GitHub!

## Pull Requests

We prefer that any code contributions are submitted via [pull requests](https://help.github.com/articles/creating-a-pull-request/) so that they can be reviewed before changes are merged into the master.

Before you start, an [issue should be added to the ldmx-sw issue tracker](https://github.com/LDMXAnalysis/ldmx-sw/issues/new).

### Branch Name Convention
Then you should make a local branch from `trunk` using a command like `git checkout -b iss1234-short-desc` where _1234_ is the issue number from the issue tracker and `short-desc` is a short description (using `-` as spaces) of what the branch is working one.

Once you have committed your local changes to this branch using the `git add` and `git commit` commands, then push your branch to github using a command like `git push -u origin 1234-short-desc`.

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

## Rebasing
In ldmx-sw, I (Tom Eichlersmith) have pushed (pun intended) to rebase branches before merging them into ldmx-sw trunk so that
the commit history is as linear as possible.

~~~admonish tip title="Learn More"
`git`'s [page on rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing) gives helpful description
and includes a discussion on the pros and cons of using this rebasing style (as opposed to simply merging
and creating merge commits).
~~~

Oftentimes since ldmx-sw is such a large code base, the files that two developers work on do not conflict
and therefore changes can be rebased automatically without human intervention.
This is done in most PRs by GitHub when the "Rebase & Merge" button is pressed; however,
some branches need to be manually rebased by a developer in order to handle the case where two developers
have changes the same lines of a file. This section is focused on that manual rebase procedure.

```
# make sure `trunk` is up to date so I don't have to do this again
git fetch
git switch trunk
git pull
git switch iss1373
```
To first order, `rebase` _re-applies_ the changes from commits onto the new "base" (Here, your current branch is "based" on an old commit of trunk and we are updating the base to be the latest commit on trunk.) Often times, there are commits that don't need to be re-applied (you tried them and then later undid them because they didn't work or whatever); thus, I start an `--interactive` rebase.
```
git rebase --interactive
```
Now a file is open listing the different commits that would be re-applied. The syntax for how to interact with these commits is at the bottom of this file. Most often, I just remove the lines with commits that I don't want to keep. Once you save and exit this file the rebase begins.

If there is a CONFLICT, make sure to resolve it. There are many tools available to more quickly resolve conflicts, but the simplest is just to open the file and look for the area with `<<<<<` denoting the beginning of the conflicting section. This corresponds to the two changes (the commit already on `trunk` and your commit that is being re-applied).

Once you've resolved the conflict, you `git add <file>` and `git rebase --continue`.

This cycle continues until all commits have been re-applied. You may have some commits that don't have any conflicts. These commits will just be automatically applied and the rebase continues unless you changed the command associated with that commit in the file opened earlier.

Now you have a rebased branch on your _local_ computer. Double check that things work as intended (e.g. at least compiles) and that the changes you want to make are included. I often do this by `git diff trunk` to make sure my changes (and only my changes) are different compared to the latest trunk.

Once you are certain that everything is good and rebased, you can push your branch `git push`. Rebasing _rewrites_ commits so you may need to `git push --force` to _overwrite_ the copy of your branch on GitHub. **Again, double check the changes and test them!!**
