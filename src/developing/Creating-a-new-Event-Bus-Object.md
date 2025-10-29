# Creating a New Event Bus Object

If the objects already in an Event module do not suit your purposes, you can define your own Event Bus Object that will carry your data between processors. You will need to meet a few requirements in order for your class to be able to be added to the event bus.

* Write the class header and implementation files like normal. Let's say the name of your class is `ClassName`.
* Your class _needs_ to have a default constructor `ClassName()`. A simple way to do this is to let the compiler define one for you with `ClassName() = default;` in the header.
* In the header file, include `ClassDef( ClassName , 1 );` at the bottom of your class declaration (right before the closing bracket `};`).
* At the top of the implementation file, include `ClassImp( ClassName );` right after the include statement.
* Your class shouldn't use `TRef` (or any derived class)
* Your object needs to be "registered" with the software so that ROOT can put it in our event model dictionary. This is done by adding lines to `LinkDef.h` in the module you are putting the new object. For example, the `Recon` module has an object shared by Hcal and Ecal in it. This object is not put inside a collection, so no other lines are needed.

```cpp
// inside Recon/include/Recon/Event/LinkDef.h
#pragma link C++ class ldmx::HgcrocDigiCollection+;
```

* If you class is going to be inside an STL container, then you need

Method | Description
---|---
`Print()` | Summarize object in a one line description of the form: `MyObject { param1 = val, param2 = val,...}` output to input ostream.
`operator<` | This is used to sort the collection before inputting into event bus.

and you should add the STL container class to the `LinkDef.h` file as well, for example
```cpp
// for a std::vector
#pragma link C++ class std::vector<ClassName>+;
// and/or for a std::map with int keys
#pragma link C++ class std::map<int, ClassName>+;
```

* If your class is going to be outside an STL container (i.e. put into the event bus by itself), then you need

Method | Description
---|---
`Print()` | Summarize object in a one line description of the form: `MyObject { param1 = val, param2 = val,...}` output to input ostream.
`Clear()` | Resets object to default-constructed state.

These should be the minimum requirements that allow you to `add` and `get` your class to/from the event bus.

```admonish note title="Class Versions"
ROOT has a weird way of keeping track of class "versions" so if you change your class, you may need to increment the number in the ClassDef command by one in order to force ROOT to recognize the newer "version" of your class. You can reset this incrementation by deleting the ldmx-sw install and build and recompiling from scratch.

The versions are helpful for longer-term developments when we wish to change something about the class (e.g. add a new member variable)
without breaking the ability of our software to read the old version of the class.
```

### Clean Environment
If you are adding a new object after already developing with ldmx-sw, you will need to remove some auto-generated files so that the cmake system can "detect" your new event bus object. The easiest way to do this is to delete your build directory and then go into the Framework module and use `git` to clean it:
```
cd Framework
git clean -xxfd
```
This last step is only necessary for developments built off of ldmx-sw prior to v3.3.4.

### CMake Registration
If you are developing off of ldmx-sw prior to v4.5.3, then instead of editing the `LinkDef.h` file directly, you would register within the `CMakeLists.txt` file and then some CMake code writes a LinkDef file for you.
This extra indirection did not save much effort and got in the way of developing manual schema evolution, so it was dropped.
