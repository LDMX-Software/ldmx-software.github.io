# ldmx-sw Framework Structure

ldmx-sw is organized into "modules" that contain related code, the `Framework` module
is of particular importance since it defines the core processing interfaces and handles
reading/writing data from/to the ROOT files.

## Where is the `main`?
Many developers, especially those who are more familiar with C++, will want to know
where the `fire` executable is defined.
`fire` is defined within `Framework/app/fire.cxx` and this file reveals the overall
flow of the program.

1. Configure - run the provided Python script and then extract the run configuration
    from the Python objects that were created when the script was run.
2. Run - execute the configured run. The `framework::Process` class is the main object
    that handles the execution.

## How does Python get run?
We launch Python from within our C++ program by
[embedding Python](https://docs.python.org/3/extending/embedding.html).
In the configuration area of `Framework`, you'll see may of these calls to Python's
C interface (like `Py_InitializeEx()` for example).
