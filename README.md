# ldmx-software.github.io
Documentation for all LDMX software packages.

# Building
This site is built with [mdbook](https://rust-lang.github.io/mdBook/index.html) to generate
the website from markdown files. If you wish to contribute a large amount of documentation,
it may be helpful to install `mdbook` and develop locally using `mdbook serve`. If you
are simply contributing single-page changes/additions, editing the file in the browser
at GitHub is probably sufficient since the GitHub-rendering of markdown is very close
to the mdbook-rendering.

# Notes
Some notes on how this site is structured and built.

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
In order to prevent confusion, I've added in some symlinks from the old manual paths to the new paths.
These are the `_doxygen/index.html` and `_sphinx/index.html` links and a similar strategy could be
used in the future if other links wish to be deprecated. I don't see a reason to ever remove these links
unless we can find a way to check that nobody is using them.
