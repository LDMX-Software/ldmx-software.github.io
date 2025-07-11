# Logging

In ldmx-sw, we use the [logging library from boost](https://www.boost.org/doc/libs/1_63_0/libs/log/doc/html/index.html).
The initialization (and de-initialization) procedures are housed in the `Logger` header and implementation files in the `Framework` module. The general idea is for each class to have its own logger which gives a message and some meta-data to the boost logging core which then filters it before dumping the message to sinks. In our case, we have two (optional) sinks: the terminal and a logging file. All of the logging configuration is done by the parameters passed to the Process in the python configuration file.

## Configuration
The python class `Process` has the `logger` member that configures how the logging works.

Parameter | Description
---|---
`filePath` | path to logging file. No logging to file is done if this is not set.
`fileLevel` | Logging level (and above) to print to the file
`termLevel` | Logging level (and above) to print to the terminal

Besides these parameters you can set directly, the `logger` also has
the ability to customize logging levels depending on the name of the logging
channel (usually the processor's name).

### Examples
to lower the level for everyone
```python
p.logger.termLevel = 0
```
to debug a specific processor
```python
p.logger.debug(my_processor)
# OR
p.logger.debug("MyProcessorName")
```
to silence a specific processor
```python
p.logger.silence(my_processor)
# OR
p.logger.silence("MyProcessorName")
```
or something in between
```python
p.logger.custom(my_processor, level = 1)
```
It is usually better to provide the processor object
instead of the string in order to avoid typos, but
the string option is there in case you don't have easy
access to the channel configuration object yourself.

The logging levels are defined in the `Logger` header file, and a general description is given below.
Right now, configuration uses the `int` equivalent while the C++ uses the enum `level`s.

## Basics: Logging in Processors

In order to save time and lines of code, we have defined a macro that can be used anywhere in ldmx-sw.
```c++
ldmx_log(info) << My message goes here;
```
`info` is the severity level of this message. A severity level can be any of the following:

Level | Int | Description | Example | Printout frequency
--- | --- | --- | --- | ---
`trace` | -1 | Printouts for cases that are more verbose than what you would put for `debug | SimHit level information, or processes that are skipped in the end, or printouts that only help to see that the code got to line xyz, but  are not very helpful for the end user | Several dozens
`debug` | 0 | Extra-detailed information that you would want if you were suspicious that things were running correctly | Whether a sensitive detector is skipping a hit or not | Few O(10) / event
`info` | 1 | Helpful comments for checking operations, average one message per event per channel | What processes are enabled in Geant4, event-level information like the number of hits | O(1) / event
`warn` | 2 | Something wrong happened but its not too bad | REGEX mismatch in GDML parsing | O(10) / run
`error`| 3 | Something _really_ wrong happened and the user needs to know that something needs to change | Extra information before an `EXCEPTION_RAISE` calls  | O(1) / run
`fatal`| 4 | Reserved for run-ending exceptions | Message from catches of `Exception` | 1 / run

This is really all you need for an `EventProcessor`. Notice that the logger _does not_ need a new line character at the end of the line. The logger automatically makes a new line after each message.

## More Detail: Logging Outside Processors

There are some other inheritance trees inside of ldmx-sw that have `theLog_` as a protected member variable (like how it is set up for processors). For example, `XsecBiasingOperator`, `UserAction`, and `PrimaryGenerator`, so you _may not_ need to define a new member `theLog_` in your class if it inherits from a class with `theLog_` already defined and accessible (i.e. public or protected).

There is _a lot_ going on under the hood for this logging library, but I can give slightly more detail to help you if you want to have logging inside of a class that does not inherit from a class that already has the log defined. Basically, each class has a member variable called `theLog_` that is constructed by `makeLogger`. The logger has an associated attribute that boost calls a "channel": a short name for the source of the message. For example, inside of a processor, the channel is the name of the processor. There is another convenience wrapper around the necessary code to "enable logging" inside of your class. Again, this is best illustrated by an example:
```c++
//myClass.h
#include "Framework/Logger.h" //<-- defines the macros you need
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
