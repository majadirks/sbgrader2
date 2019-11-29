# -*- coding: utf-8 -*-
"""
Main code to run interface for bsd405 users.
This module replaces simple_interface.py.
"""

# import modules
import classperiod_module as cpm
import sbg_data_methods as dm
import lt_module as ltm
import student_module as stu
import nitty_gritty_of_grading as ngog
import sys
import synergy_to_sbg as synergy
import user_prefs_module as upm
from os import path

# Constants
DEFAULT_CP_DESCRIPTION = 'sample_classperiod'
DEFAULT_OVERALL_KEYWORD = 'ignore'


"""
# Delete this
def load_sample_classperiod(description=DEFAULT_CP_DESCRIPTION):
    '''
    This function loads a sample ClassPeriod file whose description
    is given as an argument. It looks for a file with the name
    {description}.txt (e.g. "sample_classperiod.txt")
    If that file does not exist, an empty ClassPeriod is created
    with the given description
    The function returns the resulting ClassPeriod object.
    '''
    filename = path.join('.', description, description + ".txt")
    # Check if file exists.
    data_str = dm.fetch_data_from_file(filename)
    file_exists = bool(data_str)
    # If file exists, try to use it to build a sample.
    if file_exists:
        return cpm.build_classperiod_from_data(data_str)
    else:  # If file does not exist, return empty ClassPeriod
        return cpm.ClassPeriod(DEFAULT_CP_DESCRIPTION)

"""

def get_string_from_input(prompt, illegal_substring=':::'):
    '''
    This function prompts the user for a string. It rejects
    any string containing a specified illegal_substring.
    The function returns the user input.
    '''
    input_str = illegal_substring
    while illegal_substring in input_str:
        input_str = input(prompt)
        if illegal_substring in input_str:
            print(f"Error: illegal substring '{illegal_substring}'")
    return input_str


def get_float_from_input(prompt):
    '''
    This function prompts the user for a float input.
    If the input has zero in its tenths place, it is returned as an int.
    For example, 3.5 is returned as 3.5, but 4.0 is returned as 4.
    '''
    while True:
        input_str = input(prompt)
        try:
            input_float = float(input_str)
            # If input has no tenths place, return it as an int.
            if (input_float * 10) % 10 == 0:
                return int(input_float)
            return input_float
        except ValueError:
            print("Please enter a float")



def generate_reports_interface(cp):
    '''
    This function generates reports for all students in a period.
    It takes one argument, a ClassPeriod object.
    It returns True on success, False otherwise.
    '''
    print("Generating report files.")
    successful = cpm.generate_reports(cp)
    if successful:
        print("Reports generated successfully.")
    else:
        print("An error occurred. Reports did not finish writing.")
    return successful


def import_from_synergy(driver):
    '''
    This function prompts the user to direct a browser to
    a Synergy gradebook page, and then downloads the data.
    It returns a ClassPeriod object that holds the data.
    It takes one argument, driver, a selenium WebDriver object
    '''
    return synergy.create_classperiod_from_synergy(driver)


def write_overall_grades_to_synergy(cp, driver):
    '''
    This function writes the list of overall scores to Synergy.
    It returns True on success, False on failure.
    It takes two arguments:
        (i) a ClassPeriod object
        (ii) driver, a selenium WebDriver object
                pointed at a Synergy gradebook page.
    '''
    grades = cp.get_list_of_overall_grades()
    return synergy.fill_overall_scores(driver,
                                       grades,
                                       comments=[],
                                       keyword=DEFAULT_OVERALL_KEYWORD)


def save_and_exit(cp):
    '''
    This function saves a given classperiod to a file
    and then halts execution.

    This function is almost exactly equivalent to
    cpm.write_classperiod_to_datafile()
    except that it also halts program execution after writing to the file.
    '''
    cpm.write_classperiod_to_datafile(cp)
    sys.exit()


def main_menu(cp, train_mode=True):
    '''
    This function displays the str representation of a given ClassPeriod
    object and prompts the user to take an action.
    Arguments:
        (i) cp, a ClassPerid object,
        (ii) train_mode, a boolean indicating whether the online
            gradebook should launch in training mode
    '''
    browser = False  # Initialize browser variable.
    browser_launched = False
    data_downloaded = False
    exit_choice = 5
    choice = -1
    while choice != exit_choice:


        # Is browser still open?
        try:
            # Try to do something with the browser.
            # If it works, the browser must be open!
            # If it fails, the browser isn't open.
            # Ironclad logic.
            browser.window_handles
            browser_launched = True
        except:
            browser_launched = False



        print("\n=== SBGRADER ===")
        print(cp)
        print("\n")
        print("=== OPTIONS ===")
        print("1. Launch Browser" + (" in test mode" * train_mode))
        print("2. Update preferences")
        print("3. Calculate/Fill Overall Grades" * browser_launched)
        print("4. Generate grade reports" * browser_launched)
        print("5. Exit")
        choice_str = ""
        while True:
            choice_str = input("> ")
            try:
                choice = int(choice_str)
                if choice < 1 or choice > exit_choice:
                    print("Invalid Selection.")
                else:
                    break
            except ValueError:
                print("Invalid selection")
        # Call the function corresponding to the user's choice
        if choice == 1:
            if train_mode:
                synergy_url = synergy.SYNERGY_TRAIN_MODE_URL
            else:
                synergy_url = synergy.SYNERGY_URL
            browser = synergy.initialize_driver_with_user_input(synergy_url)
            # If user cancelled browser by entering 0,
            # the following conditional does not run.
            if bool(browser):
                cp = synergy.create_classperiod_from_synergy(browser)
                browser_launched = True
        if choice == 2:
            # TODO
            pass
        if choice == 3 and browser_launched:
            # Download data
            cp = synergy.create_classperiod_from_synergy(browser)
            # Calculate and fill scores
            write_overall_grades_to_synergy(cp, browser)
        if choice == 4 and browser_launched:
            cp = synergy.create_classperiod_from_synergy(browser)
            generate_reports_interface(cp)


def show_disclaimer():
    '''
    This function displays a disclaimer on the screen
    and pauses for user acknowledgement.
    '''
    disclaimer = ("Notice:\n\nsbgrader is not officially condoned or " +
                  "supported by the Bellevue School District.\n" +
                  "It is designed for use " +
                  "with Synergy Education Platform, " +
                  "and was written during the " +
                  "2019-2020 school year.\n" +
                  "If Synergy is replaced by a new " +
                  "gradebook program or is " +
                  "significantly updated, this script " +
                  "may stop working, and might not be updated.\n" +
                  "Please forward any questions, comments, or concerns to " +
                  "Matthew Dirks.\n\n")
    print(disclaimer)
    input("Press Enter to acknowledge >")


# Main code: run an interface.
if __name__ == "__main__":
    show_disclaimer()  # Disclaimer that bsd does not support this script
    # Prompt for login.
    # Look for user's preferences in 'user_prefs.txt'
    # Store prefs as dict.
    prefs_dict = upm.login_prompt('user_prefs.txt')
    train_mode = prefs_dict['TRAIN_MODE']
    empty_class = cpm.ClassPeriod('No Class Loaded')
    main_menu(empty_class, train_mode)
