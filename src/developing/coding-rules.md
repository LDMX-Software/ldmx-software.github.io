# Coding rules for development in ldmx-sw

When developing code in ldmx-sw please follow the following best practises and style rules

## I. Naming conventions
1. Avoid one letter variables, `x`
2. Use `snake_case` for local variables
3. Use `snake_case_` for class member variables
4. Use `UpperCase()` for classes
5. Use `camalCase()` for functions
6. Use `lowercase` for namespaces
7. Run `just format-cpp` so the automated formatting is applied
8. For setters, include the word `set` in the beginning of the function, e.g. `setHitValsX()`
9. Set the value of the setter in the header, i.e. make the relevant quanities class members 
10. Do not use `__` in any c++ variable name

## II. Packaging Rules
1. Put the header files with the extension of `.h` into `Package/include/Package/MyFile.h`
2. Put the c++ file with the extension of `.cxx` into `Package/src/Package/MyFile.cxx`
3. The `test` directory is for unit tests
4. Example configs should be put under `exampleConfigs`
5. All producers should have a configurable pass names, input collection names, and output collection names
    

## III. Code quality
1. Run UBSAN / ASAN to make sure you don’t introduce memory leaks, or undefined behavior: `just configure-asan-ubsan`, then `just build`
2. Run the LTO build: `just configure-clang-lto`, then `just build`
3. Use the default constructor if possible, i.e.  `~MyClass();` should become `virtual ~MyClass() = default;`
4. If you inherit from a class and you overwrite its function, don't forget `override`, e.g. `void configure(framework::config::Parameters&) override;`
5. Do not inline virtual functions
6. Do not let const member functions change the state of the object
7. Keep the ordering of methods in the header ﬁle and in the source ﬁle identical.
8. Move `cout`-s to the ldmx logging system, see [Logging](developing/Logging.md)
9. Delete commented out code, or move them to `ldmx_log(trace)` if you think it's helpful for a future developer
10. When updating code, be sure to update and revise comments too
11. Set all parameters to be `const` that do not need to be non-const.
12. Use `constexpr` for all constant values that can be evaluated at compile time
13. Do not use magic numbers
