# -*- coding: utf-8 -*-
"""
Matthew Dirks
MET CS 521
Due date: 10/19/2019
Final Project
Description: sbg_data_methods module.
This module contains some functions dealing with extracting and
interpreting data from data files.
"""

# import modules
import os


def no_taboos(string_to_check, verbose=False):
    '''
    This function makes sure a given string does not contain any substrings
    from a list of reserved strings.
    It returns True if the string is free of reserved strings.
    Otherwise, it returns False.
    If the argument verbose is set to True, it prints an error message.
    '''
    reserved = ['sid: ', 'lastname: ',
                'firstname: ', 'pronoun: ', 'scores: ']
    for taboo in reserved:
        if taboo in string_to_check:
            if verbose:
                print(f"Error: string cannot contain" +
                      "reserved substring '{taboo}'")
            return False
    return True


def fetch_data_from_file(filename):
    '''
    This function takes a string argument specifying a file name.
    It attempts to open that file. If successful, it returns
    a string holding the file's contents.
    Otherwise, it returns False.
    '''
    # Make sure file exists.
    if not(os.path.exists(filename)):
        print(f"Warning: invalid path {filename} or file does not exist.")
        return False
    elif not(os.path.isfile(filename)):
        print(f"Warning: path {filename} is not a file.")
        return False
    try:
        with open(filename, "r") as file:
            return file.read()
    except IOError:
        print(f"Warning: could not read file {filename}")
        return False


def str_to_list(string_rep_of_list):
    '''
    This function takes a list of floats that is stored as a string,
    e.g. "[2.5, 3, 4]"
    and returns the corresponding list (in our example, [2.5, 3, 4]"
    It also accepts lists with one or both of the brackets missing.
    '''
    entries = string_rep_of_list.split(",")
    # Remove '[' from first entry if present
    if entries[0][0] == '[':
        entries[0] = entries[0][1:]
    # Remove ']' from last entry if present
    if entries[-1][-1] == ']':
        entries[-1] = entries[-1][:-1]
    for index, entry in enumerate(entries):
        # If entry is a float, add it as a float.
        # Then convert to int if there is no tenths digit
        if (float(entry) * 10) % 10 == 0:
            entries[index] = int(float(entry))
        else:
            entries[index] = float(entry)
    return entries


def build_scores_dict_from_data(data_str):
    '''
    This function takes a string argument that has been read from a data file.
    It finds the dictionary of scores that is represented in that string
    and returns a dictionary built from that representation.
    The dictionary is assumed to have key-value pairs of the form
    {string, list_of_floats}
    '''
    scores_dict = {}
    dict_string = data_str.split("scores: ")[1].strip()
    # Remove '{' and '}' surrounding dict.
    assert dict_string[0] == '{' and dict_string[-1] == '}'
    dict_string = dict_string[1:-1]
    assert no_taboos(dict_string)  # Check for reserved strings
    # If dictionary is empty, return empty dictionary
    if dict_string.strip() == '':
        return {}
    # Otherwise, parse items
    # Create a list, items, whose entries are of the form
    # lt_label: [score1, score2, etc.]
    # For example:
    # ["'LT1A': [3, 4]", "'LT1B': [2, 3]", "'LT1C': [4]"]
    items = dict_string.split('],')
    for item in items:
        pair = item.strip().split(':')
        # Parse out the label and remove any quote marks bookending it.
        label = pair[0]
        if label[0] == "'" or label[0] == '"':
            label = label[1:]
        if label[-1] == "'" or label[-1] == '"':
            label = label[:-1]
        # Parse out the list of scores
        list_of_scores = str_to_list(pair[1].strip())
        # Add key-value pair (label, list_of_scores) to dictionary
        scores_dict[label] = list_of_scores
    return scores_dict


def write_student_data_to_file(student, filename):
    '''
    This function takes two arguments:
        (i) student, an object of the Student class,
        (ii) filename, a string,
    The function writes the return value of the Student's __str__ method
    to the specified data file.
    The function returns True on success, False on failure.
    '''
    # Make sure student data does not contain reserved substrings
    if not(student.all_strings_are_safe()):
        print("Error: student data contains reserved substrings.")
        print("Cancelling write.")
        return False
    # Attempt to open file in write mode; create if it doesn't exist yet
    try:
        with open(filename, "w+") as data_file:
            data_file.write(str(student))
            return True
    except IOError:
        print(f"Could not open file {filename} for writing.")
        return False


def write_lts_in_list_to_datafile(list_of_lts, filename):
    '''
    This function takes a list of LearningTarget objects
    and exports them to a data file.
    It takes two arguments:
        (i) a list of LearningTarget objects
        (ii) a string holding the filename of the datafile to write.
    It returns True on success, False on failure.
    '''
    # If no LTs, write an empty string to file.
    if bool(list_of_lts) is False:
        print("Warning: no LTs specified to write; creating blank file.")

    string_to_write = ""
    # Make sure LT descriptions do not contain ":::"
    if bool(list_of_lts):  # Code executes only if there are LTs present
        for lt in list_of_lts:
            if not(lt.all_strings_are_safe()):
                print("Error: at least one learning target contains " +
                      "the illegal combination ':::'.")
                print("Problem found in: " + str(lt))
                return False
            else:  # If LT strings are valid
                string_to_write += lt.string_for_datafile() + "\n"
    # Attempt to open file in write mode; create if it doesn't exist yet
    try:
        with open(filename, "w+") as data_file:
            data_file.write(string_to_write)
            return True
    except IOError:
        print(f"Could not open file {filename}.")
        return False
