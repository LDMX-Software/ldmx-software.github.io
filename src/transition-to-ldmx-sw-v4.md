# Transition to ldmx-sw v4

~~~admonish note title="TLDR"
If you don't have a branch of ldmx-sw that you wish to update,
the easiest way to update ldmx-sw to v4 is with a new clone.
```
rm -rf ldmx-sw # are you SURE you have no changes? We are deleting everything now...
git clone --recursive git@github.com:LDMX-Software/ldmx-sw.git
```
~~~

Before the major release v4, ldmx-sw contained a lot of git submodules.
They were introduced to try to help improve the developing workflow, but
they ended up being an impedance for how we develop ldmx-sw and so were
removed. Changing a git submodule into a normal subdirectory is a highly
technical change that, while it doesn't change the source code, significantly
alters how users interact with the source code via `git`.

### Goals

This documentation page is here to help users update their local copy of
ldmx-sw from before the v4 transition to after the v4 transition.

- The target audience are those less familiar with `git`
- We aim to avoid manually re-writing changes

~~~admonish warning title="This guide will NOT preserve the history of any branches."
The process described here is similar to "squashing" all of the changes on
a branch into one commit. While the history of a branch is sometimes helpful
when trying to understand the code, carrying the history through this transition
is a complicated process that is non uniform. Discarding the history of a branch
in the way described here will also discard any previous committers or authors
of the changes. Assuming the branch has just been edited by an individual developer,
squashing the changes into one commit and discarding the history is an acceptable
procedure in most cases. **If you have a branch with multiple authors or a history you'd like to
preserve, please reach out.** We can talk about trying to recover the history while
updating the branch.
~~~

With the introduction out of the way, let's get started.

## Step 1: Align branch with ldmx-sw v3.4.0
The last release before the de-submodule transition was v3.4.0,
and in order for the update to work as described below, your
branch must first be "aligned" with this version of ldmx-sw.

```shell
# make sure you have access to the tags of ldmx-sw
git fetch --tags
# merge the v3.4.0 tag into your branch
git merge -s theirs v3.4.0
# check that the resulting diff contains your changes
git diff v3.4.0
```

## Step 2: Prepare to Cross Boundary
The submodule to no-submodule transition is one that `git` struggles with, especially when
going "backwards" (i.e. going from a branch after the transition to one from before the transition),
so it is easiest to make a new clone and rename your old clone to emphasize
that it is the old one.
```
mv ldmx-sw old-ldmx-sw # rename old clone
git clone --recursive git@github.com:LDMX-Software/ldmx-sw.git # get new clone
```
Then create a _new_ branch in the new clone that has the same name as the branch you want to update.
```
git -C ldmx-sw switch --create my-branch
```
~~~admonish warning title="This step should succeed."
If you see any warnings or errors, that means a local copy of `my-branch` already exists in the
new clone of ldmx-sw. This should **not** happen.
~~~

## Step 3: Cross Transition Boundary
The basic idea behind this procedure is to write your changes into
a file (called a "patch" file) and then re-apply those changes onto
the new version of ldmx-sw. The actual procedure for doing this
depends on _where_ your changes are, so the specifics of creating and applying
these patch files are separated into categories depending on where your changes
are. All of the categories assume that you have done Steps 1 and 2 above.

~~~admonish note title="No Changes" collapsible=true
Your branch doesn't have any changes (or you were just running a locally-compiled
version of ldmx-sw trunk).

This is the easiest case and I would just suggest to remove the old clone of ldmx-sw
equivalent to the [TLDR](#admonition-tldr) at the top of the page.
```
rm -rf old-ldmx-sw # are you SURE you have no changes you want to keep?
```
~~~

~~~admonish note title="Changes only in ldmx-sw (and nothing in submodules)" collapsible=true
The changes you made are not in any of the submodules (i.e. you haven't changed files within
`cmake`, `Conditions`, `SimCore`, `Tracking`, `Trigger`, `Framework`, `MagFieldMap`, `TrigScint`,
`Ecal`, or `Hcal`).

This means that the changes you've made can be re-applied to the post-transition ldmx-sw
with relative ease since their location hasn't changed.
```
cd old-ldmx-sw
git diff v3.4.0 > ../my-branch.patch
cd ../ldmx-sw/
git apply ../my-branch.patch
```
~~~

~~~admonish note title="Changes within a submodule" collapsible=true
The basic idea is the same, but since the path to the files being changed also changes,
we need to use an extra argument when applying the changes to the new clone of ldmx-sw.

Call the submodule your changes are in `submodule` (for example, if you have edits in `Ecal`,
the replace `submodule` with `Ecal` in the commands below), then the following lines
will re-apply the changes currently within the `submodule` in the `old-ldmx-sw` clone
of ldmx-sw onto the same files within that directory of the new `ldmx-sw` clone.
```
cd old-ldmx-sw/submodule
git fetch
# the following just gets the default branch of the submodule
# you could equivalently just look it up on GitHub
sm_main="$(git -C ${sm} remote show origin | sed -n '/HEAD branch/s/.*: //p')"
git diff origin/${sm_main} > ../../my-branch.submodule.patch
cd ../../ldmx-sw
git apply --directory=submodule ../my-branch.submodule.patch
```
~~~

~~~admonish note title="Changes across many submodules or in both ldmx-sw and a submodule" collapsible=true
You can combine the two procedures above with the following additional notes.

Follow the [changes within a submodule](#admonition-changes-within-a-submodule) procedure for _each_ submodule.
This is pretty self-explanatory, you could even create a different commit on the newly updated branch for each
submodule if you want.

Exclude any submodule changes when following the
[ldmx-sw only](#admonition-changes-only-in-ldmx-sw-and-nothing-in-submodules) procedure.
This is a bit more complicated. If you know which files are different, the easiest way
to avoid including the submodule changes is to explicitly list the files in ldmx-sw that have changed.
```
git diff v3.4.0 <list of changed files> ../ldmx-sw-only-changes.patch
```
You could also remove the chunks of the `.patch` file manually with a text editor, but that is
more difficult and requires more familiarity with the syntax of patch files.
~~~

## Step 4: Check and Commit
For this final step, we are in the new clone `ldmx-sw` and we've already run `git apply`
(according to the commands in Step 3) so that the changes from the old branch have been applied.

~~~admonish warning title="Check"
Make sure to check that your edits have been applied as you've desired and they work as you
expected. This includes (but is not limited to):
- Look through the output of `git status` to make sure the files you wanted to change are changed
- Look through the output of `git diff` to make sure the files changed how you wanted them to change
- Recompile ldmx-sw with your changes (if they were compiling before the transition)
- Rerun and re-test the changes (if they were running and passing tests before the transition)
~~~

Now that the updates have been properly checked, we can add the changes we've made
and commit them to the new branch in the new clone of ldmx-sw.

```
git add <files-that-you-changed>
git commit
```
~~~admonish tip title=""
Make sure to write a detailed commit message explaining *ALL* of the changes
you've made (not just the most recent ones). Remember, the old commits and their
messages will be deleted!
~~~

~~~admonish warning title="History Loss"
I am pausing here to remind you to double check that your changes are what you expect
and want.
Once we run the next command, the old version of `my-branch` on GitHub will
be deleted and replaced with the new version.
~~~

```
git push --force --set-upstream origin my-branch
```

~~~admonish warning title="History Loss"
I am pausing here to remind you to triple check that your changes are what you expect
and want. Once we run the next command, the old version of `my-branch` on your computer
will be deleted.
Only run this next command when you are done transitioning all of your branches
if you have multiple branches.
~~~

```
cd ..
rm -rf old-ldmx-sw
```

---
# Extra Notes

~~~admonish note title="Movement Issues"
When attempting to go from after the transition to before the transition, `git`
struggles to handle the recursive submodule structure that we had in ldmx-sw. The first
submodule that has this issue is SimCore so you'll see an error like the following
```
fatal: could not get a repository handle for submodule 'SimCore'
```
In this case, I would suggest that you simply make a separate clone of ldmx-sw.
The `--branch` argument to `git clone` allows you to clone a specific branch or tag
rather than the default one (`trunk`) so you can have a clone of a specific branch or tag
that is from before the transition.
```
git clone --branch <name> --recursive git@github.com:LDMX-Software/ldmx-sw.git
```
~~~
