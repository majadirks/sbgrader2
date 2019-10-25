# -*- coding: utf-8 -*-
"""
Matthew Dirks
MET CS 521
Due date: 10/19/2019
Final Project
Description: sbg_data_methods module.
This module contains functions dealing with the LearningTarget class
"""

# import modules
import sbg_data_methods as dm


class LearningTarget:
    '''
    Class to hold data about a learning target
    A Learning Target has three properties:
        lt_label, a string used to identify the LT (e.g. "LT1A")
        brief, a string containing a brief description of the LT
            (e.g. "Integer operations")
        description, a string containing a more explicti description of the LT
            (e.g. "I can add, subtract, multiply, and divide integers. I can
            model real-world situations and solve problems using those
            integer operations")
        gb_column, an int specifying the position of this LT in an online
            gradebook (such as Synergy). This is optional and defaults
            to the nonsensical -1.

    '''
    def __init__(self, lt_label,
                 brief="(no description)",
                 description="(no description)",
                 gb_column=-1):
        '''
        Constructor method
        '''
        self.lt_label = lt_label
        assert dm.no_taboos(self.lt_label)
        self.brief = brief
        assert dm.no_taboos(self.brief)
        self.description = description
        assert dm.no_taboos(self.description)
        self.gb_column = gb_column

    def __repr__(self):
        '''
        Method to return a string representing the LT. This uses
        the verbose description.
        '''
        return self.brief_string()

    def __eq__(self, other):
        '''
        Method to check whether this LT equals another.
        '''
        if isinstance(other, LearningTarget):
            return self.brief_string().strip() == \
                other.brief_string().strip() and\
                self.description.strip() == other.description.strip()
        return False

    def brief_string(self):
        '''
        This function returns a string with the LT label and brief description,
        separated by a colon.
        '''
        return self.lt_label + ": " + self.brief.strip()

    def set_brief(self, brief):
        '''
        Setter method for brief description. Returns the updated
        LearningTarget object.
        '''
        self.brief = brief.strip()
        return self

    def string_for_datafile(self):
        '''
        This function returns a string that represents LT data as it will
        be stored in a data file. That is, it returns a string of the form:
            lt_label:::brief_description:::verbose_description
        '''
        return self.lt_label + ":::" + self.brief + ":::" + self.description

    def all_strings_are_safe(self):
        '''
        This function returns False if any of any of the object's
        strings (lt_label, __brief, or description) contain ':::',
        and returns True otherwise.
        '''
        return not (':::' in self.lt_label + self.brief + self.description)


def lt_with_label(search, list_of_lts):
    '''
    This function takes two arguments:
        (i) a string, and
        (ii) a list of LearningTarget objects.
    It returns a LearningTarget object from the list whose label is equal to
    the string. If no corresponding LearningTarget is found,
    the function returns false.
    '''
    for lt in list_of_lts:
        if lt.lt_label == search:
            return lt
    return False


def build_lt_list_from_data(data_str):
    '''
    This function takes a string argument that has been read from a data file.
    It returns a list of LearningTarget objects found in the file.
    The file should be formatted as follows:
        *Each learning target on its own line
        *Each line in the format:
            lt_label:::brief_description:::verbose_description
    '''
    lt_list = []  # Initialize empty list
    # Create a list whose members are the lines in the file
    lines = data_str.split("\n")
    # Parse each line for LT label and descriptions
    for line in lines:
        # Skip any empty lines
        if line.strip() == "":
            continue
        # Break each line at ':::'
        parts = line.split(":::")
        part_count = len(parts)
        assert len(parts) >= 1  # We should have at least one part!
        # Create new learning target with specified label
        lt_label = parts[0]
        new_lt = LearningTarget(lt_label)
        if part_count >= 2:
            new_lt = new_lt.set_brief(parts[1])
        if part_count >= 3:
            new_lt.description = parts[2]
        lt_list.append(new_lt)
    return lt_list


def build_lt_list_from_datafile(filename):
    '''
    This function takes a filename (string). It reads in learning target
    information and returns a list of LearningTarget objects.
    If the LT list cannot be built, this function returns an empty list.
    '''
    data_str = dm.fetch_data_from_file(filename)
    if (data_str):  # True if data fetched successfully, False otherwise
        return build_lt_list_from_data(data_str)
    else:
        return []


def rows_of_lt_briefs(lt_list):
    '''
    This function takes a list of LearningTarget objects.
    It returns a string containing the LT label and brief description
    for each item in the list, each on a new line.
    '''
    str_list = []
    # If lt_list is False, there are no LTs; return an empty string
    if bool(lt_list) is False:
        return ''
    for lt in lt_list:
        str_list.append(lt.brief_string())
    # Sort list, join with newlines, and return
    return ("\n".join(sorted(str_list)))


def find_lt_by_column(search, list_of_lts):
    '''
    This function returns the LearningTarget in list_of_lts
    with gb_column equal to search (an int).
    If no LTs or multiple LTs are found with that value,
    the function returns False.
    '''
    match_count = 0
    for lt in list_of_lts:
        if lt.gb_column == search:
            match_count += 1
            if match_count > 1:
                print("Warning: " +
                      f"multiple LTs found with gb_column == {search}")
                return False
            else:
                first_found_match = lt
    if match_count == 0:
        # print(f"Warning: no LTs found with gb_column == {search}")
        return False
    return first_found_match


# Unit tests
if __name__ == "__main__":
    # import some data
    import data_for_unit_testing as dfut
    list_of_all_lts = dfut.sample_list_of_lts()

    # Test __init__() method
    print("Testing __init__():")
    lt_label = 'Test LT'
    lt_brief = 'this is brief'
    lt_desc = 'this is verbose'
    test_lt = LearningTarget(lt_label, lt_brief, lt_desc)
    assert type(test_lt) == LearningTarget
    # Check the LearningTarget attributes: lt_label, __brief, and description.
    assert test_lt.lt_label == lt_label
    assert test_lt.brief == lt_brief
    assert test_lt.description == lt_desc
    assert test_lt.gb_column == -1
    print("Success!")
    # Test __repr__() method
    print("Testing __repr__():")
    assert test_lt.__repr__() == lt_label + ': ' + lt_brief
    print("Success!")
    # Test __eq__() method
    print("Testing __eq__():")
    other_lt = LearningTarget(lt_label, lt_brief, lt_desc)
    assert test_lt == other_lt
    # Mess with white space.
    other_lt = LearningTarget(lt_label, lt_brief + "   ", "\n  " + lt_desc)
    assert test_lt == other_lt
    yet_another_lt = LearningTarget('Another test LT')
    assert test_lt != yet_another_lt
    print("Success!")
    # Test brief_string()
    print("Testing brief_string():")
    assert test_lt.brief_string() == lt_label + ': ' + lt_brief
    print("Success!")
    # Test set_brief()
    print("Testing set_brief():")
    test_lt.set_brief("new brief")
    print(test_lt.brief_string())
    assert test_lt.brief_string() == "Test LT: new brief"
    print("Success!")
    # Test string_for_datafile()
    print("Testing string_for_datafile():")
    assert test_lt.string_for_datafile() == \
        "Test LT:::new brief:::this is verbose"
    print("Success!")
    # Test all_strings_are_safe()
    print("Testing all_strings_are_safe():")
    assert test_lt.all_strings_are_safe
    assert not(LearningTarget("Bad:::Bad").all_strings_are_safe())
    assert not(LearningTarget("Okay", "Bad:::Bad").all_strings_are_safe())
    assert not(LearningTarget("OK", "OK", "Bad:::Bad").all_strings_are_safe())
    print("Success!")
    # Test lt_with_label
    print("Testing lt_with_label():")
    assert lt_with_label('LT01', list_of_all_lts) == list_of_all_lts[0]
    assert lt_with_label('LT02', list_of_all_lts) != list_of_all_lts[0]
    assert lt_with_label('Invalid Label', list_of_all_lts) is False
    print("Success!")
    # Test build_lt_list_from_data
    print("Testing build_lt_list_from_data():")
    # Check case where all data is provided
    alpha_lts = build_lt_list_from_data("A:::B:::C\nD:::E:::F")
    assert len(alpha_lts) == 2
    assert alpha_lts[0] == LearningTarget('A', 'B', 'C')
    assert alpha_lts[1] == LearningTarget('D', 'E', 'F')
    # Check case where some data is missing or extraneous
    defective_lts = build_lt_list_from_data(
            "A\nD:::E:::F\nG:::H\nI:::J:::K:::L")
    assert defective_lts[0] == LearningTarget('A')
    assert defective_lts[1] == LearningTarget('D', 'E', 'F')
    assert defective_lts[2] == LearningTarget('G', 'H')
    # On this last LT, the 'L' should be discarded
    assert defective_lts[3] == LearningTarget('I', 'J', 'K')
    # Check that no data -> empty list
    assert build_lt_list_from_data("") == []
    print("Success!")
    # Test build_lt_list_from_datafile
    print("Testing build_lt_list_from_datafile():")
    dm.write_lts_in_list_to_datafile(alpha_lts, "alpha_lts.ltdat")
    alpha_lts_2 = build_lt_list_from_datafile("alpha_lts.ltdat")
    assert alpha_lts == alpha_lts_2
    print("Success!")
    # Test def rows_of_lt_briefs()
    print("Testing def rows_of_lt_briefs():")
    lt_abc = alpha_lts[0]  # LT containing 'A', 'B', 'C'
    lt_def = alpha_lts[1]  # LT containing 'D', 'E', 'F'
    assert rows_of_lt_briefs(alpha_lts) == (lt_abc.brief_string() +
                                            '\n' + lt_def.brief_string())
    print("Success!\n\n")
    print("All tests were successful.")
    print("I created the extra file 'alpha_lts.ltdat', " +
          "which you may want to delete.")