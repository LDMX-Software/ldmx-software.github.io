# Debugging

CMAKE provides several useful flags for debugging and code analysis. We've included many of these in `just` recipes for convenience.

## Commands to use:

### Static Analysis
  - **`configure-clang-tidy`** - Enables clang-tidy static analysis during compilation to catch potential bugs and style issues before runtime. The CMAKE flag is `-DENABLE_CLANG_TIDY=ON`. This will slow down compilation but provides valuable feedback on code quality.

### Optimization
  - **`configure-clang-lto`** - Switches to the clang/clang++ compiler and enables LTO (Link Time Optimization), which can improve performance by optimizing across compilation units during linking. The flags are `-DENABLE_LTO=ON -DCMAKE_CXX_COMPILER=clang++ -DCMAKE_C_COMPILER=clang`. Note: LTO significantly increases link time but may catch additional optimization-related issues.

### Runtime Sanitizers
  - **`configure-asan-ubsan`** - Enables both ASAN (AddressSanitizer) and UBSAN (UndefinedBehaviorSanitizer) to detect memory errors (buffer overflows, use-after-free, etc.) and undefined behavior at runtime. The flags are `-DENABLE_SANITIZER_UNDEFINED_BEHAVIOR=ON -DENABLE_SANITIZER_ADDRESS=ON`. 
    - **Important:** These sanitizers only detect issues when the problematic code is actually executed.
    - If issues are detected, the program will abort and print detailed diagnostic information.

### Interactive Debugging
  - **`configure-gdb`** - Compiles with debug symbols preserved and optimizations disabled, enabling effective debugging with GDB (GNU Debugger). The flag is `-DCMAKE_BUILD_TYPE=Debug`. This allows you to:
    - Set breakpoints and step through code line-by-line
    - Inspect variable values during execution
    - View readable stack traces
    - Note: Debug builds are significantly slower than release builds due to disabled optimizations.