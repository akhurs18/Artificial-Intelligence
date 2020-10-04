# Artificial-Intelligence
-------------------------------------------------------------------------------
Name:          Abdul Rehman 
Professor:     David Barbella
Class:         CS365: Artificial Intelligence & Machine Learning
Date:          February 7th, 2020
-------------------------------------------------------------------------------
Description:

This program allows the user to deploy an agent as it explores a text-based
maze. 

The program will first ask for a .txt file, representing a maze. The mazes are
defined with " " and "%" characters representing spaces and walls, respectively.

The program will then prompt the user which search algorithm they would like to
use. Once chosen, the agent (represented by the "P" character) will search the
maze for prizes (represented by the "." character).

Once the agent has collected all the prizes, the program will print the newly
traversed maze with the agent's chosen path (now marked with "#" characters).

The user will then be promted if they would like to try again. They can either
continue traversing mazes, or end the program.
-------------------------------------------------------------------------------
Preliminary Information:

   - Make sure arehman_jwolfe_lab-A.py is in the same folder or directory as
     your maze files. Otherwise, the interface will return an error if you 
     try to type your file name.
  
   - The mazes don't check if the prize is unreachable, so please try and
     avoid those test cases if possible.
-------------------------------------------------------------------------------
Instructions:

   1. Open the terminal.

   2. Make sure you are currently inside the folder.

   3. Start the program by typing: python arehman_jwolfe_lab-A.py

   4. When it asks for your maze file name, type it within quotation
      marks. (Example: "file_name.txt")

   5. When it asks which search algorithm you would like to use, type 
      the corresponding number (no quotes).

   6. The chosen path by the agent, plus the step count and the number of
      expanded nodes, will be printed.
      
   7. The program will then ask if you would like to try again. Type 1 to
      return to the maze prompt, or type 2 to end the program.
-------------------------------------------------------------------------------
Sources Cited:
   - We used StackOverflow to remind ourselves the simple tree traversal algorithm
-------------------------------------------------------------------------------
