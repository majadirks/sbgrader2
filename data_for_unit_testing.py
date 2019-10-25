# -*- coding: utf-8 -*-
"""
Matthew Dirks
MET CS 521
Due date: 10/19/2019
Final Project
Description: data_for_unit_testing. This module contains data that
will be useful in unit testing.
"""

# Modules will be imported inside of functions
# to avoid infinite loops when those modules themselves are tested.


def sample_list_of_lts():
    '''
    This function imports lt_module and returns a sample list of 10 LTs
    labeled 'LT01', 'LT02', ..., 'LT10'.
    '''
    # Create some LTs to use in our unit tests.
    # These will be called LT01, LT02, ... , LT09, LT10
    import lt_module as ltm
    list_of_all_lts = []
    for index in range(10):
        lt_num = index + 1
        lt_num_str = ('0' * (lt_num < 10)) + str(lt_num)
        lt_label = 'LT' + lt_num_str
        lt_brief = 'This is a brief description of ' + lt_label
        lt_description = 'This is a verbose description of ' + lt_label
        list_of_all_lts.append(ltm.LearningTarget(lt_label,
                                                  lt_brief,
                                                  lt_description))
    return list_of_all_lts


def sample_list_of_students():
    '''
    This function imports the student_module and returns a sample list
    of nine students.
    '''
    import student_module as stu
    # Create some students for use in our unit tests
    aerik = stu.Student(1, 'Frank', 'Aerik', 'he')
    bob = stu.Student(2, 'Livingston', 'Bob', 'he')
    catherine = stu.Student(3, 'Hilders', 'Catherine', 'she')
    dilbert = stu.Student(4, 'Adams', 'Dilbert', 'he')
    egbert = stu.Student(5, 'Wheatley', 'Egbert', 'he')
    farina = stu.Student(6, 'Spelt', 'Farina', 'she')
    gilgamesh = stu.Student(7, 'Mesopo', 'Gilgamesh', 'he')
    henry = stu.Student(8, 'Harrison', 'Henry', 'he')
    ivan = stu.Student(9, 'Whittier', 'Ivan', 'he')
    janet = stu.Student(10, 'Foo', 'Janet', 'she')
    list_of_students = [aerik, bob, catherine, dilbert, egbert, farina,
                        gilgamesh, henry, ivan, janet]

    # Give the students some scores
    aerik.scores = {'LT01': [1, 2, 4], 'LT02': [2, 4], 'LT03': [2, 4],
                    'LT04': [1, 3, 4], 'LT05': [2, 4], 'LT06': [2, 3],
                    'LT07': [2, 3], 'LT08': [1, 3], 'LT09': [2, 3],
                    'LT10': [2, 3]}
    bob.scores = {'LT01': [4], 'LT02': [4], 'LT03': [4], 'LT04': [4],
                  'LT05': [0, 3], 'LT06': [2, 3], 'LT07': [1, 3],
                  'LT08': [2, 3], 'LT09': [1, 2, 3], 'LT10': [3]}
    catherine.scores = {'LT01': [2, 4], 'LT02': [2, 2, 2, 3, 4],
                        'LT03': [3, 4], 'LT04': [4], 'LT05': [4],
                        'LT06': [2, 4], 'LT07': [4], 'LT08': [4],
                        'LT09': [4], 'LT10': [2]}
    dilbert.scores = {'LT01': [4], 'LT02': [4], 'LT03': [3], 'LT04': [4],
                      'LT05': [4], 'LT06': [3], 'LT07': [4], 'LT08': [4],
                      'LT09': [2], 'LT10': [2, 2]}
    egbert.scores = {'LT01': [3, 4], 'LT02': [4], 'LT03': [4], 'LT04': [4],
                     'LT05': [4], 'LT06': [4], 'LT07': [4], 'LT08': [4],
                     'LT09': [4], 'LT10': [1]}
    farina.scores = {'LT01': [4], 'LT02': [4], 'LT03': [2, 4], 'LT04': [4],
                     'LT05': [4], 'LT06': [4], 'LT07': [4], 'LT08': [2],
                     'LT09': [2], 'LT10': [2]}
    gilgamesh.scores = {'LT01': [4], 'LT02': [4], 'LT03': [4], 'LT04': [4],
                        'LT05': [4], 'LT06': [4], 'LT07': [2, 2], 'LT08': [2],
                        'LT09': [2], 'LT10': [2]}
    henry.scores = {'LT01': [4], 'LT02': [4], 'LT03': [2], 'LT04': [1],
                    'LT05': [2, 2], 'LT06': [1, 2], 'LT07': [2], 'LT08': [2],
                    'LT09': [1], 'LT10': [2]}
    ivan.scores = {}  # Ivan has not taken any assessments yet.
    janet.scores = {'LT01': [-1], 'LT02': [4]}  # Janet is exempt on LT01
    return list_of_students


# Make sure that all worked properly
if __name__ == "__main__":
    print("Printing all LearningTarget objects in sample ClassPeriod:")
    for lt in sample_list_of_lts():
        print(lt.lt_label)
        print(lt.brief_string())
        print(lt.description)
        print("\n")
    print("Printing all Student objects in sample ClassPeriod:")
    for student in sample_list_of_students():
        print(student)
