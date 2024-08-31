# Quick Switch to `denv`+`just`

No frills, no explanations.

If anything goes wrong, fall back to the more full getting
started guides for [using](../using/getting-started.md) (for details on `denv`)
or [developing](getting-started.md) (for details on `just`).

This is targeted towards LDMX contributors who were present
before the transition to `denv`+`just` so they already have
a container runner present on their machine.

```sh
# install denv into ~/.local
curl -s https://raw.githubusercontent.com/tomeichlersmith/denv/main/install | sh 
# install just into the same location
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh |\
  bash -s -- --to ~/.local/bin
# add just tab completion to your ~/.bashrc
printf '\neval "$(just --completions bash)"\n' >> ~/.bashrc
```

The `denv` install script attempts to help you update your `~/.bashrc`
so that `~/.local/bin` is in your `PATH` and discoverable by `bash` as
a program, but you may need to update your `PATH` manually.
