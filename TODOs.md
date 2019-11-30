sbgrader2 next steps:

* **DONE** Figure out how to scrape Synergy (using selenium?)
* **DONE** Interface to create ClassPeriod from a Synergy page.
  * **DONE** Figure out which columns are LTs (probably by "Contains LT" and "does not contain "Overall"; also look at assignment type, which could be "LT" or "Learning Target" or "LearningTarget").
* **DONE** Calculate overall grades and output string
* **DONE** Fill data to Synergy using selenium, both in score boxes and comment fields
* ~~Write previous scores in comment fields~~
* Read and parse previous scores from comments field - parsing done (in stu); need to write method to read from Synergy.
* **DONE** Code a score of -1 as exempt/not calculated (in NGOG)

* Reports:
  * Make reports nice via Markdown or TeX
  * Convert reports to PDF
  * Code to print all the reports
  * Ability to customize boilerplate (so Aaron can use "complete response," for example)
  * Advice content depends on whether D is a valid grade

* login (with district id) for different preferences
  * **DONE** prefs stored in user_prefs.txt
  * ~~if only one user in file, defaults to that profile. (But confirms so that new account could be created if desired. ("Log in as smithj (y/n)?")!!~~
  * **DONE** Choose overall function: simple, piecewise, sticky
  * **DONE** Toggle whether D is a valid grade
  * **DONE** Lines starting with '#' are comments (to explain user_prefs file to anyone who opens it)
  * **DONE** example line: dirksm,function=piecewise,assign_d=False
  * **DONE** If user name not found, ask user if they want new log-in. Ask questions on preferences, and then add to user_prefs.txt
  * Use login to autofill Synergy username field
  * **DONE** toggle train mode (https://wa-bsd405.edupoint.com/train/Login.aspx)
  * **DONE**

* better interface
  * **DONE** PrettyTable display
  * ~~nicer student strings~~ Not really necessary given ClassPeriod string overhaul
  * **DONE** include overall grade in display
  * **DONE** ClassPeriod datafiles each saved to their own subfolder
  * Allow users to fill Synergy data twice without saving in between.
    * (Currently causes ElementClickInterceptedException).
  * Options:
   1. **DONE** Launch browser (TRAIN MODE or LIVE MODE)
   2. **DONE** Update overall grades on Synergy (= download grades, calculate overall, fill)
   3. **DONE** Generate grade reports ( = download grades, generate reports)
   4. **DONE** Change preferences
      + **DONE** Change preferences in place in file, rather than appending to the end.
      + **FIXED** 11/29/19 bug: update_prefs is not correctly adding new users to prefs file.
      + **DONE** Adding user to prefs file should check to make sure user isn't yet present,
    and if user is present, update instead.
      + **DONE** After prefs are updated in the file, reload relevant prefs (i.e. train mode)
   5. **DONE** Exit
  * Should not have to launch new browser for each data import!
  * If user navigates away from page and then comes back, the program crashes. Fix that.
  * **DONE** Big disclaimer that this script could break at any point if Synergy/Gradebook changes

* make repo public (sans bsd-specific stuff)

* Write up an install guide (for .exe or from source)
* package as exe file (use py2exe)

Selenium docs:
https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.remote.webdriver