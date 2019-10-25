# -*- coding: utf-8 -*-
"""
Matthew Dirks
MET CS 521
Due date: 10/19/2019
Final Project
Description: nitty_gritty_of_grading (NGOG) module.
This file is a module of functions for calculating grades
according to a standards-based system
"""

# Global variables
DEFAULT_X_CODE = -1
DEFAULT_VALID_SCORES = [-1, 0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]

def list_of_most_recent_scores(dict_of_all_scores, exempt_code=DEFAULT_X_CODE):
    '''
    This function takes one argument: a dictionary of student scores for all
    learning targets. It returns a list consisting of the most recent scores.
    This function assumes the convention that the most recent score is stored
    as the last element of a list.
    For example, given the dictionary
    {"LT2A": [2,3,3], "LT2B": [2,4]}
    list_of_most_recent_scores() would return [3,4]
    (because the student has been assessed on two learning targets, and
    the most recent scores are a 3 on the first and a 4 on the second).
    '''
    list_of_scores = []
    for record in dict_of_all_scores.items():
        recent = record[1][-1]
        if recent != exempt_code:
            list_of_scores.append(record[1][-1])
    return list_of_scores


def score_is_valid(score, valid_scores=DEFAULT_VALID_SCORES):
    '''
    This function takes two arguments: a score, and a list of numbers
    that count as a valid score.
    It returns True if the score is in that list, False otherwise.
    '''
    return score in valid_scores


def list_is_valid(list_of_scores,
                  valid_scores=DEFAULT_VALID_SCORES):
    '''
    This function takes two arguments: a list of scores, and a list
    of numbers that count as valid scores.
    It returns True if every score in the list_of_scores is valid,
    False otherwise.
    '''
    # Create a Map object of bools corresponding to the list of scores:
    # each entry is True or False depending on whether the corresponding
    # entry in the list is valid.
    for score in list_of_scores:
        if not(score in valid_scores):
            return False
    return True


def lt_count(list_of_scores, exempt_code=DEFAULT_X_CODE):
    '''
    This function takes a list of scores and returns the number of
    learning targets on which a student has been assessed.
    It ignores any scores that match the exempt code.
    '''
    count = 0
    for score in list_of_scores:
        if score != exempt_code:
            count += 1
    return count


def free_of_zeroes_and_ones(list_of_scores):
    '''
    This function checks whether a list of scores contains any 0s or 1s.
    If it does not contain any 0s or 1s, the function returns True.
    If it does contain at least one 0 or 1, the function returns False.
    '''
    return not(0 in list_of_scores or 1 in list_of_scores)


def count_of(search, list_of_scores):
    '''
    This function takes two arguments: search value and a list.
    It returns the number of times that the search occurs in the list.
    '''
    count = 0
    for score in list_of_scores:
        if score == search:
            count += 1
    return count


def count_of_lts_met(list_of_scores):
    '''
    This function returns the number of LTs on which a student has earned
    a 3, 3.5, or 4
    '''
    return (count_of(3, list_of_scores) +
            count_of(3.5, list_of_scores) +
            count_of(4, list_of_scores))


def pct_of_lts_met(list_of_scores):
    '''
    This function returns the percentage of learning targets on which
    a student is meeting or exceeding standard.
    '''
    lt_count_val = lt_count(list_of_scores)
    if lt_count_val == 0:  # Avoid division by 0!
        return 0
    return (count_of_lts_met(list_of_scores) / lt_count(list_of_scores))


def curved_pct_of_lts_met(list_of_scores):
    '''
    This function scales the percentage of learning targets met to align with
    conventional percent cutoffs for grades.
    Specifically,

    If a student is meeting at least 90% of the learning targets, this function
    returns a percentage in the A range (90% - 100%).

    If a student is meeting 80% - 89% of the learning targets, this function
    returns a percentage in the B range (80% - 89%).

    If a student is meeting 65% - 79% of the learning targets, this function
    returns a percentage in the C range (70% - 79%)

    If a student is meeting 50% - 64% of the learning targets, this function
    returns a percentage in the D range (60% - 69%)

    If a student is meeting fewer than 50% of learning targets, this function
    returns a percentage in the F range (50% - 59%).

    Note that 50% is the lowest F assigned by this function.
    '''
    pct = pct_of_lts_met(list_of_scores)
    if pct >= 0.8:
        curved = pct
    elif pct >= 0.5:
        curved = (2 * pct + 0.8) / 3
    else:
        curved = (0.2 * pct + 0.5)
    return round(curved, 2)


def has_A_from_LTs(list_of_scores):
    '''
    This function returns True if a student is meeting three critera:
        (i) is meeting standard (3 or 4) on at least 90%
            of the learning targets
        (ii) is exceeding standard (4) on at least 50% of the learning targets
        (iii) has no 0s or 1s
    '''
    return (pct_of_lts_met(list_of_scores) >= 0.9 and
            count_of(4, list_of_scores) >= (lt_count(list_of_scores) / 2) and
            free_of_zeroes_and_ones(list_of_scores))


def has_B_from_LTs(list_of_scores):
    '''
    This function returns True if a student does not qualify for an A
    and meets two criteria:
        (i) is meeting standard on 80% of the learning targets
        (ii) has no 0s or 1s
    '''
    return (not(has_A_from_LTs(list_of_scores)) and
            pct_of_lts_met(list_of_scores) >= 0.8 and
            free_of_zeroes_and_ones(list_of_scores))


def has_C_from_LTs(list_of_scores):
    '''
    This function returns True if a student does not qualify for an A
    or a B, and is meeting standard on at least 65% of the learning targets.
    '''
    return (not(has_A_from_LTs(list_of_scores)) and
            not(has_B_from_LTs(list_of_scores)) and
            pct_of_lts_met(list_of_scores) >= 0.65)


def has_D_from_LTs(list_of_scores):
    '''
    This function returns True if a student does not qualify for
    an A, B, or C, and is meeting standard on at least 50% of the learning
    targets.
    '''
    return (not(has_A_from_LTs(list_of_scores)) and
            not(has_B_from_LTs(list_of_scores)) and
            not(has_C_from_LTs(list_of_scores)) and
            pct_of_lts_met(list_of_scores) >= 0.5)


def has_F_from_LTs(list_of_scores):
    '''
    This function returns True if a student does not qualify for
    an A, B, C, or D.
    '''
    return (not(has_A_from_LTs(list_of_scores)) and
            not(has_B_from_LTs(list_of_scores)) and
            not(has_C_from_LTs(list_of_scores)) and
            not(has_D_from_LTs(list_of_scores)))


def simple_grade(list_of_scores):
    '''
    This function takes a list of student scores and returns
    the student's grade as one of the following five numbers:
        50 (F), 65 (D), 75 (C), 85 (B), 95 (A)
    This function is less useful than piecewise_grade, which should be
    used in most cases, but can be useful as a point of comparison
    for more complicated functions such as piecewise_grade.
    '''
    assert list_is_valid(list_of_scores, [0, 1, 1.5, 2, 2.5, 3, 3.5, 4])
    if has_A_from_LTs(list_of_scores):
        return 95
    elif has_B_from_LTs(list_of_scores):
        return 85
    elif has_C_from_LTs(list_of_scores):
        return 75
    elif has_D_from_LTs(list_of_scores):
        return 65
    else:
        assert has_F_from_LTs(list_of_scores)
        return 50


def letter_grade(list_of_scores):
    '''
    This function takes a list of student scores and returns
    the student's letter grade (char).
    '''
    simple_pct = simple_grade(list_of_scores)
    if simple_pct == 95:
        return 'A'
    elif simple_pct == 85:
        return 'B'
    elif simple_pct == 75:
        return 'C'
    elif simple_pct == 65:
        return 'D'
    elif simple_pct == 50:
        return 'F'
    else:  # Something bad happened
        return 'X'


def piecewise_grade(list_of_scores):
    '''
    This function takes a list of scores and returns a percentage
    to represent the student's grade. The percentage is curved
    using the piecewise function described in cuved_pct_of_lts_met(),
    and is then modified, as follows:
        - If a student is meeting more than 90% of LTs but has a B,
                their grade is returned as 89%.
        - If a student is earning more than 80% of LTs but has a C,
                their grade is returned as 79%.
    '''
    assert list_is_valid(list_of_scores)
    cpoltm = curved_pct_of_lts_met(list_of_scores)
    if has_A_from_LTs(list_of_scores):
        grade = cpoltm
    elif has_B_from_LTs(list_of_scores):
        if cpoltm >= 0.9:  # Student has not earned enough 4s for an A
            grade = 0.89
        else:  # Student has not met standard on 90% of LTs
            grade = cpoltm
    elif has_C_from_LTs(list_of_scores):
        if cpoltm >= 0.8:  # Student has 0s or 1s
            grade = 0.79
        else:
            grade = cpoltm
    else:
        assert has_D_from_LTs(list_of_scores) or has_F_from_LTs(list_of_scores)
        assert cpoltm < 0.7
        grade = cpoltm
    return round(grade, 3)


# Unit tests
if __name__ == "__main__":
    # Import sample student data
    from data_for_unit_testing import sample_list_of_students
    students = sample_list_of_students()
    # Test list_of_most_recent_scores()
    print("Testing list_of_most_recent_scores():")
    # Create a list whose elements are each a list of a student's
    # most recent scores
    most_recent_scores = list(
            map(lambda x: list_of_most_recent_scores(x.scores), students))
    # Aerik's most recent scores should be those shown on next line
    assert most_recent_scores[0] == [4, 4, 4, 4, 4, 3, 3, 3, 3, 3]
    assert most_recent_scores[8] == []  # Ivan should have no scores
    print("Success!")
    # Test score_is_valid()
    print("Testing score_is_valid():")
    assert score_is_valid(4)
    assert score_is_valid(2.5)
    assert not(score_is_valid(5))
    assert score_is_valid(5, [1, 2, 3, 4, 5])
    assert not(score_is_valid(3, [1, 2, 4]))
    print("Success!")
    # Test list_is_valid()
    print("Testing list_is_valid():")
    assert list_is_valid([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4])
    assert not(list_is_valid([2, 2.5, 2.6, 2.7, 4]))
    assert not(list_is_valid([2.7]))
    assert not(list_is_valid([3, 4], [1, 5]))
    assert list_is_valid([3, 4], [1, 2, 3, 4, 5])
    print("Success!")
    # Test lt_count
    print("Testing lt_count():")
    assert lt_count([1, 2, 3]) == len([1, 2, 3])
    print("Success!")
    # Test free_of_zeroes_and_ones
    print("Testing free_of_zeroes_and_ones():")
    assert free_of_zeroes_and_ones([2, 2, 3, 4, 3, 2, 4])
    assert not(free_of_zeroes_and_ones([1, 2, 3, 4, 0, 1, 4]))
    print("Success!")
    # Test count_of()
    print("Testing count_of():")
    assert count_of(2, [2, 2, 3, 4, 1, 4, 2]) == 3
    assert count_of(1, [2, 3]) == 0
    print("Success!")
    # Test count_of_lts_met()
    print("Testing count_of_lts_met():")
    assert count_of_lts_met([1, 2, 3, 2.5, 3.5, 4]) == 3
    print("Success!")
    # Test pct_of_lts_met()
    print("Testing pct_of_lts_met():")
    assert pct_of_lts_met([1, 2, 3, 2.5, 3.5, 4]) == 0.5
    print("Success!")
    # Test curved_pct_of_lts_met()
    print("Testing curved_pct_of_lts_met():")
    # Run through the sample students and check on their scores.
    curved_scores = list(map(curved_pct_of_lts_met, most_recent_scores))
    assert curved_scores == [1.0,  # Aerik
                             1.0,  # Bob; has B but is meeting all LTs
                             0.9,  # Catherine
                             0.8,  # Dilbert
                             0.9,  # Egbert; has C but is meeting 90% of LTs
                             .73,  # Farina
                             .67,  # Gilgamesh
                             .54,  # Henry
                             0.5,  # Ivan
                             1.0]  # Janet
    print("Success!")
    # Test has_A_from_LTs()
    print("Testing has_A_from_LTs():")
    students_with_As = list(map(has_A_from_LTs, most_recent_scores))
    assert students_with_As == [True,  # Aerik
                                False,  # Bob
                                True,  # Catherine
                                False,  # Dilbert
                                False,  # Egbert
                                False,  # Farina
                                False,  # Gilgamesh
                                False,  # Henry
                                False,  # Ivan
                                True]   # Janet
    print("Success!")
    # Test has_B_from_LTs()
    print("Testing has_B_from_LTs():")
    students_with_Bs = list(map(has_B_from_LTs, most_recent_scores))
    assert students_with_Bs == [False,  # A
                                True,  # B
                                False,  # C
                                True,  # D
                                False,  # E
                                False,  # F
                                False,  # G
                                False,  # H
                                False,  # I
                                False]  # J
    print("Success!")
    # Test has_C_from_LTs()
    print("Testing has_C_from_LTs():")
    students_with_Cs = list(map(has_C_from_LTs, most_recent_scores))
    assert students_with_Cs == [False,  # A
                                False,  # B
                                False,  # C
                                False,  # D
                                True,  # E
                                True,  # F
                                False,  # G
                                False,  # H
                                False,  # I
                                False]  #J
    print("Success!")
    # Test has_D_from_LTs()
    print("Testing has_D_from_LTs():")
    students_with_Ds = list(map(has_D_from_LTs, most_recent_scores))
    assert students_with_Ds == [False,  # Aerik
                                False,  # Bob...
                                False,  # C
                                False,  # D
                                False,  # E
                                False,  # F
                                True,  # G
                                False,  # H
                                False,  # I
                                False]  # J
    print("Success!")
    # Test has_F_from_LTs()
    print("Testing has_F_from_LTs():")
    students_with_Fs = list(map(has_F_from_LTs, most_recent_scores))
    assert students_with_Fs == [False,  # Aerik
                                False,  # Bob...
                                False,  # C
                                False,  # D
                                False,  # E
                                False,  # F
                                False,  # G
                                True,  # H
                                True,  # I
                                False] # J
    print("Success!")
    # Test simple_grade()
    print("Testing simple_grade():")
    simple_grades = list(map(simple_grade, most_recent_scores))
    assert simple_grades == [95,  # Aerik
                             85,  # Bob
                             95,  # Catherine
                             85,  # Dilbert
                             75,  # Egbert
                             75,  # Farina
                             65,  # Gilgamesh
                             50,  # Henry
                             50,  # Ivan
                             95]  # Janet
    print("Success!")
    # Test letter_grade()
    print("Testing letter_grade():")
    letter_grades = list(map(letter_grade, most_recent_scores))
    assert letter_grades == ['A', 'B', 'A', 'B', 'C', 'C', 'D', 'F', 'F', 'A']
    print("Success!")
    # Test piecewise_grade()
    print("Testing piecewise_grade():")
    piecewise_grades = list(map(piecewise_grade, most_recent_scores))
    assert piecewise_grades == [1, .89, .9, .8, .79, .73, .67, .54, .5, 1]
    print("Success!\n\n")
    print("All tests were successful.")
