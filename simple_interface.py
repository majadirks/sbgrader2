# -*- coding: utf-8 -*-
"""
Matthew Dirks
MET CS 521
Due date: 10/19/2019
Final Project
Description: Functions that comprise a simple user interface
for a few sbgrader functions
"""

# import modules
import classperiod_module as cpm
import sbg_data_methods as dm
import lt_module as ltm
import student_module as stu
import nitty_gritty_of_grading as ngog
import sys
import synergy_to_sbg as synergy

# Constants
DEFAULT_CP_DESCRIPTION = "sample_classperiod"


def load_sample_classperiod(description=DEFAULT_CP_DESCRIPTION):
    '''
    This function loads a sample ClassPeriod file whose description
    is given as an argument. It looks for a file with the name
    {description}.txt (e.g. "sample_classperiod.txt")
    If that file does not exist, an empty ClassPeriod is created
    with the given description
    The function returns the resulting ClassPeriod object.
    '''
    filename = description + ".txt"
    # Check if file exists.
    data_str = dm.fetch_data_from_file(filename)
    file_exists = bool(data_str)
    # If file exists, try to use it to build a sample.
    if file_exists:
        return cpm.build_classperiod_from_data(data_str)
    else:  # If file does not exist, return empty ClassPeriod
        return cpm.ClassPeriod(DEFAULT_CP_DESCRIPTION)


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


def add_lt_interface(cp):
    '''
    This function takes a ClassPeriod object.
    It prompts the user to enter data for a new LearningTarget
    and then adds that LearningTarget to the ClassPeriod's
    LT list and the LT list for each student in the class.
    The function returns the updated ClassPeriod object.
    '''
    # Get LT data from user
    lt_label = get_string_from_input(
            "Label for new Learning Target (e.g. 'LT01') > ", ":::")
    brief = get_string_from_input(
            "Brief description of new Learning Target > ", ":::")
    description = get_string_from_input(
            "Verbose description of new Learning Target > ", ":::")
    new_lt = ltm.LearningTarget(lt_label, brief, description)
    # Add LT to ClassPeriod object
    cp.course_lts.append(new_lt)
    # Add LT to each student
    for student in cp.students_in_period:
        student_score = -1  # invalid score
        while not(ngog.score_is_valid(student_score)):
            student_score = get_float_from_input(
                    f"Enter score for {student.name_str()} > ")
            if ngog.score_is_valid(student_score):
                stu.add_lt(student, lt_label, student_score)
                break
            else:
                print("Error: invalid score entered.")
    return cp


def add_student_interface(cp):
    '''
    This function takes a ClassPeriod object.
    It prompts the user for data on a student and adds the new
    student to the ClassPeriod.
    If there are already learning targets in the class,
    the student is not assigned scores for those LTs. Instead, the student
    starts out scoreless.
    The function returns the updated ClassPeriod.
    '''
    # Get student data from user
    sid_is_unique = False
    while not(sid_is_unique):
        sid = int(get_float_from_input(
                "Unique Student ID number, 0 to cancel > "))
        # If user enters 0, return the unaltered ClassPeriod
        if sid == 0:
            return cp
        # Otherwise, check wither the SID is unique.
        sid_is_unique = not(bool(cp.find_student(sid)))
        if not(sid_is_unique):
            print("Error: student with that ID already exists.")
            print("Try again")
    # Get last name, first name, preferred pronoun
    lastname = get_string_from_input("Student last name > ", ":")
    firstname = get_string_from_input("Student first name > ", ":")
    pronoun = get_string_from_input("Student preferred pronoun > ", ":")
    new_student = stu.Student(sid, lastname, firstname, pronoun)
    cp.students_in_period.append(new_student)
    return cp


def update_score_interface(cp):
    '''
    This function takes a ClassPeriod object.
    It prompts the user for information to update the score
    of a specific student on a specific learning target.
    This function should not be used for editing previous scores,
    but rather for appending new scores based on student reassessments.
    The function returns the updated ClassPeriod.
    '''
    # Prompt user for SID and make sure student is present in ClassPeriod
    student_to_update = False
    while not(student_to_update):
        sid = int(get_float_from_input("Enter SID for student to update > "))
        student_to_update = cp.find_student(sid)
        if not(student_to_update):  # Print error if student does not exist
            print(f"Error: could not find student with SID {sid}")
    print("Student accepted: " + str(student_to_update))
    # Prompt user for LT label and make sure it's already in the ClassPeriod
    lt_exists = False
    while not(lt_exists):
        lt_label = get_string_from_input(
                "Enter LT to update (e.g. 'LT01') > ", ":::")
        lt_exists = cp.has_lt_with_label(lt_label)
        if not(lt_exists):
            print(f"Error: could not find learning target {lt_label}")
    # Prompt user for score and make sure it's valid.
    score_valid = False
    while not(score_valid):
        score = get_float_from_input(f"Student score on {lt_label} > ")
        score_valid = ngog.score_is_valid(score)
        if not(score_valid):
            print(f"Error: invalid score {score}")
    student_to_update = stu.update_grade(student_to_update, lt_label, score)
    return cp


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
    return synergy.fill_overall_scores(driver, grades, 'OVERALL')


def save_and_exit(cp):
    '''
    This function saves a given classperiod to a file
    and then halts execution.

    This function is almost exactly equivalent to
    cpm.write_classperiod_to_datafile()
    with two differences:
        (i) there is no filename argument required or allowed
        (ii) this function halts program execution after writing to the
             file.
    '''
    filename = cp.description + ".txt"
    cpm.write_classperiod_to_datafile(cp, filename)
    sys.exit()


def main_menu(cp):
    '''
    This function displays the str representation of a given ClassPeriod
    object and prompts the user to take an action.
    '''
    browser = False  # Initialize browser variable.
    exit_choice = 7
    choice = -1
    while choice != exit_choice:
        print("\n=== SAMPLE GRADEBOOK ===")
        print(cp)
        print("\n")
        print("=== OPTIONS ===")
        print("1. Add student to class")
        print("2. Add learning target to class")
        print("3. Update a student score")
        print("4. Generate grade reports")
        print("5. Import data from Synergy")
        print("6. Write overall grades to Synergy")
        print(f"{exit_choice}. Save and exit")
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
        # Call the function corresponding to the user's coice
        if choice == 1:
            cp = add_student_interface(cp)
        elif choice == 2:
            cp = add_lt_interface(cp)
        elif choice == 3:
            cp = update_score_interface(cp)
        elif choice == 4:
            generate_reports_interface(cp)  # No return value
        elif choice == 5:
            browser = synergy.initialize_driver_with_user_input()
            cp = synergy.create_classperiod_from_synergy(browser)
        elif choice == 6:
            if bool(browser):
                write_overall_grades_to_synergy(cp, browser)
            else:
                print("Error: no web driver object initialized.")
        elif choice == exit_choice:
            save_and_exit(cp)  # No return value


# Main code: run an interface.
if __name__ == "__main__":
    cp = load_sample_classperiod()
    main_menu(cp)
