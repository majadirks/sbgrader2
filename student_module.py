# -*- coding: utf-8 -*-
"""
Matthew Dirks
MET CS 521
Due date: 10/19/2019
Final Project
Description: sbg_data_methods module.
This module contains function dealing with the Student data type.
"""

# Import modules
import nitty_gritty_of_grading as ngog
import sbg_data_methods as dm
import lt_module as ltm
import advice
import datetime
from math import floor


class Student:
    '''
    Class to hold data about a student.
    Specifically: student ID number, last name, first name,
    preferred pronoun, and scores
    '''
    def __init__(self, sid, lastname, firstname, pronoun="they"):
        '''
        Constructor method
        '''
        self.sid = sid  # Student ID number
        self.lastname = lastname
        assert dm.no_taboos(self.lastname)
        self.firstname = firstname
        assert dm.no_taboos(self.firstname)
        # self.pronoun is the student's preferred pronoun.
        # If set to 'NONE', program should display student's full name
        # and avoid pronouns entirely.
        self.pronoun = pronoun
        assert dm.no_taboos(self.pronoun)
        self.scores = {}

    def all_strings_are_safe(self):
        '''
        This method makes sure that none of the strings stored by this class
        contain reserved substrings.
        '''
        all_safe = dm.no_taboos(self.lastname) and\
            dm.no_taboos(self.firstname) and dm.no_taboos(self.pronoun)
        return all_safe

    def __repr__(self):
        '''
        Method that returns a string representation of student data.
        '''
        strs_to_display = [f"sid: {self.sid}",
                           f"lastname: {self.lastname}",
                           f"firstname: {self.firstname}",
                           f"pronoun: {self.pronoun}",
                           f"scores: {self.scores}"]

        if not(self.all_strings_are_safe()):
            strs_to_display.append("\n\nWARNING: Reserved substring found.")
        return ", ".join(strs_to_display)

    def __eq__(self, other):
        '''
        Method that checks whether two students have the same student ID
        and returns the result
        '''
        if isinstance(other, Student):
            return self.sid == other.sid
        return False

    def name_str(self):
        '''
        This function returns a student's name in the format
        Firstname Lastname
        '''
        return self.firstname + ' ' + self.lastname

    def calculate_piecewise_grade(self):
        '''
        This method uses the ngog module to calculate the student's
        overall grade.
        '''
        return ngog.piecewise_grade(
                ngog.list_of_most_recent_scores(self.scores))

    def letter_grade(self):
        '''
        This method uses the ngog module to calculate the student's
        letter grade.
        '''
        return ngog.letter_grade(
                ngog.list_of_most_recent_scores(self.scores))

    def lts_assessed(self, list_of_all_LTs):
        '''
        This method takes a list of all learning targets in the
        gradebook (a list of LearningTarget objects).
        The student has been assessed on some subset of those, but may
        not have been assessed on all of them (e.g. due to absences or
        because the teacher excused the LT for some reason).
        This function returns a list of LearningTarget objects
        for which the student has a corresponding score.
        '''
        lts_assessed = []
        for lt_label in self.scores:
            search = ltm.lt_with_label(lt_label, list_of_all_LTs)
            # Make sure that an LT with the given label is in the
            # list of LTs, and throw an error if not.
            if not(search in list_of_all_LTs):
                error_str = ("Error: Learning Target " +
                             lt_label + " not found!")
                assert False, error_str
            # If that error wasn't raised, add this LT object to the list
            lts_assessed.append(search)
        return lts_assessed

    def __best_advice(self, list_of_all_lts):
        '''
        Obligatory private method for project requirements.

        This method returns a string containg study advice for the student.
        It requires one argument: a list of all LearningTargets
        in the gradebook.
        '''
        # Store misc. data needed to generate advice strings
        lts_assessed = self.lts_assessed(list_of_all_lts)
        most_recent_scores = ngog.list_of_most_recent_scores(self.scores)
        pct_met = ngog.pct_of_lts_met(most_recent_scores)
        has_A = ngog.has_A_from_LTs(most_recent_scores)
        has_B = ngog.has_B_from_LTs(most_recent_scores)
        has_C = ngog.has_C_from_LTs(most_recent_scores)
        has_D = ngog.has_D_from_LTs(most_recent_scores)
        has_F = ngog.has_F_from_LTs(most_recent_scores)
        list_of_0s = advice.extract_LT_list_by_score(0, self, lts_assessed)
        list_of_1s = advice.extract_LT_list_by_score(1, self, lts_assessed)
        list_of_0s_and_1s = list_of_0s + list_of_1s
        list_of_2s = advice.extract_LT_list_by_score(2, self, lts_assessed)
        list_of_0s_1s_and_2s = list_of_0s_and_1s + list_of_2s
        list_of_3s = advice.extract_LT_list_by_score(3, self, lts_assessed)
        list_of_4s = advice.extract_LT_list_by_score(4, self, lts_assessed)
        count_of_4s = len(list_of_4s)
        total_lt_count = len(lts_assessed)

        if has_A:
            if pct_met == 1:  # Case 1: Student has A; all LTs met
                return advice.advice_for_A_with_all_LTs_met()
            else:  # Case 2: Student has A; not all LTs met
                return advice.advice_for_A_without_all_LTs_met(
                    list_of_0s_1s_and_2s)
        elif has_B:
            if pct_met >= 0.9:  # Case 3: Student has B; more than 90% met
                return advice.advice_for_B_geq_90_pct(list_of_3s,
                                                      count_of_4s,
                                                      total_lt_count)
            else:  # Case 4: Student has B; 89% or below
                return advice.advice_for_B_under_90(list_of_2s,
                                                    list_of_3s,
                                                    count_of_4s,
                                                    total_lt_count)
        elif has_C:
            if pct_met >= 0.8:  # Case 5: Student has C; over 80% met
                return advice.advice_for_C_geq_80(list_of_0s_and_1s)
            else:  # Case 6: Student has C; 79% or below met
                return advice.advice_for_C_under_80(list_of_0s_1s_and_2s,
                                                    total_lt_count)
        elif has_D:  # Case 7: Student has a D
            return advice.advice_for_D(list_of_0s_1s_and_2s, total_lt_count)
        elif has_F:
            # Case 8: student has taken assessments and has F
            if total_lt_count > 0:
                return advice.advice_for_F(list_of_0s_1s_and_2s,
                                           total_lt_count)
            # Case 9: student has F and has taken no assessments
            elif total_lt_count == 0:
                return advice.advice_when_no_LTs_in_gradebook()
        else:  # This should never happen
            return ("Error: invalid grade calculation occurred; " +
                    "no advice given.")

    def report(self, list_of_all_lts):
        '''
        This function takes as an argument a list of LearningTarget
        objects, containing at minimum the LTs on which the student
        has been assessed.
        This function returns a string representing a grade report
        for a student.
        '''
        current_date_str = str(datetime.datetime.now()).split(' ')[0]
        pseudo_pct = floor(self.calculate_piecewise_grade() * 100)
        lines = [
                f"Grade Report for {self.firstname} {self.lastname}" +
                f"\t{current_date_str}",
                f"\nOverall grade: {self.letter_grade()} " +
                f"({pseudo_pct}%)\n",
                "Learning Target Scores:"]
        for lt in self.lts_assessed(list_of_all_lts):
            # Create a line for most recent score on this LT
            lt_brief = "{:.<70}".format(lt.brief_string())
            scores_on_lt = self.scores[lt.lt_label]
            recent_score = scores_on_lt[-1]
            old_scores = scores_on_lt[:-1]
            next_line = lt_brief + "  " + str(recent_score)
            lines.append(next_line)
            # If student had previous assessment attempts, add those
            # on a new line
            if len(old_scores) > 0:
                lines.append("\tPrevious scores: " + str(old_scores))
        lines.append("\n")
        lines.append("Advice for study plan:\n")
        lines.append(self.__best_advice(list_of_all_lts))
        lines.append("\n\nStudent Signature: ___________________________")
        lines.append("\n\nParent Signature: ___________________________")
        return "\n".join(lines)


def make_scoreless_student_from_data(data_str):
    '''
    This function takes a string argument that has been read from a data file.
    It looks for a student ID number, last name, first name, and pronoun,
    and uses that data to create a Student object, which it returns.
    The returned student is initialized without any learning target scores.
    The function returns False on an error.
    '''
    data_list = data_str.split(",")
    for entry in data_list:
        # We're looking for entries of the form 'heading: value'
        # (e.g. 'sid: 101', 'lastname: Smith')
        # Skip any entries that don't have colons,
        # and skip the entry introducing the scores dictionary
        if 'scores: ' in entry or ':' not in entry:
            continue
        # Only look at entries that contain specified keywords
        # This is the unusual case where the code actually expects
        # the "taboos" to be present!
        if dm.no_taboos(entry):
            continue
        # Find the first colon and use it to parse out
        # heading from value.
        split_index = entry.index(':')
        heading = entry[:split_index].strip().lower()
        value = entry[split_index + 1:].strip()
        assert dm.no_taboos(value)
        # Interpret the values for headings that we want.
        if heading == 'sid':
            sid = int(value)
        elif heading == 'lastname':
            lastname = value
        elif heading == 'firstname':
            firstname = value
        elif heading == 'pronoun':
            pronoun = value
    # Having completed the for loop, we will create and return the student.
    try:
        new_student = Student(sid, lastname, firstname, pronoun)
    except UnboundLocalError:
        print(f"UnboundLocalError: data file is missing crucial student data.")
        return False
    return new_student


def make_student_from_datafile(filename):
    '''
    This function takes a filename (string). It reads in student
    data and scores from a data file and builds a Student object
    with that data, which it returns.
    '''
    data_str = dm.fetch_data_from_file(filename)
    assert data_str  # True if data fetched successfully, False otherwise
    new_student = make_scoreless_student_from_data(data_str)
    assert new_student  # True if student made successfully, False otherwise
    new_student.scores = dm.build_scores_dict_from_data(data_str)
    return new_student


def update_grade(student, lt_label, new_score):
    '''
    This function takes three arguments:
        student, and object of the Student class;
        lt_label, a string (e.g. "LT01"); and
        new_score, the student's most recent score for the specified
        learning target.
    It modifies the student's grades to incorporate the new score.
    It returns the updated Student object.
    '''
    assert ngog.score_is_valid(new_score)  # Make sure score is valid
    # Look in scores dictionary for the lt label (key).
    # If it's already there, append the new score to the list (value).
    # Otherwise, create it
    if lt_label in student.scores:
        student.scores[lt_label].append(new_score)
    else:
        student.scores[lt_label] = [new_score]
    return student


def fix_grade_history(student, lt_label, score_history):
    '''
    This function takes three arguments:
        student, an object of the Student class;
        lt_label, a string (e.g. "LT01"); and
        score_history, a list of scores.
    It replaces the student's grades for the specified LT
    with the new list.
    It returns the updated student object
    '''
    assert ngog.list_is_valid(score_history)
    student.scores[lt_label] = score_history
    return student


def add_lt(student, lt_label, score):
    '''
    This function takes three arguments:
        student, an object of the Student class;
        lt_label, a string (e.g. "LT01"); and
        score, a float representing the student's score.
    It adds the new learning target and score to the student's grades
    and returns the Student object.

    If the learning target is already in the dictionary,
    this function raises an assertion error.
    '''
    assert ngog.score_is_valid(score)  # Make sure score is valid
    # Make sure LT is not already in dict
    assert not(lt_label in student.scores)
    # Make sure lt label doesn't contain reserved strings
    assert dm.no_taboos(lt_label)
    student.scores[lt_label] = [score]  # Add new LT and score
    return student


def remove_lt(student, lt_label):
    '''
    This function takes a Student object and a learing target label (string).
    It removes that learning target from the student's scores
    and then returns the updated Student object.
    The function raises an assertion error if the learning target
    is not in the student's scores.
    '''
    assert lt_label in student.scores
    student.scores.pop(lt_label)
    return student

def remove_everything_between_parens(string_to_clean):
    '''
    This function takes a string input and returns the same string
    but with all characters between parentheses removed, as well as
    the parentheses themselves.
    If there is an open paren with no closing paren, everything after
    the opening paren is removed.
    If there is a closing paren without an opening paren,
    it is removed.
    The string is stripped of leading/trailing whitespace and then
    returned.
    Examples:
        'hello (world) of mine' -> 'hello  of mine'
                        (two spaces between 'hello' and 'of'!)
        'hello (world)' -> 'hello'
        'hello (world' -> 'hello'
        'hello )world' -> 'hello world'
        'well )hello there( world' -> 'well hello there'
    '''
    # TODO
    pass


def parse_score_history_from_comment(comment):
    '''
    This function takes a string (a comment in a gradebook)
    and returns a list of the student's score history.
    Comments may contain previous scores in in the following formats:
        'Previous scores: 1, 2.5, 3'
        'Previous scores: 1 2.5 3'
        'Previous scores: 1 (5/28 - try again!), 2.5 3'
    'Previous scores: 1 (5/28), 2.5 (6/1 - getting there!!!), 3 Good job :)'
        'Previous: 1, 2.5, 3'
        Program will look for 'Previous scores:' or 'Previous:',
        and then try to parse scores.
        It will ignore anything in parentheses. Commas and/or spaces
        separate scores. If it encounters an invalid character outside of
        parentheses, it assumes the score list is over.
    If no starting phrase ('Previous scores:' or 'Previous:') is found,
    the function returns an empty list. Otherwise, it returns
    a list of the scores.
    Starting phrases are not case sensitive.
    '''
    comment = comment.upper()
    starting_phrases = ['PREVIOUS SCORE:',
                        'PREVIOUS SCORES:',
                        'PREVIOUS:',
                        'PAST SCORE:',
                        'PAST SCORES:',
                        'OLD SCORE:',
                        'OLD SCORES:',
                        ]
    phrase_index = -1  # Initialize as nonsense
    phrase_len = 0  # length of phrase
    for phrase in starting_phrases:
        if phrase in comment:
            phrase_index = comment.find(phrase)
            phrase_len = len(phrase)
            break
    if phrase_index == -1:  # If phrase not found
        return []
    # Remove starting phrase and everything before it
    comment = comment[phrase_index + phrase_len:]
    # Remove everything between parentheses.
    # TODO
    pass


# Unit tests
if __name__ == "__main__":
    # Test remove_everything_between_parens
    print("Testing remove_everything_between_parens():")
    assert remove_everything_between_parens(
            'hello (world) of mine') == 'hello  of mine'  # NB: Two spaces
    assert remove_everything_between_parens(
            'hello (world)') == 'hello'
    assert remove_everything_between_parens(
            'hello (world of mine') == 'hello'  # Missing closing paren
    # Ignore and remove closing paren that has no opening paren
    assert remove_everything_between_parens(
            'hello) world') == 'hello world'
    assert remove_everything_between_parens(
            'well )hello there( world') == 'well hello there'

    # Test parse_score_history_from_comment
    print("Testing parse_score_history_from_comment()")
    assert parse_score_history_from_comment("no comment") == []
    assert parse_score_history_from_comment(
            "yadayadayada PREVIOUS SCORES: 1, 2.5, 3") == [1, 2.5, 3]
    assert parse_score_history_from_comment(
            'previous scores: 1 2.5 3') == [1, 2.5, 3]
    assert parse_score_history_from_comment(
            "Previous scores: 1 (5/28), 2.5 (6/1 - getting there!!!), " +
            "3 Good job :)") == [1, 2.5, 3]
    assert parse_score_history_from_comment(
            "Previous: 1 2.5 3") == [1, 2.5, 3]
    # Test with mismatched parentheses
    assert parse_score_history_from_comment("Previous: 1, (2, 3") == [1]

    # Print final success message
    print("All tests passed successfully!")