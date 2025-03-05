# But... Why?

Editorial written by Tom Eichlersmith in August 2024.

Our [using](../using/getting-started.md) and [developing](getting-started.md)
workflows are somewhat contrived and so many other LDMX collaborators
(particularly those with more software experience) have asked me a variation
on this question. I think the answer to this question can be best given
with historical context and so I break this apart into three "why" questions
that follow the history of how I got to this workflow.

## Why Containers?
ldmx-sw is the mixed C++ and Python project I talk about within
[the motivation for denv](https://tomeichlersmith.github.io/denv/background/motivation.html)
and so I would direct your attention to that page for why containers at all.

In short, containers provide **stability** by fixing the same software stack
all the way down to the kernel (but not including the kernel!), **maneuverability**
by allowing sharing of this software stack in a known way ("images"), and **usability**
by offputting any OS-related support issues to the more widely used and
developed "runners" that handle creating these containers from their images.

## Why `denv` and not `scripts/ldmx-env.sh`?

For a few years, the bash function `ldmx` and its sub-functions
defined within `scripts/ldmx-env.sh` have served us well.
It has allowed us to utilize containers in a quick and easy way
from the most to least experience coders to share identical environments.

However, over these intervening years, I experienced some friction
that can be summarized in two main issues with this bash function
solution.

1. As the underlying Operating Systems and the container runners
   evolved, new issues revealed themselves in the ldmx-env script
   which were mostly encountered by new users bringing their new
   computers. This extra friction for new users could be ameliorated
   by more strictly testing the container running procedure, but
   testing the `ldmx` bash functions would be difficult to implement
   since they are embedded within ldmx-sw.

2. I noticed that other projects would benefit from containerizing
   the base software stack. Most obviously to me were pythonic analysis
   which benefit from using newer Python versions that were not installed
   natively on the cluser or within our rather large image built for
   compiling and running ldmx-sw.

Both of these issues can be resolved by putting these bash functions
into their own project. `denv` is more strictly unit tested, is
project agnostic (just bring an image to develop within), is
arguably the most cross platform executable (a POSIX-sh compliant script),
and supports more container runners than the original bash functions.

In addition, for LDMX specifically, since we build version releases of
ldmx-sw into their own container images, folks can use ldmx-sw without
even having to clone it! This is especially helpful when doing intricate
physics studies where the specific version of ldmx-sw can be pinned for
reproducibility.

## Why `just` instead of custom scripts or nothing at all?

In general, sharing common commands or sets of commands between different
developers on a project is helpful so that people do not have to worry about
typing as much and can be more certain they are running the correct commands
for their goals.
Many programs have arisen to accomplish this goal and I refer to these
as "task runners" (GNU's `make` is one very common example).

The `ldmx` suite of bash functions partially accomplished the "task runner" goals
with subcommands like `clean` and `checkout` attempting to share common "tasks"
with all of the developers of ldmx-sw.
When designing `denv`, I didn't want to attempt to create yet another task runner so
I omitted those commands or defining a more generic "task running" feature.

This leaves a few paths forward when moving away from the `ldmx` bash functions
and towards `denv`.

- Adopt a task runner to use as developers of ldmx-sw (my choice).
- Write our own custom solution sharing common tasks (I don't like this because it puts more developing load on us.)
- Don't attempt to share tasks and rely on documentation (I don't like this because it puts more documentation load on us.)

As mentioned earlier, there are many programs satisfying the "task runner" description
(just search "task runner" on GitHub) and - while I am very committed to having _a_ task runner -
I am not very committed to any particular task runner.
I chose `just` because I liked how easy it was to install, how simple the syntax is for
defining tasks (or what it calls "recipes"), and its [promise of stability](https://just.systems/man/en/backwards-compatibility.html).
Perhaps a different task runner more well-suited to our purposes will come along and
we will transition from a `justfile` to some other storage of our shared tasks.
