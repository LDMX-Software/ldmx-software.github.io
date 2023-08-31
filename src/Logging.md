In ldmx-sw, we use the [logging library from boost](https://www.boost.org/doc/libs/1_63_0/libs/log/doc/html/index.html).
The initialization (and de-initialization) procedures are housed in the `Logger` header and implementation files in the `Framework` module. The general idea is for each class to have its own logger which gives a message and some meta-data to the boost logging core which then filters it before dumping the message to sinks. In our case, we have two (optional) sinks: the terminal and a logging file. All of the logging configuration is done by the parameters passed to the Process in the python configuration file.

## Configuration
The python class `Process` has three parameters that configure how the logging works.

Parameter | Description
---|---
`logFileName` | Name of logging file. No logging to file is done if this is not set.
`termLogLevel` | Logging level (and above) to print to terminal
`fileLogLevel` | Logging level (and above) to print to file

The logging levels are defined in the `Logger` header file, and a general description is given below.
Right now, configuration uses the `int` equivalent while the C++ uses the enum `level`s.

## Basics: Logging in Processors

In order to save time and lines of code, we have defined a macro that can be used anywhere in ldmx-sw.
```c++
ldmx_log(info) << My message goes here;
```
`info` is the severity level of this message. A severity level can be any of the following:

Level | Int | Description | Example
--- | --- | --- | ---
`debug` | 0 | Extra-detailed information that you would want if you were suspicious that things were running correctly | Whether a sensitive detector is skipping a hit or not
`info` | 1 | Helpful comments for checking operations | What processes are enabled in Geant4
`warn` | 2 | Something wrong happened but its not too bad | REGEX mismatch in GDML parsing
`error`| 3 | Something _really_ wrong happened and the user needs to know that something needs to change | Extra information before an `EXCEPTION_RAISE` calls
`fatal`| 4 | Reserved for run-ending exceptions | Message from catches of `Exception`.

This is really all you need for an `EventProcessor`. Notice that the logger _does not_ need a new line character at the end of the line. The logger automatically makes a new line after each message.

There is an additional logging level below "debug". A lot of times during development, a developer puts messages inside of the code to make sure it is working properly. A lot of these extra messages are not very helpful for the end user, so they should go into the log at all. Feel free to leave these messages in, but comment them out so that they don't clog up the log. A good rule of thumb is that the debug channel should have at most one message per event, info - one message every few events, warn - a few messages total per run, and error only one message per run.

## More Detail: Logging Outside Processors

There are some other inheritance trees inside of ldmx-sw that have `theLog_` as a protected member variable (like how it is set up for processors). For example, `XsecBiasingOperator`, `UserAction`, and `PrimaryGenerator`, so you _may not_ need to define a new member `theLog_` in your class if it inherits from a class with `theLog_` already defined and accessible (i.e. public or protected).

There is _a lot_ going on under the hood for this logging library, but I can give slightly more detail to help you if you want to have logging inside of a class that does not inherit from a class that already has the log defined. Basically, each class has a member variable called `theLog_` that is constructed by `makeLogger`. The logger has an associated attribute that boost calls a "channel": a short name for the source of the message. For example, inside of a processor, the channel is the name of the processor. There is another convenience wrapper around the necessary code to "enable logging" inside of your class. Again, this is best illustrated by an example:
```c++
//myClass.h
#include "Exception/Logger.h" //<-- defines the macros you need
class myClass {
 public:
  void someFunctionThatLogs() {
    ldmx_log(info) << "I can log!"; //<-- macro that calls theLog_
  }
 private:
  /** enable logging for myClass */
  enableLogging("myClass") //<-- macro that declares and defines theLog_
};
```
Notice that the macro `enableLogging` is _in the class declaration_. It needs to be here because it declares and defines the member variable `theLog_` --- it is good practice to keep `theLog_` private, so put the macro in the `private` branch of your class declaration. You can provide any channel name to `enableLogging` that you wish, but the class name is a good name to default to.
