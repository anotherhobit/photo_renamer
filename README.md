# photo_renamer
This is a simple python tool that renames photos in selected directory.

The photos inside the directory must start with prefix "DSC". I use it to rename all such a files so they have unique names. This tool adds a prefix to the original names that consists of the last date of modification of the original file. 
I found it very useful when I work with my Nikon camera, because it always names the photos I take as DSC_number, where number starts at 1 and ends at 9999 and then it resets to one. 

# Dependencies

You need to install click in order to use this tool

# Usage

Simply run the tool with python in terminal or as a normal shell script and it prompts you for the folder that contains all photos that you wish to rename.
