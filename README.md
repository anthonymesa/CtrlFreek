# ControlFreak
ControlFreak is a script I made with python to automate the process of compiling java in the command line because I can't stand how bloated IDE's are.

That said, it only works with a specific file structure:

```bash
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
Just drop this script into PROJECT_FOLDER_NAME and then run it, easy peasy.

So much easier than wondering why eclipse or netbeans is throwing you some fucky error.
