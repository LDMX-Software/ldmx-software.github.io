# ldmx-software.github.io
Documentation for all LDMX software packages.

# Building
This site is built with [mdbook](https://rust-lang.github.io/mdBook/index.html) to generate
the website from markdown files. If you wish to contribute a large amount of documentation,
it may be helpful to install `mdbook` and develop locally using `mdbook serve`. If you
are simply contributing single-page changes/additions, editing the file in the browser
at GitHub is probably sufficient since the GitHub-rendering of markdown is very close
to the mdbook-rendering.

In addition to `mdbook`, we also use an `mdbook` plugin `mdbook-admonish` which you can
install using `cargo` like you would for `mdbook`. Honestly, the best reference for how
to install these tools is shown in [the workflow itself](.github/workflows/mdbook.yml),
but `mdbook` is Rust-based and is very multi-platform. The first line is all that would
change depending on your OS and you can see the full options at [rustup.rs](https://rustup.rs/#).
```shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup update
cargo install --version 0.4.36 --locked mdbook
cargo install --version 1.14.0 --locked mdbook-admonish
```
After these parts are installed (takes ~10min) you can clone this repository and "serve"
the site so you can view it in your browser. The files within the `src` directory are watched
and the site in your browser will be updated to any changes you introduce.
```shell
git clone git@github.com:LDMX-Software/ldmx-software.github.io
cd ldmx-software.github.io
mdbook serve
# click on the link printed to the terminal or copy it into your browser
```
If you are adding a new file, you will need to create a new `.md` file in the `src`
directory and decide where it should go in the site by putting a link to it in the `SUMMARY.md`
file that `mdbook` uses as a reference.

# Notes
Some notes on how this site is structured and built.

### Special Text Blocks
Often when writing documentation, you want to draw the reader's attention to specific pieces of text.
We incorportated [mdbook-admonish](https://tommilligan.github.io/mdbook-admonish/) into this setup to
allow for this. Writers are highly encouraged to use mdbook-admonish text blocks in their rendered
pages to help make the documentation easier to read. The linked page above gives examples on how
to write these code blocks (and shows how they get rendered), but you can also browse the markdown
for this site to see some examples as well.

### Manual Redirects
We can use [a nifty HTML trick](https://www.w3docs.com/snippets/html/how-to-redirect-a-web-page-in-html.html)
to redirect any links in the sidebar of the website to other websites.
```html
<meta http-equiv="refresh" content="0; url='<destination URL>'" />
```
In some browsers, this will still flash the HTML page and in really old browsers this may not work
so it is helpful to put the link to the destination in the `<body>` of the page so users can
access it if the redirect fails.

Right now, the redirects I've added do not do any styling of the page that is displayed while
the browser is redirecting. This could be improved to use the mdbook style like all of the other
pages but I'm unsure on how to do this. One method could be to use mdbook's
[preprocessors](https://rust-lang.github.io/mdBook/format/configuration/preprocessors.html) to
write a basic redirect file which is then updated to the correct style by mdbook's HTML renderer.

### Old Links
In order to prevent confusion, I've added some redirects to mdbook so that old paths to the
reference manuals are still usable. If any future pages are moved/renamed, one should consider
doing the same so that the page is still accessible.

### LaTeX Support
[mdbook supports LaTeX through Mathjax](https://rust-lang.github.io/mdBook/format/mathjax.html).
We've enabled mathjax support for this book so the only thing documentation writers need to
know is that the open/close brackets are different.
- Inline equations are marked by `\\(` and `\\)`
- Block equations are marked by `\\[` and `\\]`
