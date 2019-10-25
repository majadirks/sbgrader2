# -*- coding: utf-8 -*-
"""
Matthew Dirks
10/21/2019
Module to scrape SBG data from Synergy Education Platform

Dependencies:
    selenium
    geckodriver (for Firefox)
    ChromeDriver (for Chrome)
"""

# import modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import student_module as stu
import lt_module as ltm
import classperiod_module as cpm
import string
from nitty_gritty_of_grading import DEFAULT_X_CODE

# Global variables (shudder)
# Keyword to look for in assignment name of 'overall grade' column
OVERALL_GRADE_KEYWORD = 'OVERALL'

# Define functions


def count_assignments(driver):
    '''
    This function takes a selenium WebDriver object as an argument.
    The WebDriver should be pointed at a Grade Book Main page
    on the Synergy Education Platform.
    It returns the number of columns on that gradebook page.
    '''
    assignment_elts = driver.find_element_by_id(
            'ctl00_lowerFixedBarContainer_hf_AssignmentNameIndex')
    assignment_list_str = assignment_elts.get_attribute('value')
    assignments = assignment_list_str.split('║')
    return len(assignments)


def assignment_is_probably_lt(assignment_name):
    '''
    This function returns True if a given string is likely the name
    of an LT assignment.
    It's really stupid. It just checks whether the first two characters
    are 'LT'
    '''
    return assignment_name[0:2] == 'LT'


def get_classperiod_name(driver):
    '''
    This function takes a selenium WebDriver object as an argument.
    The WebDriver should be pointed at a Grade Book Main page
    on the Synergy Education Platform.
    The function returns a string describing the class period.
    All spaces and commas from Synergy are replaced by underscores.
    (e.g. 'Dirks_M__Int_Math_Top_1_S1(3)')
    '''
    '''
    Look for code like the following
    <span id="ctl00_lbl_ACC_ClassFocus" class="sr-only">
        Current Focus: (S1) Dirks, M  Int Math Top 1 S1(3)
    </span>
    '''
    span_elt = driver.find_element_by_id('ctl00_lbl_ACC_ClassFocus')
    class_name = str(span_elt.text)
    # Chop off leading string 'Current focus',
    # and also everything after 'SEC'.
    current_focus_str = 'Current_Focus: '
    current_focus_len = len(current_focus_str)
    sec_index = class_name.find(' SEC:')
    class_name = class_name[current_focus_len:sec_index].strip()
    # Exclude evr
    # Strip and replace all punctuation with underscores
    exclude = set(string.punctuation + ' ')
    for ch in class_name:
        if ch in exclude:
            class_name = class_name.replace(ch, '_')
    return class_name


def get_lt_list(driver):
    '''
    This function takes a selenium WebDriver object as an argument.
    The WebDriver should be pointed at a Grade Book Main page
    on the Synergy Education Platform.
    The function returns a list of LearningTarget objects
    corresponding to gradebook assignments whose titles begin with 'LT'.
    For example, if there is an assignment called 'LT1A Basket Weaving',
    the list will contain a corresponding LearningTarget object
    with lt_label '1A' and lt_brief 'Basket Weaving'.
    '''
    list_of_lts = []
    assignment_elts = driver.find_element_by_id(
            'ctl00_lowerFixedBarContainer_hf_AssignmentNameIndex')
    assignment_list_str = assignment_elts.get_attribute('value')
    assignments = assignment_list_str.split('║')
    for column, assignment in enumerate(assignments):
        assignment = assignment.strip()
        if assignment_is_probably_lt(assignment):
            first_space_index = assignment.find(' ')
            lt_label = assignment[0:first_space_index]
            lt_brief = assignment[first_space_index+1:]
            list_of_lts.append(ltm.LearningTarget(lt_label,
                                                  lt_brief,
                                                  gb_column=column))
    return(list_of_lts)


def get_student_list(driver):
    '''
    This function takes a selenium WebDriver object as an argument.
    The WebDriver should be pointed at a Grade Book Main page
    on the Synergy Education Platform.
    The function returns a list of Student objects
    corresponding to the students on the Grade Book page.
    '''
    list_of_students = []
    table_id = driver.find_element_by_id('ctl00_cphbody_gv_StudentsScores')
    students = table_id.find_elements_by_tag_name('tr')
    for index, record in enumerate(students[1:-1]):  # Skip heading and bottom
        # Figure out student name by splitting on newlines and then commas.
        # If for some reason a student name has multiple commas,
        # assume everything after the first comma is in the first name.
        student_name = str(record.text).split('\n')[0].split(', ')
        student_last = student_name[0]
        student_first = student_name[1]
        if len(student_name) > 2:  # Add on to first name if necessary
            for next_name in student_name[2:]:
                student_first += ', ' + next_name
        list_of_students.append(
                stu.Student(index, student_last, student_first))
    return(list_of_students)


def get_lt_score_matrix(driver, list_of_lts):
    '''
    This function takes two arguments:
        (i) a selenium WebDriver object pointed to a Synergy gradebook page
        (ii) a list of LTs whose gb_column values correspond to their
             position in the Synergy gradebook page
    The WebDriver should be pointed at a Grade Book Main page
    on the Synergy Education Platform.
    The function returns a list of lists, where each inner list
    contains one student's scores on LTs in the list.
    If the student does not have a score, the score is listed as -1.
    '''
    score_matrix = []
    # Find Synergy table with scores
    table_id = driver.find_element_by_id('ctl00_cphbody_GV_Assignments')
    # Find rows containing scores (skip header and footer)
    rowstrings = table_id.find_elements_by_tag_name('tr')[1:-1]
    # Build score matrix
    for student_index, rowstring in enumerate(rowstrings):
        score_matrix.append([])  # Initialize student row as empty list
        row = str(rowstring.text).split('\n')
        for index, score in enumerate(row):
            # Fix bug where blank boxes are lumped into next score
            if score[:2] == '  ':
                row.insert(index, '  ')
                row[index + 1] = score.strip()
                score = row[index]
            # If this column corresponds to an LT, add score to the matrix.
            lt = ltm.find_lt_by_column(index, list_of_lts)
            if bool(lt):  # If this column has a corresponding LT
                try:
                    score = float(score)
                except ValueError:
                    score = DEFAULT_X_CODE
                score_matrix[student_index].append(score)
    return score_matrix


def initialize_driver_with_user_input():
    '''
    This This function opens a browser window and instructs a user to navigate
    to a gradebook page on Synergy.
    It creates and returns the relevant WebDriver object.
    '''
    # Prompt user to navigate to gradebook, and then grab source
    print("1: Wait for the browser to open.")
    print("2: Navigate to the gradebook page you want to update.")
    print("3: Update LT scores in Synergy if applicable.")
    print("4: Then come back here and press Enter.")
    # Launch Chrome and go to Synergy
    browser = webdriver.Chrome()
    browser.get(
            'https://wa-bsd405.edupoint.com/')
    input("Press Enter to download gradebook data>")
    # Focus on source for main frame in current browser window
    browser.switch_to.frame(browser.find_element_by_id('FRAME_CONTENT'))
    return browser


def create_classperiod_from_synergy(browser):
    '''
    This function takes one argument, a WebDriver object pointed to a
    Synergy gradebook page.
    It returns a ClassPeriod object containing the students on that page,
    the learning targets, and student scores on learning targets.
    If a student score is blank, a letter, or anything other than
    a valid score (0-4), is is replaced with -1 (exempt).
    '''
    # Scrape data
    class_name = get_classperiod_name(browser)
    list_of_lts = get_lt_list(browser)  # Get list of LTs
    student_list = get_student_list(browser)  # Get list of students
    score_matrix = get_lt_score_matrix(browser, list_of_lts)  # Get scores

    # Create ClassPeriod object from the above data
    cp = cpm.ClassPeriod(class_name, student_list, list_of_lts)
    # Add student scores to the ClassPeriod
    for student_index, student in enumerate(cp.students_in_period):
        # Get the list of student scores across LTs.
        # This will be a list of floats such as [3.0, 4.0, 2.0]
        scores = score_matrix[student_index]
        for score_index, score in enumerate(scores):
            lt_label = list_of_lts[score_index].lt_label
            assert type(score) == float or type(score) == int
            student = stu.add_lt(student, lt_label, score)
    return cp


def assignment_exists_with_keyword(driver, keyword):
    '''
    Uses a selenium WebDriver pointed at a Synergy gradebook page
    to check whether an assignment exists whose title contains
    the specified keyword. Returns True if so, False if not.
    '''
    assignment_elts = driver.find_element_by_id(
            'ctl00_lowerFixedBarContainer_hf_AssignmentNameIndex')
    assignment_list_str = assignment_elts.get_attribute('value')
    assignments = assignment_list_str.split('║')
    for assignment in assignments:
        if keyword.upper() in assignment.upper():
            return True
    return False


def fill_overall_scores(driver,
                        scores,
                        keyword=OVERALL_GRADE_KEYWORD):
    '''
    This function takes three arguments:
        (i) driver, a selenium WebDriver argument pointed at a Synergy
            gradebook page;
        (ii) scores, a list of overall grades (ints),
             one per student;
        (iii) A keyword that is found only in the overall grade column.
             By default this should be something like "Overall".
    It returns True on success, False on failure.
    Note that the grades must be ints or errors will occur!
    '''
    # Take care of a few conventions
    keyword = keyword.upper()
    for score in scores:
        if type(score) != int:
            print("Error: fill_overall_scores expects a list of ints.")
            print(f"Non-int found: {score}")
            return False
    # Make sure specified column exists
    if not assignment_exists_with_keyword(driver, keyword):
        print("Error: could not find overall grade column.")
        print(f"Expected to find keyword {keyword}, but could not find it.")
        return False
    # Make sure number of scores == number of students
    if not len(scores) == len(get_student_list(driver)):
        print("Error: score count does not match student count.")
        return False
    # Find column that contains the overall scores
    assignment_elts = driver.find_element_by_id(
         'ctl00_lowerFixedBarContainer_hf_AssignmentNameIndex')
    assignment_list_str = assignment_elts.get_attribute('value')
    assignments = assignment_list_str.split('║')
    overall_grade_column = -1  # Initialize as nonsense
    for column, assignment in enumerate(assignments):
        if (keyword in assignment.upper()) and\
                (assignment[:2].upper() != 'LT'):
            overall_grade_column = column
            break
    if overall_grade_column == -1:
        print("Error: could not find column " +
              f"whose header contains {keyword}")
        return False
    # Create list containing all score boxes
    table = driver.find_element_by_id('ctl00_cphbody_GV_Assignments')
    score_boxes = table.find_elements_by_class_name('SAI')
    # Click on the first-row box of the overall grade column
    score_boxes[overall_grade_column].click()
    # Write first score, press enter, and move down the list.
    for student_index in range(len(scores)):
        score_to_write = scores[student_index]
        print(f"Writing score {score_to_write} at index {student_index}")
        clicked_box = driver.switch_to.active_element
        clicked_box.send_keys(score_to_write)
        clicked_box.send_keys(Keys.ENTER)  # press enter
    driver.switch_to.parent_frame
    return True


# Main code
if __name__ == "__main__":
    # Prompt user to navigate to gradebook, and then grab source
    browser = initialize_driver_with_user_input()
    # cp = create_classperiod_from_synergy(browser)
    # print(cp)
    scores = list(range(20))  # Just for testing purposes, need a 20-elt list
    fill_overall_scores(browser, scores, 'IGNORE')
