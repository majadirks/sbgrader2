# -*- coding: utf-8 -*-
"""
Matthew Dirks
MET CS 521
Due date: 10/19/2019
Final Project
Description: This is a module of functions that generate advice
for students based on their scores. This module does not
actually perform the analysis; it just generates the strings.

The meanings of letter grades (A = Excellent, B = Exceeds Expectations, etc.)
are based on Bellevue School District Procedure 2420P:
    <https://bsd405.org/wp-content/pdf/policy/2420P.pdf>
"""

# import modules
from math import ceil  # ceiling function
import lt_module as ltm



def extract_LT_list_by_score(search, student, list_of_all_LTs):
    '''
    This function takes two arguments:
        (i) an LT score (0, 1, 2, 3, 4, or other valid scores)
        (ii) a Student object
        (iii) a list of LearningTarget objects that holds (at minimum)
            all LTs on which the student has been assessed.
    It returns a list of LearningTarget objects on which the student
    has earned the specified score.
    '''
    list_of_LTs_with_desired_score = []  # Initialize empty list
    student_lt_dict = student.scores
    # Look at each lt in the student's dictionary. If the student's
    # most recent score matches the searched-for score, add it.
    for lt_label in student_lt_dict:
        # Compare most recent score to search
        if student_lt_dict[lt_label][-1] == search:
            list_of_LTs_with_desired_score.append(
                ltm.lt_with_label(lt_label, list_of_all_LTs))
    return list_of_LTs_with_desired_score

def read_templates_from_file_to_dict(filename="advice_template.txt"):
    '''
    This function reads boilerplate from a data file.
    It replaces specific variables with appropriate values.
    Any newline characters are changed to spaces,
    and then the '\n' combination is changed to newlines.
    Finally, the text is stored in a dictionary
    which this function returns.
    '''
pass

def advice_for_A_with_all_LTs_met():
    '''
    This function returns an advice string for the scenario where a student
    is meeting all learning targets and qualifies for an A.
    '''
    advice = ("You currently have an A, which reflects excellent achievement" +
              " in this class.  Keep working hard, and focus on studying "
              "the most recent material from class.")
    return advice


def advice_for_A_without_all_LTs_met(list_of_lts_below_standard):
    '''
    This function returns an advice string for the scenario where a student
    qualifies for an A but is not yet meeting standard on all
    learning targets.
    It takes as an argument a list of LearningTarget objects representing
    LTs on which the student has earned 2.5 or below.
    '''
    advice = ("You currently have an A, which reflects excellent " +
              "achievement in this class. In order to make sure that " +
              "you're building a strong foundation for future classes, " +
              "you should study the learning targets where you are " +
              "not yet meeting standard and try to deepen your " +
              "understanding of those topics.\n\nYou are showing a " +
              "developing level of understanding on the following "
              "learning targets:\n")
    advice += ltm.rows_of_lt_briefs(list_of_lts_below_standard)
    return advice


def advice_for_B_geq_90_pct(list_of_3s, count_of_4s, total_lt_count):
    '''
    This function returns a string for the scenario in which a student
    is meeting more than 90% of the learning targets but has a B instead
    of an A. This scenario occurs if and only if the student has 3s on
    over 50% of the learning targets.
    It takes three arguments:
        The first is a list of LearningTarget objects on which the student
            has earned 3s.
        The second is an int representing the number of LTs on which
            the student has earned 4s.
        The third is an int representing the total number of LTs on which
            the student has been assessed.
    '''

    min_4_count_for_A = ceil(total_lt_count / 2)

    # For purposes of plurals, we may assume that there is more than one LT in
    # the gradebook, since it is impossible to earn a B when there are fewer
    # than five LTs.
    advice = ("You currently have a B, which means that your work in this " +
              "class exceeds expectations. You are meeting standard on " +
              "more than 90% of the learning targets. Currently, out of the " +
              f"{total_lt_count} learning targets in the grade book, you " +
              f"are meeting standard (earning 3s) on {len(list_of_3s)} and " +
              "exceeding standard (earning 4s) on an additional " +
              f"{count_of_4s}.\nIn order to raise your grade to an A, " +
              "you need to exceed standard on at least half of the " +
              f"learning targets, i.e. {min_4_count_for_A} of the LTs.\n\n" +
              "You are meeting (but not yet exceeding) standard on the " +
              "following learning targets:\n")
    advice += ltm.rows_of_lt_briefs(list_of_3s)
    return advice


def advice_for_B_under_90(list_of_2s, list_of_3s, count_of_4s, total_lt_count):
    '''
    This function returns an advice string for the scenario in which a student
    has a B and is not yet meeting 90% of learning targets.
    It takes three arguments:
        *a list of LearningTarget objects on which the student has earned 2s
        *a list of LearningTarget objects on which the student has earned 3s
        *an int representing the number of learning targets on which the
            student has earned 4s
        *an int representing the total number of learning targets on which
            the student has been assessed
    '''

    min_count_of_lts_met_for_A = ceil(total_lt_count * 0.9)
    min_4_count_for_A = ceil(total_lt_count / 2)

    advice = ("You currently have a B, which means that your work in " +
              "this class exceeds expectations. Currently, out of the " +
              f"{total_lt_count} learning targets in the grade book, you " +
              f"are meeting standard (earning 3s) on {len(list_of_3s)} " +
              f"and exceeding standard (4) on an additional {count_of_4s}. " +
              "In order to raise your grade to an A, you need to meet " +
              f"standard on 90% (or {min_count_of_lts_met_for_A}) of the " +
              "learning targets. You also need to make sure that at least " +
              "half of the learning targets " +
              f"(at least {min_4_count_for_A} of the Learning Targets) " +
              "are at the 4 level (exceeding standard).\n\nYour first " +
              "priority should be to study the following learning targets " +
              "on which you are not yet meeting standard:\n")
    advice += ltm.rows_of_lt_briefs(list_of_2s)
    advice += ("\n\nYour second priority should be to study learning " +
               "targets on which you are meeting (but not yet " +
               "exceeding) standard:\n")
    advice += ltm.rows_of_lt_briefs(list_of_3s)
    return advice


def advice_for_C_geq_80(list_of_0s_and_1s):
    '''
    This function returns an advice string for the scenario in which a student
    has a C in the course despite having passed over 80% of the LTs.
    This scenario occurs if and only if a student has 0s or 1s in the
    gradebook.
    This function takes as an argument a list of LearningTarget objects
    on which the student has scored 0 or 1.
    '''
    # We have to worry about plurals here. For now, deal with the ambiguity
    # with the construction 'learning target(s)'
    advice = ("You currently have a C in this course, which means that " +
              "your work in this course is meeting expectations.\n" +
              f"There are {len(list_of_0s_and_1s)} learning target(s) on " +
              "which you have provided an incomplete response or on " +
              "which there is no basis for assessment. In order to " +
              "raise your grade to an A or a B, you should focus on " +
              "those learning targets. As long as you have any 0s " +
              "or 1s in the gradebook, a C is the highest grade " +
              "you can earn.\n\n You should focus on studying the " +
              "following learning targets:\n")
    advice += ltm.rows_of_lt_briefs(list_of_0s_and_1s)
    return advice


def advice_for_C_under_80(list_of_0s_1s_and_2s, total_lt_count):
    '''
    This function returns an advice string for the scenario in which
    a student has a C because they are meeting between 65% and 79%
    of learning targets.
    This function takes two arguments:
        (i) a list of LearningTarget objects on which the student is not
            yet meeting standard.
        (ii) an int representing the total number of learning targets
            in the grade book
    '''
    lts_met_count = total_lt_count - len(list_of_0s_1s_and_2s)
    min_lts_for_B = ceil(0.8 * total_lt_count)
    advice = ("You currently have a C in this course, which means " +
              "that your work in this course is meeting expectations.\n" +
              f"Currently, out of the {total_lt_count} learning targets " +
              "in the grade book, you are meeting or exceeding " +
              f"standard on {lts_met_count}. In order to earn a B, " +
              "you need to meet or exceed standard on at least 80% " +
              " of the learning targets " +
              f"(i.e. {min_lts_for_B} of the learning targets).\n\n" +
              "You should focus on studying the following " +
              "learning targets:\n")
    advice += ltm.rows_of_lt_briefs(list_of_0s_1s_and_2s)
    return advice


def advice_for_D(list_of_0s_1s_and_2s, total_lt_count):
    '''
    Advice for student who has a D.
    This function takes two arguments: a list of LearningTarget
    objects on which the student is not meeting standard
    and an int representing the total number of LTs.
    '''
    min_lts_for_C = ceil(0.65 * total_lt_count)
    advice = ("You currently have a D, which means that your work in " +
              "this course is not yet satisfactory. In order to raise " +
              "your grade to a C, you need to meet or exceed standard " +
              "on at least 65% of the learning targets "+
              f"(i.e. {min_lts_for_C} of the learning targets) " +
              "\n\nYou should focus on studying the " +
              "following learning targets:\n")
    advice += ltm.rows_of_lt_briefs(list_of_0s_1s_and_2s)
    return advice


def advice_for_F(list_of_0s_1s_and_2s, total_lt_count):
    '''
    Advice for student who has an F.
    This function takes two arguments: a list of LearningTarget
    objects on which the student is not meeting standard
    and an int representing the total number of LTs.
    '''
    min_lts_for_D = ceil(0.5 * total_lt_count)
    advice = ("Your grade is currently an F, which means you are not " +
              "yet eligible for credit for this course. In order to raise " +
              "your grade to a D, you need to meet or exceed standard on " +
              "at least 50% of the leearning targets " +
              f"(i.e. {min_lts_for_D} of the learning targets). " +
              "\n\nYou should focus on studying the " +
              "following learning targets:\n")
    advice += ltm.rows_of_lt_briefs(list_of_0s_1s_and_2s)
    return advice

def advice_when_no_LTs_in_gradebook():
    '''
    Advice for student who has an F simply because they have taken
    no assessments.
    '''
    advice = ("Your grade is currently reported as an F. This is " +
              "because there are no assessment scores for you yet. " +
              "You can expect your grade to change as soon as you " +
              "complete an assessment.")
    return advice


# Unit tests
if __name__ == "__main__":
    # Get some test data
    import data_for_unit_testing as dfut
    list_of_all_lts = dfut.sample_list_of_lts()
    list_of_students = dfut.sample_list_of_students()
    aerik = list_of_students[0]
    bob = list_of_students[1]
    catherine = list_of_students[2]
    dilbert = list_of_students[3]
    egbert = list_of_students[4]
    farina = list_of_students[5]
    gilgamesh = list_of_students[6]
    henry = list_of_students[7]
    ivan = list_of_students[8]

    # Test extract_LT_list_by_score(search, student, list_of_all_LTs):
    print("Testing extract_LT_list_by_score...")
    # Aerik has no 2s
    assert extract_LT_list_by_score(2, aerik, list_of_all_lts) == []
    # Aerik has five 4s
    assert len(extract_LT_list_by_score(4, aerik, list_of_all_lts)) == 5
    # Ivan has no scores at all
    assert extract_LT_list_by_score(2, ivan, list_of_all_lts) == []
    print("Success.\n\n")

    # Print advice strings
    print("Testing advice strings:\n\n")
    # Print advice_for_A_with_all_LTs_met()
    print("Advice for A with all LTs met:")
    print(advice_for_A_with_all_LTs_met())
    # Print advice_for_A_without_all_LTs_met
    print("\n\nAdvice for A without all LTs met:")
    print(advice_for_A_without_all_LTs_met(
            extract_LT_list_by_score(2, dilbert, list_of_all_lts)))
    # Print advice_for_B_geq_90_pct
    print("\n\nAdvice for B with >= 90%")
    print(advice_for_B_geq_90_pct(
            extract_LT_list_by_score(3, bob, list_of_all_lts),
            extract_LT_list_by_score(4, bob, list_of_all_lts),
            len(list_of_all_lts)))
    # Other methods are similar; testing them is not a priority.
