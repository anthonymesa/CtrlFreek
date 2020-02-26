# CtrlFreek

CtrlFreek is a script I made with python to automate the process of compiling Java and C++ source code in the command line because I do not want to use any IDE's for the time being if I can help it. Taking this approach has given me better insight into the step-by-step process of Java and C++ compilation (as well as beginner Python development).

=========================================================================

Out of the box, CtrlFreek works with a specific base file structure as outlined below:

```
JAVA_PROJECT_FOLDER/
├─── lib (All of your downloaded .jar libraries)
├─── src (All of your project source files)
├─── res (All of your project resources)
└─── out (The final destination folder )
```

```
C++_PROJECT_FOLDER/
├─── lib (All of your included libraries)
├─── src (All of your project source files)
├─── res (All of your project resources)
├─── bin (The compiling destination folder)
├─── build (The linking destination folder)
└─── CMakeLists.txt
```

As you can see compiling C++ uses CMake in this case so...

## Dependencies

I have not added multiple compiler options or anything like that so to use CtrlFreek out of the box without any issues you will need:

Installed:
- Python3
- Visual Studio 16 2019 or Xcode
- CMake 3.16.0-rc2-win64-x64
- Java Development Kit

To use different compilers or different versions of the software listed, you must edit the calls to CMake in the script:
```
# Call CMAKE for visual studio to generate BIN
call([path + "/Compiling_Tools/winCompile/cmake-3.16.0-rc2-win64-x64/bin/cmake.exe", "-B", "bin/win", "-G", "Visual Studio 16 2019"], cwd=project_location)
print("\n\n\tCMAKE COMPILE CALL COMPLETE\n\n")

# Call CMAKE for visual studio to generate BUILD
call([path + "/Compiling_Tools/winCompile/cmake-3.16.0-rc2-win64-x64/bin/cmake.exe", "--build", "bin/win", "--config", "Release"], cwd=project_location)
print("\n\n\tCMAKE BUILD CALL COMPLETE\n\n")
```
YOU WILL NEED TO EDIT THIS AT LEAST ONCE TO POINT TO YOUR CMAKE INSTALLATION (I may include automatic detection in the future).

You will also need to edit the compilers for the CMakeLists variable in the script (for generating new projects).

## Execution

When you run the script you are prompted with:
```
===========================================================================
|   CTRLFREEK   |             x | j | r | c | n | d | help                |
===========================================================================
```
The commands are as follows:
```
Options:

    x   Exit Program
    j   Compile Java to class
    r   Compile Java to .Jar
    c   Compile Cpp project
    d   Set current project directory

    n[j or c]   Create new project for Java or Cpp
```

To compile, type your indicator and just hit enter, and hope that you have no compilation errors. :")

Currently, the jar option will only successfully create an executable jar if your libraries or dependencies do not require any native C code (such as any code that would be used with Java Native Interface).

## Plans for the future:
* Add Native C code inclusion into executable jar
* Test and update as requred for compiling and archiving larger and more complicated projects
* Add Java Package directory defaults
* Add automatic CMake detection
