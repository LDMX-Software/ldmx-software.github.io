---
layout: default
---

We just merged in a new testing framework to use with ldmx-sw: [Catch2](https://github.com/catchorg/Catch2/blob/master/docs/tutorial.md#top)

This testing framework allows us to write several different testing functions throughout all of ldmx-sw, which are then compiled into one executable: `ldmx-test`. This executable has several command line options, all of which are detailed in Catch2's [reference documentation](https://github.com/catchorg/Catch2/blob/master/docs/Readme.md#top). This documentation does an excellent job detailing how to write new tests and how to have your tests do a variety of tasks; please refer to that documentation when you wish to write a test.

The basic idea behind Unit Testing is to make sure that we change only what we want to change. The compiler in C++ does a good job of catching syntax errors and writing tests using this package allows us to test the run-time behavior of `ldmx-app` in a similar way.

Catch2 allows us to organize our tests into labels so that the user can run a specific group of tests instead of all at once. A basic structure for ldmx-sw tests is as follows:
1. Put any tests you write into the `test` directory in the module you wish to test.
2. Use the module name as one of the labels for your test.
3. Provide a detailed, one sentence description for your test as the title (spaces are allowed).
4. Use one of the following additional labels as applicable:
 - `[physics]` --> tests that validate that physics is working as we expect (e.g. biasing up PN produces events with PN in them in the correct volume)
 - `[functionality]` --> tests that a certain ability successfully runs the way we expect it (e.g. providing multiple input files and one output file runs without segmentation fault and provides the correct information to all processors)
 - `[dev]` --> test is in development and may have undefined behavior
 - `[performance]` --> test checking the performance of certain functions (e.g. how long do they take? how much memory they use...)

Please follow these guidelines when writing a new test and please write tests often. Unit testing allows us to move forward with developments a lot quicker because we can validate changes quickly.

---

Just to give you an example, here is a basic test that would be compiled into the `ldmx-test` executable.

```c++
//file is MyModule/test/MyTest.cxx
#include "Exception/catch.hpp" //for TEST_CASE, REQUIRE, and other Catch2 macros

/**
 * my test
 * 
 * What does this test?
 *  - I can compile my own test.
 */
TEST_CASE( "My first test can compile." , "[MyModule][meta-test]" ) {
    
    std::cout << "My first test!" << std::endl;

    // this will pass
    CHECK( 2 == 1 + 1 );

    // this will fail but continue processing
    CHECK( 2 == 1 );

    // this will fail and end processing
    REQUIRE( 2 == 1 );

    // this will not be run
    std::cout << "I won't get here!" << std::endl;
} //my test
```
