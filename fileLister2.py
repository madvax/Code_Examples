#!/usr/bin/env python

# When given a folder name, print list of files names in the folder sorted by size

import sys
import os
import subprocess # used for operating system call Popen 
import operator   # Used to sort the files by size 

# === DICTIONARY ==============================================================
# TODO: Branch on OS for list_command and file_size_index
VERSION           = "2.0.0"     # Version of the agent
DEBUG             = False       # Flag for debug operation
VERBOSE           = False       # Flag for verbose operation 
FIRST             = 0           # first element in a list 
LAST              = -1          # last element in a list
list_command      = "ls -al %s" # OS Command to list the files 
files_of_interest = {}          # Dictionay of file names nad sizes 
file_size_index   = 4           # The index for the file sizes form ls -al

# === MAIN ====================================================================
if __name__ == "__main__":

   # STEP 1: Get a folder from the user
   # TODO: Change this to a command line argument implementation  
   folder = raw_input("Please enter a folder: ")

   # STEP 2: Verify that the folder provided existis on the current file system
   try:
       assert os.path.isdir(folder)
   except Exception as e:
       sys.stderr.write("ERROR -- The folder you provided is not a valid folder on this file system.\n")
       sys.stderr.write("         %s\n" %str(e))
       sys.exit(1)

   # STEP 3: Get the file names and file sizes from the operating system 
   results = subprocess.Popen(list_command % folder    , 
                              stdout = subprocess.PIPE , 
                              stderr = subprocess.PIPE ,
                              shell  = True            )      
   STD_output, STD_error = results.communicate() 
   if DEBUG: 
      print "DEBUG: RESULTS OF RUNNING THE FILE LIST COMMAND:\n" 
      print STD_output
      print STD_error

   # STEP 4: Filter the results to get only the file names and file sizes
   #         Omit sub folders, smbolic links, processes, devices, ..., etc.   
   folderList = STD_output.split(os.linesep)
   if DEBUG: print "DEBUG: LINES OF OUTPUT AS LIST:\n%s" %folderList
   for line in folderList: 
      if len(line) > 0:
         if line[FIRST] == '-':
            files_of_interest[line.split()[LAST]] = int(line.split()[file_size_index])
   if DEBUG: print "DEBUG: DICTIONAY OF FILES:\n%s" % str(files_of_interest)
         
   # STEP 5: Sort the files by size
   sortedFiles = sorted(files_of_interest.items(), key=operator.itemgetter(1))
   if DEBUG: print "DEBUG: SORTED FILES TUPLE:\n%s" %str(sortedFiles)

   # STEP 6: Print the results: File name(Left justified)   Size(right justified) 
   for fileEntry in sortedFiles:
      # print "%s %7d" %(fileName, sortedFiles[fileName])
      print "%-27s %7d" %(fileEntry[FIRST], fileEntry[LAST])

   # STEP 7: Clean Exit 
   sys.exit(0)
