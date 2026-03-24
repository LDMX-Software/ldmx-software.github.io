# Structure of Event Processors

In ldmx-sw, processors have a structure that overlap between C++ and python where we attempt to use the strengths of both languages.

In C++, we do all the heavy lifting and try to utilize the language's speed and efficiency.

In python, we do the complicated task of assigning values for all of the configuration parameters, regardless of type.

### C++

The C++ part of the event processor is a derived class that has multiple different methods accessing different parts at different points of time along the processing chain. I am not going to go through all of those parts in detail, but I will focus on two methods that are used in almost all processors.

The `configure` method of your event processor is given an object called `Parameters` which contains all the parameters retrieved from python (more on that later).
This method is called immediately after the processor is constructed, so it is the place to set up your processor and make sure it will do what you want it to do.

The `produce` (for Producers) or `analyze` (for Analyzers) method of your event processor is given the current event object.
With this event object, you can access all of the objects that have been previously stored into it and (for Producers only)
put new event objects into it.

Here is an outline of a Producer with these two methods.
**This was not tested.**
It is just here for illustrative purposes.

```cpp
// in the header file
// ldmx-sw/MyModule/include/MyModule/MyProducer.h

namespace mymodule {
/**
 * We inherit from the Producer class so that
 * the application can know what to do with us.
 */
class MyProducer : public Producer {
 public:
  /**
   * Constructor
   * Required to match the structure set up by Producer
   */
  MyProducer(const std::string& name, Process& p) : Producer(name, p) {}

  /**
   * Destructor
   * Marked override so that it will be called when MyProducer
   * is destructed via a pointer of type Producer*
   */
  ~MyProducer() override = default;

  /**
   * Configure this instance of MyProducer
   *
   * We get an object storing all of the parameters set in the python.
   */
  void configure(Parameters& params) override;

  /**
   * Produce for the input event
   *
   * Here is where you do all your work on an event-by-event basis.
   */
  void produce(Event& event) override;

 private:
  /// a parameter we will get from python
  int my_parameter_;

  /// another parameter we will get from python
  std::vector<double> my_other_parameter_;
}; // MyProducer
}  // mymodule


// in the source file
// ldmx-sw/MyModule/src/MyModule/MyProducer.cxx

#include "MyModule/MyProducer.h"

namespace mymodule {

void MyProducer::configure(const Parameters& params) {
  my_parameter_ = params.get<int>("my_parameter");
  my_other_parameter_ = params.get<std::vector<double>>("my_other_parameter");
  
  std::cout << "I also know the name "
      << params.get<std::string>("instance_name")
      << " and class "
      << params.get<std::string>("class_name")
      << " of this copy of MyProcessor" << std::endl;
}

void MyProducer::produce(Event& event) {
  // insert processor's event-by-event work here
}

}  // mymodule

DECLARE_PRODUCER(mymodule::MyProducer);
```

### Python

The python part of the event processor is set up to allow the user to specify the parameters the processor should use.
We also define a class in python that will be accessed by the application.

The python class has three objectives:
 1. Define _all_ of the parameters that the processor requires (and reasonable defaults)
 2. Include the library that the C++ processor is apart of
 3. Tell the configuration what the C++ class it links to is

Here is an outline of the python class that would go with the C++ class `MyProducer` above.

```python
@processor("mymodule::MyProducer", "MyModule")
class MyProducer(Processor) :
    """An outline for a producer configuration in python
    
    Parameters
    ----------
    my_parameter : int
      An example of an integer parameter
    my_other_parameter : list[float]
      An example of a vector of doubles parameter
    """
    
    # define the parameters and their defaults
    # the names of the parameters here should match what is in the C++
    my_parameter: int = 5
    my_other_parameter: list[float] = [1.0, 2.0, 3.0]
```

Now in a configuration script you can create a configuration for MyProducer and (if you want) change some of the parameters to something other than the defaults.
There is a wealth of examples present in `ldmx-sw` - just look in the `python` subdirectory of any module - but I want to highlight some specific features that can be helpful.
- writing a `__post_init__` function can give you access to the configuration class while it is being constructed so you can do more dynamic things like (for example) having some parameters depend on others (maybe the output name depends on which input is being looked at)
- the parameters are spell- and type- checked on the Python side using their spelling and types as written above. This means any parameter changes should be propagated to the `class` _first_ and then the checker can point out where downstream changes are needed

```python
# in a configuration python script
#   my_producer is the python file in MyModule/python
#   that contains the python class definition of MyProducer
from LDMX.MyModule import my_producer
myProd = my_producer.MyProducer(instance_name = 'myProd')
myProd.my_parameter = 10 #will change the 5 to 10 so the C++ class will receive 10
```

# Other Objects
This structure for Event Processors is pretty general,
and actually there are other objects in the C++ application that are configured in this way:
PrimaryGenerators, UserActions, ConditionsObjectProviders, DarkBremModels, BiasingOperators.
