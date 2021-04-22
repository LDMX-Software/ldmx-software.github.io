---
layout: default
---

If the objects already in an Event module do not suit your purposes, you can define your own Event Bus Object that will carry your data between processors. You will need to meet a few requirements in order for your class to be able to be added to the event bus.

* Your class shouldn't use `TRef` (or any derived class)
* Your object needs to be "registered" with the software so that ROOT can put it in our event model dictionary. This is done by adding a line to the `CMakeLists.txt` file in the module you are putting the new object. For example, the `Recon` module has an object shared by Hcal and Ecal in it.

```
  register_event_object( module_path "Recon/Event" namespace "ldmx" 
                         class "HgcrocDigiCollection" )
```

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
