Sbgrader next steps:

* Figure out how to scrape Synergy (using selenium?)
* Interface to create ClassPeriod from a Synergy page.
  * Figure out which columns are LTs (probably by "Contains LT" and "does not contain "Overall"; also look at assignment type, which could be "LT" or "Learning Target" or "LearningTarget").
* Calculate overall grades and output string
* Fill to Synergy using Selenium, including previous scores in comments field
* Read previous scores from comments field
* Code a score of -1 as exempt/not calculated (in NGOG) **DONE!**

* Make reports nice via Markdown

* login (with district id) for different preferences
  * prefs stored in user_prefs.txt
  * if only one user in file, defaults to that profile. (But confirms so that new account could be created if desired. ("Log in as dirksm (y/n)?")
  * Choose overall function: simple, piecewise, sticky
  * Toggle whether D is a valid grade
  * Lines starting with '#' are comments (to explain user_prefs file to anyone who opens it)
  * example line: dirksm,function=piecewise,assign_d=False
  * If user name not found, ask user if they want new log-in. Ask questions on preferences, and then add to user_prefs.txt
  * Use login to autofill Synergy username field

* better interface
  * PrettyTable display
  * nicer student strings
  * include overall grade in display
  * ClassPeriod datafiles each saved to their own subfolder
  * Options: import from Synergy, generate reports, save local copy, export to Synergy, etc.

* make public repo after deleting senstiive data

* Write up install guide
* package as exe file (use py2exe)
