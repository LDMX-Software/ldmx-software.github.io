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
// ldmx-sw/Module/include/Module/MyProducer.h

namespace module {
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
   * Configure this instance of MyProducer
   *
   * We get an object storing all of the parameters set in the python.
   */
  void configure(Parameters& params) final override;

  /**
   * Produce for the input event
   *
   * Here is where you do all your work on an event-by-event basis.
   */
  void produce(Event& event) final override;

 private:
  /// a parameter we will get from python
  int my_parameter_;

  /// another parameter we will get from python
  std::vector<double> my_other_parameter_;
}; // MyProducer
}  // module


// in the source file
// ldmx-sw/Module/src/Module/MyProducer.cxx

#include "Module/MyProducer.h"

namespace module {

void MyProducer::configure(const Parameters& params) {
  my_parameter_ = params.getParameter<int>("my_parameter");
  my_other_parameter_ = params.getParameter<std::vector<double>>("my_other_parameter");
  
  std::cout << "I also know the name "
      << params.getParameter<std::string>("instanceName")
      << " and class "
      << params.getParameter<std::string>("className")
      << " of this copy of MyProcessor" << std::endl;
}

void MyProducer::produce(Event& event) {
  // insert processor's event-by-event work here
}

}  // module

DECLARE_PRODUCER_NS(module, MyProducer);
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
class MyProducer(Producer) :
    """An outline for a producer configuration in python
    
    Parameters
    ----------
    my_parameter : int
      An example of an integer parameter
    my_other_parameter : list[float]
      An example of a vector of doubles parameter
    """

    def __init__(self,name) :
        super().__init__(
            name, # unique instance name because you could have more than one copy of a processor
            'cool::MyProducer', #the full name including namespaces of the C++ class
            'MyModule' #the name of the module this processor is in (e.g. Ecal or Analysis)
            )
        
        # define the parameters and their defaults
        #   notice that the names of the parameters
        #   are what we look for in the C++ configure method
        self.my_parameter = 5
        self.my_other_parameter = [ 1. , 2. , 3. ]
```

Now in a configuration script you can create a configuration for MyProducer and (if you want) change some of the parameters to something other than the defaults.

```python
# in a configuration python script
#   my_producer is the python file in MyModule/python
#   that contains the python class definition of MyProducer
from LDMX.MyModule import my_producer
myProd = my_producer.MyProducer('myProd')
myProd.my_parameter = 10 #will change the 5 to 10 so the C++ class will receive 10
```

# Other Objects
This structure for Event Processors is pretty general,
and actually there are other objects in the C++ application that are configured in this way:
PrimaryGenerators, UserActions, ConditionsObjectProviders, DarkBremModels, BiasingOperators.
