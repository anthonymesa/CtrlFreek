# CtrlFreek

CtrlFreek is a script I made with python to automate the process of compiling java source code in the command line because I do not want to use any IDE's for the time being if I can help it. Taking this approach has given me better insight into the step-by-step process of java compiling and archiving.

=========================================================================

Out of the box, CtrlFreek works with a specific file structure as outlined below:

```
PROJECT_FOLDER_NAME/
├───lib
|     ( All of your downloaded .jar libraries )
├───src
|     ( All of your source files )
├───bin
|     ( The .java compiled source code )
└───out
      ( The final destination folder )
```

If you choose to use a seperate file structure, you will need to edit the script itself, by changing the variable paths:

```python
# Name of the main class file for the application
applicationName = "Application"          #<- The name of the main entry-point class
MANIFEST_NAME = "Manifest.txt"           #<- The manifest that is automatically generated and then merged into the MANIFEST.MF

libFolder = "lib/*.jar"                  #<- The folder containing all of your downloaded .jar libraries
librariesList = glob.glob(libFolder)

srcFolder = "src/*.java"                 #<- The folder containing all of your .java source code
sourcesList = glob.glob(srcFolder)

destinationFolder = "out/"               #<- The destination folder that you would like to compile to and create jar in
```

The script should be placed at the root of the project folder. When you run the script you are prompted with:

```
_______ _______  ______        _______  ______ _______ _______ _     _
|          |    |_____/ |      |______ |_____/ |______ |______ |____/ 
|_____     |    |    \_ |_____ |       |    \_ |______ |______ |    \_


Would you like to run the compiled class, or create a jar (r/j)?
```

To compile and run your project, type 'r' and hit enter. To compile your class into a .jar, type 'j' and then enter. Currently, the jar option will only successfully create an executable jar if your libraries or dependencies that do not require any native C code (such as any code that would be used with Java Native Interface).

After that you will be prompted to hit enter once or twice as it runs depending on your choice.

## Plans for the future:
* Add Native C code inclusion into executable jar
* Test and update as requred for compiling and archiving larger and more complicated projects
