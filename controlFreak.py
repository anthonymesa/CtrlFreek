#
# ControlFreak.py is a script that allows me to control EXACTLY how my programs
# are compiled. Essentially, all it does is automate the command line with
# arguments based on the local file structure
#
# Control Freak - 0.1.2
# Anthony Mesa
# 

import subprocess
from subprocess import Popen
import os
import time
import platform
import glob
import os.path
import shutil

name = "Application"

MANIFEST_NAME = "Manifest.txt"

libraries = 'lib/*.jar'
libList = glob.glob(libraries)
manifestLibList = " ".join(libList)

source = 'src/*.java'
sourceList = glob.glob(source)

destination = "bin"

#=============================================================
print("------------------------------------------------------")
print("--------------------CONTROL--FREAK--------------------")
print("------------------------------------------------------")
print("")

direction = raw_input("Would you like to run the compiled class, or create a jar (r/j)? ")
while (direction != "j" and direction != "r"):
  direction = raw_input("Please type r or j: ")

# determines which osBreak to us ( : vs ; ) based off of current os
if platform.system() == "Windows":
  print "\n", "Formatting for Windows OS", "\n"
  osBreak = ";"
elif platform.system() == "Darwin":
  print "\n", "Formatting for Mac OS", "\n"
  osBreak = ":"
else:
  print "\n", "Cannont format, Unknown System", "\n"

# join the initial lists into strings, using osBreak
sources = osBreak.join(sourceList)
compileLib = osBreak.join(libList)
runLib = compileLib + osBreak + "bin"

# if the compiled class exists already, remove it to get rid of possible errors
if os.path.exists("bin/" + name + ".class"):
    os.remove("bin/" + name + ".class")

# user feedback to see libraries used
print "source code", sources, "\n"
print "compiling libraries", compileLib, "\n"
print "running libraries", runLib, "\n"

# compile the java classes
subprocess.call(["javac", sources, "-cp", compileLib, "-d", destination])
raw_input("press Enter to finish compiling...")

# create a Manifest.txt to be used in creating the jar if the user selects j
if (direction == "j"):
  if os.path.exists(MANIFEST_NAME):
    os.remove(MANIFEST_NAME)
    f = open(MANIFEST_NAME, "wb+")
  else:
    f = open(MANIFEST_NAME, "wb+")

  f.write("Main-Class: " + name + "\n")
  f.write("Class-Path: " + manifestLibList + "\r\n\r\n")
  f.flush()
  f.close()
  raw_input("Press Enter to finish manifest...")
else:
  pass

# if user selected j, create jar, if not, just run the class
if os.path.exists("bin/" + name + ".class"):
  if (direction == "j"):
    if os.path.exists( destination + "/" + name + ".jar"):
      os.remove( destination + "/" + name + ".jar")
      raw_input("Press Enter to clear old jar...")
      subprocess.call(["jar", "-cvmf", MANIFEST_NAME, destination + "/" + name + ".jar", destination + "/" + name + ".class", "lib"])
    else:
      subprocess.call(["jar", "-cvmf", MANIFEST_NAME, destination + "/" + name + ".jar", destination + "/" + name + ".class", "lib"])
  else:
    subprocess.call(["java", "-cp", runLib, name])
else:
  print("Main class wasn't compiled.")
