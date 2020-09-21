---
layout: default
---

If the objects already in ldmx-sw/Event module do not suit your purposes, you can define your own Event Bus Passenger that will carry your data between processors. You will need to meet a few requirements in order for your class to be able to be added to the event bus.

* Your class must be [in the ROOT dictionary]({% link docs/Adding-a-new-class-to-the-ldmx-framework-ROOT-dictionary.md %}).
* Your class shouldn't use `TRef` (or any derived class)
* The type of class you wish to be in the event bus needs to be added to the EventBusPassenger variant type in `Event/include/EventDef.h`. This could be your class or a container of your classes. See the EventDef file for examples.
* If you class is going to be inside an STL container, then you need

Method | Description
---|---
`Print()` | Summarize object in a one line description of the form: `MyObject { param1 = val, param2 = val,...}` output to input ostream.
`operator<` | This is used to sort the collection before inputting into event bus.

* If your class is going to be outside an STL container (i.e. put into the event bus by itself), then you need

Method | Description
---|---
`Print()` | Summarize object in a one line description of the form: `MyObject { param1 = val, param2 = val,...}` output to input ostream.
`Clear()` | Resets object to default-constructed state.


These should be the minimum requirements that allow you to `add` and `get` your class to/from the event bus.
