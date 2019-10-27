# -*- coding: utf-8 -*-
"""
Matthew Dirks
MET CS 521
Due date: 10/19/2019
Final Project
Description: sbg_data_methods module.
This module contains functions dealing with the ClassPeriod class
"""

# import modules
import lt_module as ltm
import student_module as stu
import sbg_data_methods as dm
import datetime
from prettytable import PrettyTable


class ClassPeriod:
    '''
    This is a class to hold all data about a group of students and their
    scores on a set of LTs.
    '''

    def __init__(self, description, students_in_period=[], course_lts=[]):
        '''
        Constructor method for a ClassPeriod.
        There is one mandatory argument, a string used to describe the
        class period (e.g. "Period_1"). The description should
        contain only characters that are valid in file names.
        The function also takes two optional arguments:
            students_in_period, a list of Student objects
            course_lts, a list of LearningTarget objects
        '''
        self.description = description
        self.students_in_period = students_in_period
        self.course_lts = course_lts
        # If ClassPeriod was generated from some data source,
        # remove any exempts
        self.remove_exempts()

    def __repr__(self):
        '''
        This function returns a string representation of the class period.
        '''
        lt_table = PrettyTable()
        lt_table.field_names = ['Learning Target', 'Description']
        for lt in self.course_lts:
            lt_table.add_row([lt.lt_label, lt.brief])
        student_table = PrettyTable()
        student_table.field_names = ['Last',
                                     'First',
                                     'Scores',
                                     'Overall LT grade']
        for student in self.students_in_period:
            scores_str = ']\n'.join(str(student.scores)[1:-1].split('],'))
            student_table.add_row([student.lastname,
                                   student.firstname,
                                   scores_str,
                                   str(
                                    round(100 *
                                          student.calculate_piecewise_grade()
                                          ))])
        return str(lt_table) + "\n" + str(student_table)

    def find_student(self, search):
        '''
        This method takes an int for a student ID number.
        If the student is present in the ClassPeriod, that
        Student object is returned. Otherwise False is returned.
        One use of this function is that its return value
        can be cast as a bool; that bool evaluates to True
        if the student is present and False if not.
        '''
        for student in self.students_in_period:
            if student.sid == search:
                return student
        return False

    def has_lt_with_label(self, search):
        '''
        This method returns True if the ClassPeriod has an LT with a specified
        label, False otherwise.
        '''
        for lt in self.course_lts:
            if lt.lt_label == search:
                return True
        return False

    def remove_exempts(self, exempt_code=-1):
        '''
        This method looks at all student score dictionaries.
        If there is any LT for which the student's most recent score
        is -1 (code for exempt), that LT is removed from the student's
        score dict.
        '''
        for student in self.students_in_period:
            for lt in self.course_lts:
                # Careful! The -1 in the next line refers to
                # most recent score, not the value of exempt_code!
                try:
                    if student.scores[lt.lt_label][-1] == exempt_code:
                        student.scores.pop(lt.lt_label)
                except KeyError:
                    pass

    def get_list_of_overall_grades(self):
        '''
        This method calculates overall grades for each student
        and returns a list containing all of them.
        The grades are returned as percentages (0-100) rather than
        decimals (0.00 - 1.00).
        '''
        grades = []
        for student in self.students_in_period:
            grades.append(round(student.calculate_piecewise_grade()*100))
        return grades


def student_list_from_datafile_list(list_of_datafiles):
    '''
    This function takes a list of strings specifying data files,
    one data file per student. It creates a Student object
    from each data file and returns a list of those Students.
    '''
    student_list = []
    for filename in list_of_datafiles:
        next_student = stu.make_student_from_datafile(filename)
        student_list.append(next_student)
    return student_list


def build_classperiod_from_data(data_str):
    '''
    This function takes a data string that has been read in from
    a file and uses it to build a ClassPeriod.
    It assumes that the first line of the file is the ClassPeriod description.
    The second line should be a filename for a file of learning targets,
    and every subsequent line should contain the filename of a file
    containing student data.
    '''
    lines = data_str.split("\n")
    description = lines[0]  # Get description
    list_of_student_files = lines[2:]  # Get list of student data files
    # Generate list of Students
    student_list = student_list_from_datafile_list(list_of_student_files)
    # Get learning target data file
    lt_filename = lines[1]
    # Generate list of LearningTargets
    lt_list = ltm.build_lt_list_from_datafile(lt_filename)
    # Create and return the ClassPeriod
    return ClassPeriod(description, student_list, lt_list)


def build_classperiod_from_datafile(filename):
    '''
    This function creates a class period from a specified data file.
    It assumes that the first line of the file is the ClassPeriod description.
    The second line should be a filename for a file of learning targets,
    and every subsequent line should contain the filename of a file
    containing student data.
    '''
    data_str = dm.fetch_data_from_file(filename)
    return build_classperiod_from_data(data_str)


def write_classperiod_to_datafile(classperiod, filename):
    '''
    This function creates/overwrites a data file to hold data on a
    class period.
    It takes two arguments: a ClassPeriod object and a string
    specifiying the destination file.
    The function returns True on success, False on failure.
    '''
    # Create a list of strings to be written.
    # First line: description
    datafile_lines = [classperiod.description]
    # Write learning targets to a file
    lt_filename = classperiod.description + "_lts.ltdat"
    lt_write_success = dm.write_lts_in_list_to_datafile(
            classperiod.course_lts, lt_filename)
    if not(lt_write_success):
        print("Error in saving Learning Targets")
        return False
    # Save name of that LT file as second line
    datafile_lines.append(lt_filename)
    # Write student data to files
    for student in classperiod.students_in_period:
        student_filename = (classperiod.description + "_" +
                            str(student.sid) + ".studat")
        student_write_success = dm.write_student_data_to_file(
                student, student_filename)
        if not(student_write_success):
            print(f"Error in saving data for student with SID {student.sid}")
            return False
        # Save name of that student data file
        datafile_lines.append(student_filename)
    string_to_write = "\n".join(datafile_lines)
    # Attempt to open file in write mode; create if it doesn't exist yet
    try:
        with open(filename, "w+") as data_file:
            data_file.write(string_to_write)
            return True
    except IOError:
        print(f"Could not open file {filename}.")
        return False


def generate_reports(cp):
    '''
    This function takes a ClassPeriod as an argument.
    It then writes grade reports for each Student in the ClassPeriod
    to .txt files.
    The function returns True on success, False on failure.
    '''
    success = True
    for student in cp.students_in_period:
        date_str = str(datetime.datetime.now()).split(' ')[0]
        filename = "_".join([date_str,
                             cp.description,
                             "sid" + str(student.sid),
                             student.lastname,
                             student.firstname,
                             "grade_report.txt"])
        try:
            with open(filename, "w+") as student_report_file:
                student_report_file.write(student.report(cp.course_lts))
        except IOError:
            print(f"Warning: could not write to file {filename}")
            success = False
    return success


# Unit tests
if __name__ == "__main__":
    import data_for_unit_testing as dfut
    # Create sample class period
    cp = ClassPeriod("Period X Grades",
                     dfut.sample_list_of_students(),
                     dfut.sample_list_of_lts())
    # Test __repr__()
    print("Testing __repr__() method for ClassPeriod:")
    print(cp)  # Print for visual inspection
    input("(1/4) Inspect visually and press enter.")
    print("\n\n")
    # Test find_student()
    print("Testing find_student():")
    assert cp.find_student(1) == cp.students_in_period[0]  # Aerik == Aerik
    assert cp.find_student(9) == cp.students_in_period[8]  # Ivan == Ivan
    assert cp.find_student(42) is False  # No student with sid==42
    print("Success!\n\n")
    # Test has_lt_with_label()
    print("Testing has_lt_with_label():")
    assert cp.has_lt_with_label('LT01')  # LT-01 should be present
    assert not(cp.has_lt_with_label('This LT should not exist'))
    print("Success!\n\n")
    # Test student_list_from_datafile_list
    print("Testing student_list_from_datafile_list():")
    datafile_list = []
    for index in range(1, 10):
        datafile_list.append("sample_classperiod_" + str(index) + ".studat")
    student_list = student_list_from_datafile_list(datafile_list)
    # Make sure everything in the list is a Student
    for student in student_list:
        assert type(student) == stu.Student
        print(student)  # Print for visual inspection
    input("(2/4) Inspect visually and press enter.")
    print("Success!\n\n")
    # Test build_classperiod_from_data()
    print("Testing build_classperiod_from_data()")
    cp = build_classperiod_from_data(
            dm.fetch_data_from_file("sample_classperiod.txt"))
    assert type(cp) == ClassPeriod
    print(cp)  # Print for visual inspection
    input("(3/4) Inspect visually and press enter.")
    print("Success!\n\n")
    # Test build_classperiod_from_datafile()
    print("Testing build_classperiod_from_datafile():")
    cp = build_classperiod_from_datafile("sample_classperiod.txt")
    assert type(cp) == ClassPeriod
    print(cp)  # Print for visual inspection
    input("(4/4) Inspect visually and press enter.")
    # Test write_classperiod_to_datafile(classperiod, filename)
    print("Testing write_classperiod_to_datafile():")
    # Don't overwrite "sample_classperiod.txt"
    # Instead, write cp to a new file.
    # Read that into a new ClassPeriod, cp2.
    # Write cp2 to that file and read it in again.
    # Make sure we get the same read result both times
    # by comparing the __repr__() results from the two reads.
    new_filename = "unit_test_cp.txt"
    # write_classperiod_to_datafile() returns True on success
    assert write_classperiod_to_datafile(cp, new_filename)
    cp2 = build_classperiod_from_datafile(new_filename)
    write_classperiod_to_datafile(cp, new_filename)
    assert (cp2.__repr__() ==
            build_classperiod_from_datafile(new_filename).__repr__())
    print("Success!\n\n")
    # Test generate_reports()
    print("Testing generate_reports()")
    assert generate_reports(cp)  # generate_reports returns True on success
    input("Reports should be generated. Inspect text files and press enter.")
    print("Success!\n\n")
    # Print success message.
    print("All assertion test successful.")
    print("If the visuals and reports looked good, " +
          "this module should function as expected")
    print("You may want to delete the generated reports and the file " +
          "'unit_test_cp.txt'.")