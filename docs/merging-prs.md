# Merging PRs in ldmx-sw

With our submodule-heavy structure, merging PRs can be complicated. I am taking notes here to reflect the procedure I have used to merge PRs.
This procedure uses [GitHub's CLI `gh`](https://cli.github.com/), but it is not required. You may do those steps in a browser rather than on the command line.

We begin _after_ a PR has been validated - i.e. the developer community has agreed to merge the developments into `trunk`.
The steps are rather simple and can be outlined as

0. Merge submodule PRs into submodule trunks.
1. Update submodule refs in ldmx-sw
2. Merge ldmx-sw PR into ldmx-sw trunk

An example series of commands where we have a PR in Framework with number 69 and a PR in ldmx-sw linked to it with a number 420 is

```
cd Framework
gh pr merge 69
git checkout trunk
git pull
cd ..
git add Framework 
git commit -m "Update Framework submodule for merge of its PR"
git push
gh pr merge 420
```

I often wait for the build/test check to successfully finish before the file merge command as a triple-check that I didn't break anything.
You can do this on the command line with `gh run watch` after getting the GitHub run number using `gh run list`.

This procedure is pretty simple and is a natural extension of regular (no-submodule) merging.
I've done some basic investigation into automating this merging procedure using GitHub actions;
however, GitHub understandably avoids giving its actions the rights to merging PRs.

The next best option would be to develop a bash merging script using `git` and `gh`.
This is convenient because `gh` handles authentication for us,
so it interacts with the GitHub repository in the same was as someone using the browser.
This merging script is difficult to develop because there isn't much opportunity for testing the functionality of such a script.
