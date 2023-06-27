---
layout: default
---

In ldmx-sw we use an several tools for our testing framework: 
- [Catch2](https://github.com/catchorg/Catch2/blob/master/docs/tutorial.md#top)
- [ctest](https://cmake.org/cmake/help/latest/manual/ctest.1.html)
- [GitHub Actions](https://github.com/features/actions)

# Catch2 Basics 
This testing framework allows us to write several different testing functions throughout all of ldmx-sw, which are then compiled into one executable: `run_test`. This executable has several command line options, all of which are detailed in Catch2's [reference documentation](https://github.com/catchorg/Catch2/blob/master/docs/Readme.md#top). This documentation does an excellent job detailing how to write new tests and how to have your tests do a variety of tasks; please refer to that documentation when you wish to write a test.

By default, we add `run_test` as an executable to the list of tests that `ctest` should run.

The basic idea behind Unit Testing is to make sure that we change only what we want to change. The compiler in C++ does a good job of catching syntax errors and writing tests using this package allows us to test the run-time behavior of `fire` in a similar way.

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

Just to give you an example, here is a basic test that would be compiled into the `run_test` executable.

```c++
//file is MyModule/test/MyTest.cxx
#include "catch.hpp" //for TEST_CASE, REQUIRE, and other Catch2 macros

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

## Testing Event Processors
The complicated nature of how we use our event processors is complicated to test. Here I outline a basic structure for writing a test to check a specific processor (or a series of processors).

The basic idea is to set up special processors to setup what your processor should see and to check what it produces.

```c++
#include "catch.hpp"

#include "Framework/Process.h"
#include "Framework/ConfigurePython.h"
#include "Framework/EventProcessor.h"

namespace ldmx {
namespace test {

/**
 * This Processor produces any and all collections or objects that your processor
 * needs to function. You can do this in a specific way that makes it easier to 
 * check later in the processing.
 */
class SetupTestForMyProcessor : public Producer {
 public:
  SetupTestForMyProcessor(const std::string &name,Process &p) : Producer(name,p) { }
  ~SetupTestForMyProcessor() { }
  
  void produce(Event &event) final override {
    //put any collections that your processor(s) use into the event bus
    //make sure these collections have a specific form that you can test easily
    //  (no random-ness)
  }
}; //SetupTestForMyProcessor

/**
 * This Analyzer is what actually does all the CHECKing.
 *
 * You run this processor after the processor(s) that you are testing,
 * so you have access to both the input objects made by the set
 * up processor and the objects created by your processor(s).
 */
class CheckMyProcessor : public Analyzer {
 public:
  CheckMyProcessor(const std::string &name,Process &p) : Producer(name,p) { }
  ~CheckMyProcessor() { }
  
  void analyze(const Event &event) final override {
    //Use CHECK macros to see if the event objects
    // that your processor(s) produced are what you expect
  }
}; //SetupTestForMyProcessor

} //test
} //ldmx

// Need to declare the processors we wrote
DECLARE_PRODUCER_NS(ldmx::test,SetupTestForMyProcessor)
DECLARE_ANALYZER_NS(ldmx::test,CheckMyProcessor)

/**
 * The TEST_CASE is actually pretty short since all of the setup
 * and checking is done in the test processors above.
 *
 * Here we simply write a configuration file that is then given
 * to ConfigurePython to make a process which we then run.
 */
TEST_CASE( "Testing the full running of MyProcessor" , "[MyModule]" ) {
  const std::string config_file{"/tmp/my_processor_test.py"};
  std::ofstream cf( config_file );

  cf << "from LDMX.Framework import ldmxcfg" << std::endl;
  cf << "p = ldmxcfg.Process( 'testMyProcessor' )" << std::endl;
  cf << "p.maxEvents = 1" << std::endl;
  cf << "p.outputFiles = [ '/tmp/my_processor_test.root' ]" << std::endl;
  cf << "p.sequence = [" << std::endl;
  cf << "    ldmxcfg.Producer('Setup','ldmx::test::SetupTestForMyProcessor','MyModule')," << std::endl;
  cf << "    #put your processor(s) here " << std::endl;
  cf << "    , ldmxcfg.Analyzer('Check','ldmx::test::CheckMyProcessor','MyModule')," << std::endl;
  cf << "    ]" << std::endl;

  /* debug pause before running
  cf << "p.pause()" << std::endl;
  */

  cf.close();

  char **args;
  ldmx::ProcessHandle p;

  ldmx::ConfigurePython cfg( config_file , args , 0 );
  REQUIRE_NOTHROW(p = cfg.makeProcess());
  p->run();
}

```

# ctest in ldmx-sw
Currently, we add different Catch2-tests grouped by which module they are in to the general `ctest` command to run together.
Further development could include other tests to be attached to `ctest`. 


## Invoking the test suite 
To run the full test suite enter the build directory and invoke `ldmx ctest`. 

```sh 
cd build 
ldmx make install 
ldmx ctest
```

Some useful options for `ctest` include 
- `--rerun-failed` Will skip any tests that didn't fail last time 
- `--output-on-failure` Will output the contents of `stdout` of any failing test 
- `--verbose`/`-V` and `--extra-verbose`/`-VV` 

If you want to pass any command line arguments to the `run_test` executable (see [Catch2 documentation](https://github.com/catchorg/Catch2/blob/devel/docs/command-line.md#top)), you will have to invoke the executable directly. A common reason for doing this would be to run a particular subset of the test suit, e.g. all the tests in the `Ecal` module. To invoke the executable manually, enter the `test` directory in the build directory and run the executable in the build directory 
```sh 
cd build
ldmx make install 
cd test/
ldmx ../run_test [Ecal] # Only run tests matching [Ecal]
```

*Note:* Since the python configuration will import python modules from the install directory, you have to run `ldmx make install` and not just `ldmx make` before running your tests if you have made changes to any python files.
 
# GitHub Actions and ldmx-sw
We use a variety of GitHub actions to write several different GitHub workflows to not only test ldmx-sw, but also generate documentation and build production images.
A good starting place to look at these actions is in the [.github/workflows](https://github.com/LDMX-Software/ldmx-sw/tree/trunk/.github/workflows) directory of ldmx-sw.
