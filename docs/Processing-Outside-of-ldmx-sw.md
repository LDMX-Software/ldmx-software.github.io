There is [a repository](https://github.com/LDMX-Software/ldmx-analysis) that already has implemented a few processors that can be compiled outside of ldmx-sw. This repository is a good place to start. You can try forking it to your own GitHub account and then playing around from there.

The rest of this page details the minimum requirements (that is accomplished by the linked repo) in order to compile EventProcessors outside of ldmx-sw.

---

With some fancy `cmake` nonsense, you can write an `EventProcessor` outside of ldmx-sw. This allows you to compile your processor separately than ldmx-sw which means your compiling time drastically decreases. _Currently, you are only able to use the event objects listed in `Event/EventDef.h` when compiling a processor outside of ldmx-sw._


## Structure Setup

1. Go into the directory that you want your processors to be in. I am going to call this directory `MyAnalyses`.
2. Make two directories: `include` and `src`. These directories will contain the header and implementation files of your `EventProcessor`.
3. Copy over the two `cmake` files at the bottom of this page.
4. In the end, your directory structure should look something like this:
```
MyAnalyses/
- include/
- - MyProcessor.h
- src/
- - CMakeLists.txt
- - MyProcessor.cxx
- CMakeLists.txt
```
## Compiling and Linking to ldmx-sw
With the `cmake` files you copied over earlier, you can link ldmx-sw to `MyProcessor` which allows you to run `MyProcessor` through `ldmx-app`.
1. Make a build directory for `MyAnalyses` and go into it: `mkdir MyAnalyses/build; cd MyAnalyses/build;`
2. Configure your analyses to point to your installation of ldmx-sw: 

`cmake -DLDMX_INSTALL_PREFIX=<path-to-your-ldmx-sw-install> -DCMAKE_INSTALL_PREFIX=../install/ ../`

3. Build and install your analyses library: `make install`

## Running `MyProcessor`
Now your processor should be compiled and linked to ldmx-sw. This is great! But when running, `ldmx-app` still need to know about your new processor. This means you need to add your library to the list of libraries that `ldmx-app` will load. Since your library is outside of the install path of `ldmx-sw`, you will need to give the full path to your library of analyses. In your python configuration file (`p` is the ldmx Process that you defined earlier in the file):
```python
p.libraries.append( "<path-to-MyAnalyses>/MyAnalyses/install/bin/libAnalysis.so" )
```
This step _should_ be all you need to run `MyProcessor` like any other processor that is inside ldmx-sw.

---

`MyAnalyses/CMakeLists.txt`:
```cmake
# Minimum CMake version
cmake_minimum_required(VERSION 3.1 FATAL_ERROR)

# Project name
project(ldmx-analysis LANGUAGES CXX)

# Set the CXX standard 
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Setup the LDMX INSTALL location
if(LDMX_INSTALL_PREFIX)
    set(LDMXSW_INCLUDE_DIR "${LDMX_INSTALL_PREFIX}/include")
    set(FRAMEWORK_LIBRARY "${LDMX_INSTALL_PREFIX}/lib/libFramework.so")
    set(EVENT_LIBRARY "${LDMX_INSTALL_PREFIX}/lib/libEvent.so")
    include_directories(${LDMXSW_INCLUDE_DIR})
    message( STATUS "ldmx-sw found at ${LDMX_INSTALL_PREFIX}" )
endif()

# Get root and add it as an include
find_package(ROOT REQUIRED COMPONENTS Core RIO PyROOT)
include(${ROOT_USE_FILE})
message( STATUS "ROOT found at: ${ROOT_DIR}" )

# Install configuration scripts - switching out cmake parameters
file(GLOB config_scripts ${CMAKE_CURRENT_SOURCE_DIR}/config/*)
foreach(config_script ${config_scripts})
    get_filename_component(config_script_output ${config_script} NAME)
    configure_file(${config_script} ${CMAKE_CURRENT_BINARY_DIR}/${config_script_output})
    install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${config_script_output} DESTINATION bin PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
endforeach()

# Define the headers
include_directories(include)

# Define the sources 
add_subdirectory(src)
```
`MyAnalyses/src/CMakeLists.txt`:
```cmake
file(GLOB ANALYSES
    "*.cxx"
    )

add_library(Analysis SHARED ${ANALYSES})
target_link_libraries(Analysis ${FRAMEWORK_LIBRARY} ${EVENT_LIBRARY})

install(TARGETS Analysis DESTINATION ${CMAKE_INSTALL_PREFIX}/lib)
```