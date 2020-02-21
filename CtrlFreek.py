"""

CtrlFreek.py is a script that allows the user to automate the process of compiling with 100% customization.

If this script is to be used "out of the box" without any editing, it assumes one or two things:

    1. Python 3 or above is installed and being used to run this script
    2. The proper folder structure is being used (for an example of this file structure, refer to the README.MD)
    3. Oracle's JVM and JRM are installed and PATH'd correctly
    4. If it is a Windows system, Visual Studio and its C++ compiling tools are installed and PATH'd correctly
    5. If it is a Mac system, Xcode and its commandlinetools as well as C++ compilling tools are installed and PATH'd correctly
 
 If these are not the case then you will have to edit the script accordingly before running it. (If you break it, not my fault.)

ATTENTION: The call to CMake in compileCpp() points to CMake as it is installed on my USB drive. Change this to point to your
           CMake install path (or just use the command if it is added to your PATH)

I AM NOT RESPONSIBLE FOR ANYTHING YOU CHOOSE TO DO WITH THIS SCRIPT.

CtrlFreek - 0.1.5
Anthony Mesa 

"""

from subprocess import call
from subprocess import Popen
import subprocess as sub
from os import remove
from os import rmdir
from shutil import rmtree
from os import mkdir
from os.path import exists
import os
import time
import platform
import glob

# Set variables for Java run/compile
package_url = "com.bisektor."
application_name = "Application"
mainfest_name = "Manifest.txt"
destination_folder = "build/"
compile_sources_list = []
compile_liraries_list = []
running_libraries_list = []
manifest_lib_list = []
manifest_folders = []
libraries_list = []
sources_list = []
output = ""
project_location = ""
path = os.path.dirname(os.path.abspath(__file__))
current_wd = path
path = path[:2]

def appBegin():

    libFolder = project_location + "/lib/*.jar"
    global libraries_list
    libraries_list = glob.glob(libFolder)

    srcFolder = project_location + "/src/*.java"
    global sources_list 
    sources_list = glob.glob(srcFolder)

    if platform.system() == "Windows":
        print("\n Formatting for Windows OS \n")
        osBreak = ";"
    elif platform.system() == "Darwin":
        print("\n Formatting for Mac OS \n")
        osBreak = ":"
    else:
        print("\n Cannont format, Unknown System \n")
    
    global compile_sources_list
    compile_sources_list = osBreak.join(sources_list)
    global compile_liraries_list
    compile_liraries_list = osBreak.join(libraries_list)
    global running_libraries_list
    running_libraries_list = compile_liraries_list + osBreak + project_location + "/bin"

def compileSourceCode():

    start_time = time.time()
    if exists(project_location + "/bin/" + application_name + ".class"):
        rmtree(project_location + "/bin/")
    runTime = time.time() - start_time

    sources = compile_sources_list
    print(sources)
    classes = compile_liraries_list

    if not exists(project_location + "/bin/"):
        mkdir(project_location + "/bin/")
        call(["javac", sources, "-classpath", classes, "-d", "/bin/"], cwd=project_location, shell=True)
    
def run():

    print(project_location + "/bin/" + application_name + ".class")
    if exists(project_location + "/bin/" + application_name + ".class"):
        call(["java", "-cp", running_libraries_list, application_name], cwd=project_location)
    else:
        print("\nMain class wasnt compiled, end of script.\n")

def createJar():

    input("\nPress enter to begin extracting jars...")

    for each in libraries_list:
        cutoffJar = str(each)[:-4]
        jarName = cutoffJar[4:]
        direction = "out/" + jarName

        if exists(direction):
            rmtree(direction)
            mkdir(direction)
            print("Removing tree..")
            call(["tar", "xf", each, "-C" , direction], cwd=project_location)
        else:
            mkdir(direction)
            call(["tar", "xf", each, "-C" , direction], cwd=project_location)
        
        manifest_folders.append(jarName + "/")
    
    if exists(mainfest_name):
        remove(mainfest_name)
        f = open(mainfest_name, "wb+")
    else:
        f = open(mainfest_name, "wb+")

    manifest_lib_list = " ".join((manifest_folders))
    f.write("Main-Class: " + application_name + "\n")
    f.write("Class-Path: " + "bin/ " + manifest_lib_list + "\r\n\r\n")
    f.flush()
    f.close()
    print("Manifest complete...")

    arguments = "-cvfm"
    jar_file_name = destination_folder + "/" + application_name + ".jar"
    manifest_file = mainfest_name
    c_dir = "out/"
    # entry_point = "bin/" + application_name
    
    call(["jar", arguments, jar_file_name, manifest_file, "-C", c_dir, "."], cwd=project_location)

# Compiles Cpp projects based off of OS
def compileCpp():

    if platform.system() == "Windows":
        
        # Clean prior builds for clean build
        if exists(project_location + "/build/win/"):
            print("Deleting Windows Build Folder...")
            rmtree(project_location + "/build/win/")
        if exists(project_location + "/bin/win/"):
            print("Deleting Windows Bin Folder...")
            rmtree(project_location + "/bin/win/")

        # Call CMAKE for visual studio to generate BIN
        call([path + "/Compiling_Tools/winCompile/cmake-3.16.0-rc2-win64-x64/bin/cmake.exe", "-B", "bin/win", "-G", "Visual Studio 16 2019"], cwd=project_location)
        print("\n\n\tCMAKE COMPILE CALL COMPLETE\n\n")
        # Call CMAKE for visual studio to generate BUILD
        call([path + "/Compiling_Tools/winCompile/cmake-3.16.0-rc2-win64-x64/bin/cmake.exe", "--build", "bin/win", "--config", "Release"], cwd=project_location)
        print("\n\n\tCMAKE BUILD CALL COMPLETE\n\n")

    elif platform.system() == "Darwin":

        # Clean prior builds for clean build
        if exists(project_location + "/build/mac"):
            print("Deleting Mac Build Folder...")
            rmtree(project_location + "/build/mac")
        if exists(project_location + "/bin/mac"):
            print("Deleting Mac Bin Folder...")
            rmtree(project_location + "/bin/mac")

        # Call CMAKE for Xcode to generate BIN
        call(["cmake -B bin/mac -G Xcode"], cwd=project_location, shell=True)
        print("\n\n\tCMAKE COMPILE CALL COMPLETE\n\n")
        # Call CMAKE for Xcode to generate BUILD
        call(["cmake --build bin/mac --config Release"], cwd=project_location, shell=True)
        print("\n\n\tCMAKE BUILD CALL COMPLETE\n\n")

    else:
        print("\n", "Cannont format, Unknown System", "\n")

# Check if the project directory is empty or not set
def CheckDirectory():
    global project_location
    if project_location == "":
        project_location = input("Set project directory: ")
   
# Create Cpp project directory
def CreateCppProject(name):
    new_directory = input("Set project parent: " + path)
    new_project = new_directory + "/" + name
    mkdir(new_project)
    mkdir(new_project + "/bin")
    mkdir(new_project + "/build")
    mkdir(new_project + "/src")
    mkdir(new_project + "/src/header")
    mkdir(new_project + "/res")
    mkdir(new_project + "/lib")
    mkdir(new_project + "/lib/include")
    cmake_lists = open(new_project + "/CMakeLists.txt", "wt+")
    # region CMakeLists.txt
    b = """cmake_minimum_required(VERSION 3.16.0)

# Set application name
set(APPLICATION_NAME "Muser")

# Create project
project(${APPLICATION_NAME})

# Set compiler flags based on OS
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++17 -stdlib=libc++")
endif()
if(CMAKE_CXX_COMPILER_ID MATCHES "MSVC")
	set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /std:c++latest /D_USE_MATH_DEFINES ")
endif()

# Set resource directory
set(RESOURCE_DIRECTORY ${CMAKE_SOURCE_DIR}/res)

# Include library and source header files
include_directories(${CMAKE_SOURCE_DIR}/lib/include)
include_directories(${CMAKE_SOURCE_DIR}/src/header)

# Glob source files into lists
file(GLOB_RECURSE SRC_FILES "${CMAKE_SOURCE_DIR}/src/*.cpp" "${CMAKE_SOURCE_DIR}/src/*.c")
file(GLOB_RECURSE PROJECT_H_FILES "${CMAKE_SOURCE_DIR}/src/*.hpp" "${CMAKE_SOURCE_DIR}/src/*.h")
file(GLOB_RECURSE LIBRARY_H_FILES "${CMAKE_SOURCE_DIR}/lib/*.h")
file(GLOB_RECURSE RESOURCE_FILES "${RESOURCE_DIRECTORY}/*")

# Display all files globbed
message(STATUS "==========================================\\n")
message(STATUS "Source Files === ${SRC_FILES}\\n")
message(STATUS "Project Headers === ${PROJECT_H_FILES}\\n")
message(STATUS "Library Headers === ${LIBRARY_H_FILES}\\n")

# Define a macro to copy all of the files in res directory to new build directory
macro(copy_resources)

    # WINDOWS
    if(WIN32)
        message(STATUS "==========================================================")
        message(STATUS "WIN COPY RESOURCES MACRO > PRINT RESOURCES----------------{")
        message(STATUS "==========================================================\\n")
        message(STATUS "Resource Directory === ${RESOURCE_DIRECTORY}\\n")
        message(STATUS "Resource Files === ${RESOURCE_FILES}\\n")
        message(STATUS "==========================================================")
        message(STATUS "ITERATE RESOURCES-----------------------------------------")
        message(STATUS "==========================================================\\n")

        # For each resource item, add custom command to copy it after building complete
        foreach(ITEM ${RESOURCE_FILES})
            message(STATUS "Item Directory ==== ${ITEM}")
            string(LENGTH ${RESOURCE_DIRECTORY} ITEM_POSITION)
            string(LENGTH ${ITEM} ITEM_LENGTH)
            string(SUBSTRING ${ITEM} ${ITEM_POSITION} -1 TRIMMED_ITEM)
            message(STATUS "Trimmed Item === ${TRIMMED_ITEM}")

            # Add custom command for copy
            add_custom_command(
                TARGET ${APPLICATION_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy
                        ${ITEM}
                        ${EXECUTABLE_OUTPUT_PATH}/Release/${TRIMMED_ITEM}
            )

            message(STATUS "Copied from - ${ITEM}")
            message(STATUS "Copied to - ${EXECUTABLE_OUTPUT_PATH}/Release/${TRIMMED_ITEM}\\n")
        endforeach()
        message(STATUS "==========================================================")
        message(STATUS "END MACRO-------------------------------------------------}")
        message(STATUS "==========================================================\\n")
    endif()

    # MACOS
    if(UNIX)
        message(STATUS "==========================================================")
        message(STATUS "MAC COPY RESOURCES MACRO > PRINT RESOURCES----------------{")
        message(STATUS "==========================================================\\n")
        message(STATUS "Resource Directory === ${RESOURCE_DIRECTORY}\\n")
        message(STATUS "Resource Files === ${RESOURCE_FILES}\\n")

        # Get the index for the last item in RESOURCE_FILES, no matter the length
        list(LENGTH RESOURCE_FILES LAST_INDEX)
        message(STATUS "\\n${LAST_INDEX}\\n")
        math(EXPR LAST_RESOURCE "${LAST_INDEX} - 1")
        list(GET RESOURCE_FILES ${LAST_RESOURCE} LAST_ITEM)

        # Create a string of all resource files called LOCAL_RESOURCES for compilation
        foreach(ITEM ${RESOURCE_FILES})
            message(STATUS "Item Directory ==== ${ITEM}")
            string(LENGTH ${RESOURCE_DIRECTORY} ITEM_POSITION)
            math(EXPR ITEM_POSITION_INDEX "${ITEM_POSITION} + 1")
            string(LENGTH ${ITEM} ITEM_LENGTH)
            string(SUBSTRING ${ITEM} ${ITEM_POSITION} -1 TRIMMED_ITEM)
            message(STATUS "Trimmed Item === ${TRIMMED_ITEM}\\n")

            if(NOT ${ITEM} MATCHES ${LAST_ITEM})
                string(APPEND LOCAL_RESOURCES "res${TRIMMED_ITEM};")
            else()
                string(APPEND LOCAL_RESOURCES "res${TRIMMED_ITEM}")
            endif()
        endforeach()

        message(STATUS "Local Resources === ${LOCAL_RESOURCES}")
        message(STATUS "==========================================================")
        message(STATUS "END MACRO-------------------------------------------------}")
        message(STATUS "==========================================================\\n")
    endif()
endmacro()

# Begin compiling
#=============================

# WINDOWS
if(WIN32)

    set(CMAKE_BINARY_DIR ${CMAKE_SOURCE_DIR}/bin/win)
    set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/build/win)
    set_source_files_properties(${SRC_FILES} PROPERTIES COMPILE_FLAGS /Y-)

    # Create executable
    add_executable(${APPLICATION_NAME} ${SRC_FILES} ${LIBRARY_H_FILES} ${PROJECT_H_FILES})

    # find_package(PackageName)

    # Link any found packages
    # target_link_libraries(${APPLICATION_NAME} ${PACKAGE_NAME_VARIABLE})
    
    # Link any libraries
    # target_link_libraries(${APPLICATION_NAME} ${CMAKE_SOURCE_DIR}/directory_to_library_file)

    # Run macro to copy all resources to newly created resource directory
    copy_resources()

endif()

# MACOS
if(UNIX)
	
    set(CMAKE_BINARY_DIR ${CMAKE_SOURCE_DIR}/bin/mac)
    set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/build/mac)

    # Clear variable
    set(LOCAL_RESOURCES "")

    # Run macro to define string LOCAL_RESOURCES
    copy_resources()
    
    # Evaluate each item's path and assign it to appropriate folder
    foreach(ITEM ${LOCAL_RESOURCES})
        string(FIND ${ITEM} "/data/" FIND_DATA)        
        if(NOT ${FIND_DATA} MATCHES "-1")
            set_property(
                SOURCE ${ITEM}
                PROPERTY MACOSX_PACKAGE_LOCATION "res/data")
        endif()
        string(FIND ${ITEM} "/media/" FIND_MEDIA)
        if(NOT ${FIND_MEDIA} MATCHES "-1")
            set_property(
                SOURCE ${ITEM}
                PROPERTY MACOSX_PACKAGE_LOCATION "res/media")
        endif()
        string(FIND ${ITEM} "/temp/" FIND_MEDIA)
        if(NOT ${FIND_MEDIA} MATCHES "-1")
            set_property(
                SOURCE ${ITEM}
                PROPERTY MACOSX_PACKAGE_LOCATION "res/temp")
        endif()
    endforeach()

    # Create executable
    add_executable(${APPLICATION_NAME} ${SRC_FILES} ${LIBRARY_H_FILES} ${PROJECT_H_FILES} ${LOCAL_RESOURCES})

    # Find frameworks installed on mac
    # find_library({FRAMEWORK_VARIABLE} FrameworkName)

    # Link frameworks 
    # target_link_libraries(${APPLICATION_NAME} ${VARIABLE_FRAMEWORK})

    # Link Libraries
    # target_link_libraries(${APPLICATION_NAME} ${CMAKE_SOURCE_DIR}/directory_to_library_file)

    # Create MACOS app bundle
    set_target_properties(${APPLICATION_NAME} PROPERTIES
        MACOSX_BUNDLE TRUE
        MACOSX_FRAMEWORK_IDENTIFIER com.bisektor.${APPLICATION_NAME}
    )
endif()
    """
    # endregion
    cmake_lists.write(b)
    cmake_lists.close()
    readme = open(new_project + "/README.md", "wt+")
    readme.write(name)
    readme.close()
    main = open(new_project + "/src/Main.cpp", "wt+")
    # region main.cpp
    z = """/*
 *  Project Name 0.0.0
 *
 *  (description)
 *
 *  Creator: Anthony Mesa
 *  Date: (current date)
 *
 */

int main(void)
{

}
    """
    # endregion
    main.write(z)
    main.close()

def CreateJavaProject(name):
    new_directory = input("Set project parent: " + path)
    new_project = new_directory + "/" + name + "/" + package_url
    mkdir(new_project)
    mkdir(new_project + "/res")
    mkdir(new_project + "/lib")
    mkdir(new_project + "/src")
    mkdir(new_project + "/out")

#==================================================================================

while True:

    print("===========================================================================")    
    print("|   CTRLFREEK   |             x | j | r | c | n | d | help                |")   
    print("===========================================================================")    
    
    input_var = input("")
        
    if input_var == 'x':
        break
        
    if input_var == 'd':
        project_location = input("Project Directory: ")
        
    if input_var == 'j':
        CheckDirectory()
        appBegin()
        compileSourceCode()
        run()
    
    if input_var == 'r':
        CheckDirectory()
        appBegin()
        compileSourceCode()
        createJar()
    
    if input_var == 'c':
        CheckDirectory()
        compileCpp()
    
    if input_var == 'nc':
        name = input("Project name: ")
        CreateCppProject(name)

    if input_var == 'nj':
        name = input("Project name: ")
        CreateJavaProject(name)

    if input_var == 'help':
        # region help_string
        a = """
CtrlFreek: Anthony Mesa c2019

Tool that helps to compile both C++ or Java if not using an IDE.

Options:

    x	Exit Program
    j	Compile Java to class
    r	Compile Java to .Jar
    c	Compile Cpp project
    d	Set current project directory
    
    n[j or c]   Create new project for Java or Cpp

Checkout the git: https://github.com/anthonymesa/CtrlFreek.git
        """
        # endregion
        print(a)        
