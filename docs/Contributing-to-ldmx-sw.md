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
- All file types 
  - Try not to use tabs anywhere in the project, including data files (set your editor to replace tabs with spaces).
- C++
  - General
    - 4 space indent
    - source files have '.cxx' extension
    - headers have '.h' extension
    - All C++ code with only a few exceptions should be enclosed within a namespace such as `sim`, `event`, etc.
  - Brackets
    - Brackets are always on the same line.
    - One space between bracket and statement on same line
  - Spacing
    - Before and after an equals sign: `int val = 1.234;`
    - Before bracket when it shares a line with a code statement: `if (a == true) {`
    - After a control statement: `for (int i = 0; ...)`, `if (...)`, etc.
  - Classes
    - Classes must be _defined_ in their own `.h` headers, not in `.cxx` files.
    - Class and function names are camelcase.
    - Class methods start with a lower case letter.
    - Class variables are camelcase with an `_` after them.
    - The public/private/protected declaration in a class is indented.
    - Simple variable access methods or "getters" always start with "get".
    - In class definitions, put `typedef` statements first, then the constructor and destructor, followed by public methods, then protected and private methods if applicable, and then class variable definitions.
  - Variables
    - Variables defined as `static const` should be in all caps.
    - Most other variables are camelcase.
  - Headers
    - Define short methods in header files.
    - Use an include guard macro name with the style `DIR_CLASS_H_` such as `EVENT_SIMTRACKERHIT_H_`
- Comments and Doc
  - Use `/** ... */` to denote Doxygen comments in classes and methods.
- Messages and Warnings
  - Send messages/info to `std::cout` and prefix your message with `[ MyClass ] : `.
  - Send warnings to `std::cerr` and prefix your warning with `[ MyClass ] [ WARNING ] : `.
  - Use the `EXCEPTION_RAISE` macro to throw any run-ending exceptions.
- Tests
  - Tests should be defined in the `test` directory of a module, and they should have a name similar to `ldmx_my_test`.
- Programs
  - Files that define a `main` should not define any other classes and should be included in the modules list of executables using the `EXECUTABLES src/ldmx_app.cxx` argument to the `module` macro.
- XML
  - 2 space indent
  - Do not put a space before `/>`.
- CMake
  - 2 space indent
  - Use all lower case macro names e.g.'add_library(someLib)'
  - Avoid insertion of extra spaces like 'add_library( someLib )'
- Python
  - 4 space indent
  - Try to follow the C++ code conventions when possible (???)
