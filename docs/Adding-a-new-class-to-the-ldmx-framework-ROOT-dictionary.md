---
layout: default
---

This is necessary if you want to add your own class to the event bus through a producer. Adding a class to the ROOT dictionary allows for ROOT classes to "know" that it exists and use it similar to other ROOT classes. The ldmx framework assumes that the object you are putting into the event bus is in the ROOT dictionary and is a member of the `EventBusPassenger` variant type.

1. Write the class header and implementation files like normal. Let's say the name of your class is `ClassName`.
2. In the header file, include `ClassDef( ClassName , 1 );` at the bottom of your class declaration (right before the closing bracket `};`).
3. At the top of the implementation file, include `ClassImp( ClassName );` right after the include statement.
4. Put the class header in Event/include/Event/ and the implementation file in Event/src/
5. Add your class name to the EventConstants class. In EventConstants.h, add the line `static const std::string CLASS_NAME;`. In EventConstants.cxx, add the line `const std::string CLASS_NAME = "ldmx::ClassName";`.
6. Add your class to the link definitions file EventLinkDef.h by adding the line `#pragma link C++ class ldmx::ClassName+;`.
7. If you wish to have an STL collection of your new object, add the line (for example) `#pragma link C++ class std::vector<ldmx::ClassName>+;` to the EventLinkDef.h file.
7. Add your class to the event bus file EventDef.h by adding the line `#include "Event/ClassName.h"`.
8. Recompile the whole framework (cmake and make).

Note: ROOT has a weird way of keeping track of class "versions" so if you change your class, you may need to increment the number in the ClassDef command by one in order to force ROOT to recognize the newer "version" of your class. You can reset this incrementation by deleting the ldmx install and build and recompiling from scratch.
