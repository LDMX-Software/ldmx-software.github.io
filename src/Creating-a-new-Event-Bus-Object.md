# Creating a New Event Bus Object

If the objects already in an Event module do not suit your purposes, you can define your own Event Bus Object that will carry your data between processors. You will need to meet a few requirements in order for your class to be able to be added to the event bus.

* Write the class header and implementation files like normal. Let's say the name of your class is `ClassName`.
* In the header file, include `ClassDef( ClassName , 1 );` at the bottom of your class declaration (right before the closing bracket `};`).
* At the top of the implementation file, include `ClassImp( ClassName );` right after the include statement.
* Your class shouldn't use `TRef` (or any derived class)
* Your object needs to be "registered" with the software so that ROOT can put it in our event model dictionary. This is done by adding a line to the `CMakeLists.txt` file in the module you are putting the new object. For example, the `Recon` module has an object shared by Hcal and Ecal in it. This object is not put inside a collection, so no other parameters are needed.

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

Note: ROOT has a weird way of keeping track of class "versions" so if you change your class, you may need to increment the number in the ClassDef command by one in order to force ROOT to recognize the newer "version" of your class. You can reset this incrementation by deleting the ldmx install and build and recompiling from scratch.

### Clean Environment
If you are adding a new object after already developing with ldmx-sw, you will need to remove some auto-generated files so that the cmake system can "detect" your new event bus object. The easiest way to do this is to delete your build directory and then go into the Framework module and use `git` to clean it:
```
cd Framework
git clean -xxfd
```
