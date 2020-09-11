# sbgrader
Matthew Dirks

MET CS 521

Final Project

This is a gradebook program to keep track of grades under a standards-based system and generate grade reports with study advice. It contains a collection of useful functions together with a simple interface that highlights a few of those functions.

This program is my final project for Boston University MET CS 521 (Information Structures with Python).

## Standards-Based Grading
Standards-Based Grading (SBG) is a system in which student grades are reported for individual learning targets (LTs) that are aligned with state and national standards. Students receive scores for learning targets on a scale of 1-4 based on tests, quizzes, projects, and other assessments, and they may reassess any learning target to demonstrate mastery. Ideally, student performance on these learning targets is communicated directly to parents in lieu of a letter grade. However, since school districts often require that teachers assign letter grades on an A-F scale, various schemes exist to convert SBG scores to letter grades. The scheme implemented by this program is as follows:
* To earn an A, a student must:
  * Earn 3s and 4s on at least 90% of the LTs
  * Earn 4s on at least 50% of the LTs
  * Have no 0s or 1s
* To earn a B, a student must:
  * Earn 3s and 4s on at least 80% of the LTs
  * Have no 0s or 1s
* To earn a C, a student must earn 3s and 4s on at least 65% of the LTs.
* To earn a D, a student must earn 3s and 4s on at least 50% of the LTs.

This program implements a gradebook for standards-based grading with some basic functionality. It loads a sample class period and allows a user to add new students to the class, add learning targets to the class, and update student scores to reflect recent reassessments. It also allows a user to generate grade reports for each student in a class. These reports show each student’s most recent score on each learning target, prior scores, an overall grade, and advice to the student on how to raise their grade. Finally, the program reads data from and writes data to files so that changes are saved between sessions.

## Running the Demo Interface
In order to demonstrate some features of this program, **run the code contained in sbgrader.py**. This will bring up a text-based interface. A sample gradebook is displayed, having either been read in from a data file or created anew. Overall grades are not displayed; those may be seen in generated grade reports (option 4 in the menu).

## Modules
This program consists of several modules. The main file is sbgrader.py, which runs the demo interface. The other modules, in alphabetical order, are:
* advice. This is a module of functions that generate advice for students based on their scores. This module does not actually perform the analysis; it just generates the strings.
* classperiod_module. This module contains functions dealing with the ClassPeriod class, a class that stores data on both learning targets and students. Think of a ClassPeriod as a page in a gradebook.
* data_for_unit_testing. This module contains data that is used for unit tests in other modules.
* lt_module. This module contains functions dealing with the LearningTarget class
* nitty_gritty_of_grading. This module has functions that convert learning target scores to letter grades and percentage grades.
* sbg_data_methods. This module contains some functions dealing with extracting and interpreting data from data files.
* simple_interface. This module contains all the functions that comprise the demo interface.
* student_module. This module contains functions dealing with the Student data type.

## Data Files
This repository contains some files with sample data.
* The file sample_classperiod.txt is a data file for a ClassPeriod object. It contains a description of the class period and file names of data files for learning target and student data.
* The *.studat files are data files containing student data and scores on assessments
* The file sample_classperiod_lts.ltdat contains some sample learning targets

## Known Issues
* If a learning target description contains a newline character, the LT cannot be correctly saved to or read from a file.
* I started trying to integrade this code with my district's Student Information System, but never completed that chunk of the project.

## References
A useful reference on Standards Based Grading is the book *Classroom Assessment and Grading That Work* by Robert J. Marzano (2006).
A thoughtful reference is the book *Grading for Equity* by Joe Feldman (2018), which argues for an SBG-like system as more equitable than the traditional American grading system.

## Acknowledgements
I would like to thank Ed Orsini for his help, feedback, and encouragement throughout this course.


