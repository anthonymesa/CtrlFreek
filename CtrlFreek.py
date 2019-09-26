#
# CtrlFreek.py is a script that allows me to control EXACTLY how my programs
# are compiled. Essentially, all it does is automate the command line with
# arguments based on the local file structure
#
# CtrlFreek - 0.1.2
# Anthony Mesa
# 

from subprocess import call
from os import remove
from os import rmdir
from shutil import rmtree
from os import mkdir
from os.path import exists
import time
import platform
import glob

# Name of the main class file for the application
applicationName = "Application"
MANIFEST_NAME = "Manifest.txt"

libFolder = "lib/*.jar"
librariesList = glob.glob(libFolder)

srcFolder = "src/*.java"
sourcesList = glob.glob(srcFolder)

destinationFolder = "out/"

choice = ""
compileSourcesList = []
compileLibrariesList = []
runningLibrariesList = []
manifestLibList = []
manifestFolders = []

def appBegin():

    # 'appBegin()' begins the script, prompting the user, and then setting values
    # based off of the folders assigned above, then it prints those lists.

    a = """
    \n\n
    _______ _______  ______        _______  ______ _______ _______ _     _
    |          |    |_____/ |      |______ |_____/ |______ |______ |____/ 
    |_____     |    |    \_ |_____ |       |    \_ |______ |______ |    \_
    """
    
    print(a)
    
    # Asks user if they would like to compile and run, or compile and create jar.
    global choice
    choice = raw_input("Would you like to run the compiled class, or create a jar (r/j)? ")
    while (choice != "j" and choice != "r"):
        choice = raw_input("Please type r or j:")

    # Determines which osBreak to us ( : vs ; ) based off of current os.
    if platform.system() == "Windows":
        print "\n", "Formatting for Windows OS", "\n"
        osBreak = ";"
    elif platform.system() == "Darwin":
        print "\n", "Formatting for Mac OS", "\n"
        osBreak = ":"
    else:
        print "\n", "Cannont format, Unknown System", "\n"
    
    # Create a string joined by ":" or ";" (based on os) containing all list entries.
    global compileSourcesList
    compileSourcesList = osBreak.join(sourcesList)
    global compileLibrariesList
    compileLibrariesList = osBreak.join(librariesList)
    global runningLibrariesList
    runningLibrariesList = compileLibrariesList + osBreak + "out/bin"
    
    # Prints user feedback to see what libraries are used.
    print "Source Code: ", "\n\n\t", "\n\t".join(sourcesList), "\n"
    print "Compiling Libraries: ", "\n\n\t",  "\n\t".join(librariesList), "\n"
    print "Running Libraries: ", runningLibrariesList, "\n"

def compileSourceCode():

    # Compile removes any previous classes compiled, and then compiles new classes.

    # If the compiled class exists already, delete the entire bin folder.
    print("deleting old bin directory...")
    start_time = time.time()
    if exists("out/bin/" + applicationName + ".class"):
        rmtree("out/bin/")
    print("deleted /bin in %f" % (time.time() - start_time))

    sources = compileSourcesList
    classes = compileLibrariesList

    # Compile the classes
    if not exists("out/bin/"):
        mkdir("out/bin/")
    call(["javac", sources, "-classpath", classes, "-d", destinationFolder + "bin"])

def run():

    # Runs the compiled code
    raw_input("Press enter to run...")
    if exists("out/bin/" + applicationName + ".class"):
        call(["java", "-cp", runningLibrariesList, applicationName])
    else:
        print("\nMain class wasnt compiled, end of script.\n")

def createJar():
    
    raw_input("\nPress enter to begin extracting jars...")
    # Create new folders in 'out' for all of the jars in 'lib'
    for each in librariesList:
        # Take the location of the jar file and reformat it to a single name
        cutoffJar = str(each)[:-4]
        jarName = cutoffJar[4:]
        direction = "out/" + jarName

        # If the out folder for the library already exists, remove it and then unarchive the jar
        if exists(direction):
            rmtree(direction)
            mkdir(direction)
            print("Removing tree..")
            call(["tar", "xf", each, "-C" , direction])
        else:
            mkdir(direction)
            call(["tar", "xf", each, "-C" , direction])
        manifestFolders.append(jarName + "/")
    
    # Creates manifest.txt. If exists, deletes manifest.txt and opens new file
    if exists(MANIFEST_NAME):
        remove(MANIFEST_NAME)
        f = open(MANIFEST_NAME, "wb+")
    else:
        f = open(MANIFEST_NAME, "wb+")

    # Creates list for classpath in manifest file
    manifestLibList = " ".join((manifestFolders))
    # Writes to manifest.txt
    f.write("Main-Class: " + applicationName + "\n")
    # f.write("Class-Path: " + manifestLibList + "\r\n\r\n")
    f.write("Class-Path: " + "bin/ " + manifestLibList + "\r\n\r\n")
    f.flush()
    f.close()
    print("Manifest complete...")

    arguments = "-cvfm"
    jar_file_name = destinationFolder + "/" + applicationName + ".jar"
    manifest_file = MANIFEST_NAME
    entry_point = "bin/" + applicationName
    c_dir = "out/"
    # files = "lib"
    
    call(["jar", arguments, jar_file_name, manifest_file, "-C", c_dir, "."])

def main():
    appBegin()
    compileSourceCode()
    if (choice == "j"):
        createJar()
    else:
        run()

main()
