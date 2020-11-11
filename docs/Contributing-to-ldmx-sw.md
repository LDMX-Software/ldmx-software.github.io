---
layout: default
---

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

## Code Style
In ldmx-sw we follow the [Google Style Guide](https://google.github.io/styleguide/cppguide.html). Some helpful configurations for popular text editors are listed below.

- [emacs](https://raw.githubusercontent.com/google/styleguide/gh-pages/google-c-style.el)
- [google/vim-codefmt](https://github.com/google/vim-codefmt)
- [rhysd/vim-clang-format](https://github.com/rhysd/vim-clang-format)
