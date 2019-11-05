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
  * prefs stored in user_prefs.txt
  * if only one user in file, defaults to that profile. (But confirms so that new account could be created if desired. ("Log in as dirksm (y/n)?")
  * Choose overall function: simple, piecewise, sticky
  * Toggle whether D is a valid grade
  * Lines starting with '#' are comments (to explain user_prefs file to anyone who opens it)
  * example line: dirksm,function=piecewise,assign_d=False
  * If user name not found, ask user if they want new log-in. Ask questions on preferences, and then add to user_prefs.txt
  * Use login to autofill Synergy username field
  * toggle train mode (https://wa-bsd405.edupoint.com/train/Login.aspx)
  * default values

* better interface
  * **DONE** PrettyTable display
  * ~~nicer student strings~~ Not really necessary given ClassPeriod string overhaul
  * **DONE** include overall grade in display
  * **DONE** ClassPeriod datafiles each saved to their own subfolder
  * Allow users to fill Synergy data twice without saving in between.
    * (Currently causes ElementClickInterceptedException).
  * Options: (1) Update overall grades on Synergy
                      (= download grades, calculate overall, fill, and save)
             (2) Generate grade reports ( = download grades, generate reports, close browser)
             (3) Change preferences
             (4) Exit
  * Should not have to launch new browser for each data import!
  * If user navigates away from page and then comes back, the program crashes. Fix that.

* make repo public

* Write up an install guide (for .exe or from source)
* package as exe file (use py2exe)
