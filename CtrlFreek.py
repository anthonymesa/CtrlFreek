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

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import*
from subprocess import call
from subprocess import Popen
import subprocess as sub
from os import remove
from os import rmdir
from shutil import rmtree
from os import mkdir
from os.path import exists
import time
import platform
import glob

# Set variables for Java run/compile
applicationName = "Application"
MANIFEST_NAME = "Manifest.txt"
destinationFolder = "build/"

compileSourcesList = []
compileLibrariesList = []
runningLibrariesList = []
manifestLibList = []
manifestFolders = []
librariesList = []
sourcesList = []

output = ""
projectLocation = ""

# Initialize tKinter
root = tk.Tk()

def toConsole(input):
    process = Popen(input, stdout=sub.PIPE, stderr=sub.PIPE, shell=True, universal_newlines=True, cwd=projectLocation)
    output = process.communicate()
    console.insert(END, output[0])
    console.insert(END, output)

def appBegin():

    """
    Sets up variables before Java compiling begins
     
    Keyword Arguments:
    projectLocation -- String containing the desired project working directory
    """

    # Sets variable representing folder of libraries we want to glob
    libFolder = projectLocation + "/lib/*.jar"
    global librariesList
    librariesList = glob.glob(libFolder)

    # Sets variable representing folder of source code we want to glob
    srcFolder = projectLocation + "/src/*.java"
    global sourcesList 
    sourcesList = glob.glob(srcFolder)

    # Depending on the OS, seperate list of bin's with : or ;
    if platform.system() == "Windows":
        print("\n Formatting for Windows OS \n")
        osBreak = ";"
    elif platform.system() == "Darwin":
        print("\n Formatting for Mac OS \n")
        osBreak = ":"
    else:
        print("\n Cannont format, Unknown System \n")
    
    # Create source list and library lists
    global compileSourcesList
    compileSourcesList = osBreak.join(sourcesList)
    global compileLibrariesList
    compileLibrariesList = osBreak.join(librariesList)
    global runningLibrariesList
    runningLibrariesList = compileLibrariesList + osBreak + projectLocation + "/bin"
    
    toConsole("echo '\nSource Code:'")
    for each in sourcesList:
        toConsole("echo '\n\t'" + each)

    for each in librariesList:
        toConsole("echo '\n\t'" + each)

    toConsole("echo '\nRunning Libraries:\n\n'" + runningLibrariesList + "\n")

def compileSourceCode():
    
    """
    Compile Java source code by calling Javac
     
    Keyword Arguments:
    projectLocation -- String containing the desired project working directory
    """

    # If bin directory from prior compile exists, delete
    toConsole("echo '\nDeleting old bin directory...'")

    start_time = time.time()
    if exists(projectLocation + "/bin/" + applicationName + ".class"):
        rmtree(projectLocation + "/bin/")
    runTime = time.time() - start_time

    toConsole("echo '\nDeleted bin in '" + str(runTime) + " seconds")

    # Sets sources and classes (for readability's sake)
    sources = compileSourcesList
    print(sources)
    classes = compileLibrariesList

    # Creates bin folder if there is none and calls javac
    if not exists(projectLocation + "/bin/"):
        mkdir(projectLocation + "/bin/")
    toConsole("javac " + sources + " -classpath " + classes + " -d bin/")
    #print("javac " + sources + " -classpath " + classes + " -d bin/")
    #call(["javac", sources, "-classpath", classes, "-d", "/bin/"], cwd=projectLocation, shell=True)
    
def run():
    
    """
    Run previously compiled Java program by calling command of same name
     
    Keyword Arguments:
    projectLocation -- String containing the desired project working directory
    """

    # If the main class exists, run the Java class
    # input("Press enter to run...")
    print(projectLocation + "/bin/" + applicationName + ".class")
    if exists(projectLocation + "/bin/" + applicationName + ".class"):
        call(["java", "-cp", runningLibrariesList, applicationName], cwd=projectLocation)
    else:
        print("\nMain class wasnt compiled, end of script.\n")

def createJar():

    """
    Create Java Executable JAR

    WILL NOT INCLUDE EXTERNAL C DEPENDENCIES SUCH AS JAVA NATIVE LIBRARY CODE
     
    Keyword Arguments:
    projectLocation -- String containing the desired project working directory
    """

    input("\nPress enter to begin extracting jars...")

    # Takes all libraries and 
    for each in librariesList:
        cutoffJar = str(each)[:-4]
        jarName = cutoffJar[4:]
        direction = "out/" + jarName

        if exists(direction):
            rmtree(direction)
            mkdir(direction)
            print("Removing tree..")
            call(["tar", "xf", each, "-C" , direction], cwd=projectLocation)
        else:
            mkdir(direction)
            call(["tar", "xf", each, "-C" , direction], cwd=projectLocation)
        
        # Add the libraries inside of the Executable JAR
        manifestFolders.append(jarName + "/")
    
    # Checks if Manifest file exists, deletes it and creates a new one
    if exists(MANIFEST_NAME):
        remove(MANIFEST_NAME)
        f = open(MANIFEST_NAME, "wb+")
    else:
        f = open(MANIFEST_NAME, "wb+")

    # Generates info for Manifest file
    manifestLibList = " ".join((manifestFolders))
    f.write("Main-Class: " + applicationName + "\n")
    f.write("Class-Path: " + "bin/ " + manifestLibList + "\r\n\r\n")
    f.flush()
    f.close()
    print("Manifest complete...")

    arguments = "-cvfm"
    jar_file_name = destinationFolder + "/" + applicationName + ".jar"
    manifest_file = MANIFEST_NAME
    c_dir = "out/"
    # entry_point = "bin/" + applicationName
    
    # Runs JAR command to archive project using arguments set above
    call(["jar", arguments, jar_file_name, manifest_file, "-C", c_dir, "."], cwd=projectLocation)

def compileCpp():

    """
    Compiles C++ code by running CMake
     
    Keyword Arguments:
    projectLocation -- String containing the desired project working directory
    """

    # Chooses appropriate operating system
    if platform.system() == "Windows":
        
        # If folders exist from previous build, delete
        if exists(projectLocation + "/build/win/"):
            print("Deleting Windows Build Folder...")
            rmtree(projectLocation + "/build/win/")
        if exists(projectLocation + "/bin/win/"):
            print("Deleting Windows Bin Folder...")
            rmtree(projectLocation + "/bin/win/")

        # call CMake
        call(["D:/compile/winCompile/cmake-3.16.0-rc2-win64-x64/bin/cmake.exe", "-B", "bin/win", "-G", "Visual Studio 16 2019"], cwd=projectLocation)
        print("\n\n\tCMAKE COMPILE CALL COMPLETE\n\n")
        call(["D:/compile/winCompile/cmake-3.16.0-rc2-win64-x64/bin/cmake.exe", "--build", "bin/win", "--config", "Release"], cwd=projectLocation)
        print("\n\n\tCMAKE BUILD CALL COMPLETE\n\n")

    elif platform.system() == "Darwin":

        # If folders exist from previous build, delete
        if exists(projectLocation + "/build/mac"):
            print("Deleting Mac Build Folder...")
            rmtree(projectLocation + "/build/mac")
        if exists(projectLocation + "/bin/mac"):
            print("Deleting Mac Bin Folder...")
            rmtree(projectLocation + "/bin/mac")

        call(["cmake -B bin/mac -G Xcode"], cwd=projectLocation, shell=True)
        print("\n\n\tCMAKE COMPILE CALL COMPLETE\n\n")
        call(["cmake --build bin/mac --config Release"], cwd=projectLocation, shell=True)
        print("\n\n\tCMAKE BUILD CALL COMPLETE\n\n")

    else:
        print("\n", "Cannont format, Unknown System", "\n")

def compile():
    
    """
    Compiles C++ code by running CMake
     
    Keyword Arguments:
    projectLocation -- String containing the desired project working directory
    """
    
    if projectLocation == "":
        process = Popen("echo 'Choose a working directory'", stdout=sub.PIPE, shell=True, universal_newlines=True)
        output = process.communicate()
        console.insert(END, output[0])

    # If user has chosen run Java, compile and run
    if v.get() == 1:
        appBegin()
        compileSourceCode()
        #run()

    # if user has chosen archive Java, compile and archive
    elif v.get() == 2:
        appBegin()
        compileSourceCode()
        createJar()

    # if user has chosen compile C++, compile and build
    elif v.get() == 3:
        compileCpp()

    else:
        toConsole("echo 'No choice made'")

#==================================================================================

"""
Where the program begins, Draws the tKinter window
"""

def askForDirectory():

    """
    When directory button is pressed, prompts user for directory
    """
    newDirectory.set(filedialog.askdirectory())
    global projectLocation
    projectLocation = newDirectory.get()

a = """
_______ _______  ______        _______  ______ _______ _______ _     _
|          |    |_____/ |      |______ |_____/ |______ |______ |____/ 
|_____     |    |    \_ |_____ |       |    \_ |______ |______ |    \_
"""
a = a.strip()
v = tk.IntVar()
style = ttk.Style()
style.theme_use('classic')

root.resizable(False, False)

style.configure("Fixed.TLabel", font='TkFixedFont')
headerLabel = ttk.Label(root, text=a, justify = tk.CENTER, style="Fixed.TLabel")
headerLabel.configure(background='#1f1f1f', foreground='#e96d5d', anchor="center")
headerLabel.grid(row=0, sticky=W+E+N+S, ipady=40, ipadx=40, pady=(0, 10))

newDirectory = tk.StringVar()
newDirectory.set("Select Project Folder")

directoryFrame = Frame(root)

directoryButton = tk.Button(directoryFrame, text="...", justify = tk.CENTER, command= lambda: askForDirectory())
directoryButton.configure(highlightbackground='#2b2b2b', anchor='center')
directoryButton.grid(row=0, column=0)

directoryLabel = ttk.Label(directoryFrame, textvariable=newDirectory, justify = tk.LEFT, style="Fixed.TLabel")
directoryLabel.configure(background='white', foreground='#2b2b2b', width=70)
directoryLabel.grid(row=0, column=1, sticky=W+E+N+S, pady=0)

directoryFrame.configure(background='#2b2b2b')
directoryFrame.grid(row=1, columnspan=4, sticky=W+E+N+S, padx=20, pady=(0, 10))

compileOptions = Frame(root)

radio1 = tk.Radiobutton(compileOptions, text="Java run", variable=v, value=1)
radio1.config(background='#2b2b2b', fg='white', anchor='w')
radio1.grid(row=0, column=0)

radio2 = tk.Radiobutton(compileOptions, text="Java .jar", variable=v, value=2)
radio2.config(background='#2b2b2b', fg='white', anchor='w')
radio2.grid(row=0, column=1)

radio3 = tk.Radiobutton(compileOptions, text="C++", variable=v, value=3)
radio3.config(background='#2b2b2b', fg='white', anchor='w')
radio3.grid(row=0, column=2)

if platform.system() == "Windows":
    compileButton = tk.Button(compileOptions, text="CONTROL", justify = tk.CENTER, command= lambda: compile())
    compileButton.configure(background="#e96d5d")
    compileButton.grid(row=0, column=3, sticky=W+E+N+S)

if platform.system() == "Darwin":
    compileButton = tk.Button(compileOptions, text="CONTROL", justify = tk.CENTER, command= lambda: compile())
    compileButton.configure(highlightbackground="#e96d5d", fg="Black", highlightthickness=30)
    compileButton.grid(row=0, column=3, sticky=W+E+N+S)

compileOptions.configure(background='#2b2b2b')
compileOptions.grid(row=2, sticky=W+E+N+S, padx=20, pady=(0, 10))

compileOptions.columnconfigure(3, weight=1)

console = tk.Text(font=('TkFixedFont', 12))
console.grid(row=4, sticky=W+E+N+S)

root.configure(background='#2b2b2b')

# tKinter UI loop
root.mainloop()

