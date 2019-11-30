# -*- coding: utf-8 -*-
"""
This module contains functions to read in a "user_prefs.txt" data file
and extract the relevant preferences.
"""

# Import modules
import sys

# Global variables
DEFAULT_FILENAME = "user_prefs.txt"

# Read data file
# Strip out comment lines
# Prompt user for login id.
# If login found, use that.
# Else prompt to create new user.
# Return a dictionary of username and prefs


def normalize_prefs_dict(prefs_dict):
    '''
    Make all keys in a given dict uppercase.
    '''
    prefs_dict = {k.upper(): v for k, v in prefs_dict.items()}
    return prefs_dict

def get_prefs_of_all_users(filename=DEFAULT_FILENAME):
    '''
    Read in a data file and get a list of user pref strings.
    Return that list.
    '''
    lines = []
    with open(filename, "r") as datafile:
        next_line = datafile.readline()
        while next_line:
            to_append = next_line.strip()
            if to_append[:5].upper() == 'USER=':
                lines.append(to_append)
            next_line = datafile.readline()
    return lines


def get_pref_val(prefs_string, pref):
    '''
    This function takes two strings:
        a preference string of the form
           'user=smithj,function=piecewise,d_is_valid=False,train_mode=True'
        and the label of a pref (e.g. 'function').
        It returns the value of that pref (e.g. 'piecewise')
        If the preference is not found, the function returns -1
    '''
    prefs_string = prefs_string.upper()
    search = pref.upper() + '='
    # If pref not found, return -1
    if prefs_string.find(search) == -1:
        return -1
    # Else, find pref value

    head = prefs_string[(prefs_string.find(search) + len(search)):]
    # Figure out index where pref ends: either next comma or end of string
    end = head.find(',')
    if end == -1:
        end = len(head)
    tail = head[:end]
    return tail


def get_username(prefs_string):
    '''
    This function takes a string of the form
    'user=smithj,function=piecewise,d_is_valid=False,train_mode=True'
    and returns the specified user.
    '''
    return get_pref_val(prefs_string, 'USER')


def get_list_of_users(list_of_user_prefs):
    '''
    This function takes a list of user pref strings
    (i.e. the output of get_prefs_of_all_users)
    and returns a list of usernames.
    '''
    user_list = []
    for pref_str in list_of_user_prefs:
        user_list.append(get_username(pref_str))
    return user_list


def get_bool_from_prefs_str(prefs_str, pref):
    '''
    This function takes a preferences string and a pref (e.g. 'd_is_valid')
    that should be bool.
    It returns the bool value or gives an error.
    If the preference is not found, the function returns -1.
    '''
    pref = pref.upper()
    prefs_str = prefs_str.upper()
    bool_str = get_pref_val(prefs_str, pref)
    if bool_str == -1:
        return -1
    else:
        bool_str = bool_str.upper().strip()
    if bool_str == 'TRUE':
        bool_val = True
    elif bool_str == 'FALSE':
        bool_val = False
    else:
        print(f"Error: invalid value for {pref} in")
        print(prefs_str)
        sys.exit()
    return bool_val


def get_prefs_dict(username, list_of_user_prefs):
    '''
    This function takes a username for a user whose prefs are in
    list_of_user_prefs. It returns a dict of those preferences and
    the username, e.g.
    {'user': 'smithj', 'function': 'sticky',
     'd_is_valid': True, 'train_mode': False}
    Default values if none specified:
        function = piecewise
        d_is_valid = True
        train_mode = True
    # TODO defaults
    '''
    # Make sure user name is in the given list
    username = username.upper()
    assert username in get_list_of_users(list_of_user_prefs)
    user_prefs_str = ''
    for prefs_str in list_of_user_prefs:
        if get_username(prefs_str).upper() == username:
            user_prefs_str = prefs_str
            break
    assert user_prefs_str  # This is False if user not found.

    prefs_dict = {}

    # Add user name to dict
    prefs_dict['USER'] = username
    # Add function to dict (value is String type) if found;
    # else default to piecewise
    function = get_pref_val(user_prefs_str, 'FUNCTION')
    if function == -1:  # pref not found; default to 'PIECEWISE'
        function = 'PIECEWISE'
    prefs_dict['FUNCTION'] = function
    # Add d_is_valid to dict (value is Bool type)
    d_is_valid = get_bool_from_prefs_str(user_prefs_str, 'D_IS_VALID')
    if d_is_valid == -1:  # pref not found; default to True
        d_is_valid = True
    prefs_dict['D_IS_VALID'] = d_is_valid
    # Add train_mode to dict
    train_mode = get_bool_from_prefs_str(user_prefs_str, 'TRAIN_MODE')
    if train_mode == -1:  # pref not found; default to True
        train_mode = True
    prefs_dict['TRAIN_MODE'] = train_mode
    return prefs_dict


def prefs_dict_to_prefs_str(prefs_dict):
    '''
    This function takes a prefs dict
    and converts it to a prefs string, which it returns.
    '''
    prefs_dict = normalize_prefs_dict(prefs_dict)
    user = prefs_dict['USER'].upper()
    function = prefs_dict['FUNCTION'].upper()
    d_is_valid = str(prefs_dict['D_IS_VALID']).upper()
    train_mode = str(prefs_dict['TRAIN_MODE']).upper()
    prefs_str = ("USER=" + user +
                 ",FUNCTION=" + function +
                 ",D_IS_VALID=" + d_is_valid +
                 ",TRAIN_MODE=" + train_mode +
                 "\n")
    return prefs_str


def update_prefs(prefs_dict, filename=DEFAULT_FILENAME):
    '''
    This function takes two arguments:
        (i) a dictionary of user prefs, e.g.:
            {'user': 'smithj', 'function': 'sticky',
             'd_is_valid': True, 'train_mode': False})
        (ii) a filename (optional).
    It looks for the user in the specified file.
    If present, it deletes that user.
    Then it appends the user with updated prefs to the end of the file.
    '''
    prefs_dict = normalize_prefs_dict(prefs_dict)
    search = 'USER=' + prefs_dict['USER']
    search = search.upper()
    line_num = -1
    user_already_present = False
    lines = []
    try:
        with open(filename, "r") as file:
            # Copy the file into memory
            lines = file.readlines()
            # Remove user if present
            for line_num, line in enumerate(lines):
                user_index = line.upper().find(search)
                comment_index = line.find('#')
            # Check if user occurs in line, not after comment
                print(f"Looking for '{search}' in '{line}'")
                print(f"index is {user_index}.")
                if user_index != -1:
                    # If the user is mentioned and line not commented out,
                    # replace the line with new prefs string
                    # and line is not commented out.
                    # Same thing if user is mentioned before a comment
                    # starts.
                    if comment_index == -1 or user_index < comment_index:
                        user_already_present = True
                        lines[line_num] = prefs_dict_to_prefs_str(prefs_dict)
    # If file doesn't exist, don't worry about reading it.
    except FileNotFoundError:
        pass

    # If user is not in file, append new line to end of list
    if user_already_present is False:
        lines.append(prefs_dict_to_prefs_str(prefs_dict).upper())

    # At this point, the user should be removed if relevant.
    # Replace old file text with contents of lines
    with open(filename, "w+") as file:
        print("Writing to file: \n" + '\n'.join(lines))
        file.writelines(lines)
        return True
    return False  # This should never run


def add_new_user_to_file(login_id="", filename=DEFAULT_FILENAME):
    '''
    This function takes a login id and a filename.
    It prompts the user to choose preferences,
    and then adds the new user to the file.

    TODO: If the user is already present in the file,
    it updates that user's prefs instead of appending a new line.

    The function returns a dict of the new user's preferences.
    e.g. :
    {'user': 'smithj', 'function': 'sticky',
     'd_is_valid': True, 'train_mode': False}
    '''
    # If no username passed as an argument, prompt for username.
    # In either case, add to file.
    if login_id == "":
        user = input("Please enter new username >")
    else:
        user = login_id.upper()
    prefs_dict = {"USER": user}
    # Get function
    print("Please specify overall grade function")
    valid_functions = ['SIMPLE', 'PIECEWISE', 'STICKY']
    function = 'invalid_choice'
    while function not in valid_functions:
        print("Valid choices are: " + str(valid_functions))
        function = input(" >").upper().strip()
    prefs_dict["FUNCTION"] = function
    # Is D valid?
    d_is_valid_str = 'invalid_choice'
    while d_is_valid_str not in ['Y', 'N']:
        d_is_valid_str = input("Is D a valid grade? (Y/N) >").strip().upper()
    d_is_valid = (d_is_valid_str == 'Y')
    prefs_dict["D_IS_VALID"] = d_is_valid
    # Train mode?
    train_mode_str = 'invalid_choice'
    while train_mode_str not in ['Y', 'N']:
        train_mode_str = \
            input("Use Synergy in training mode? (Y/N) > ").strip().upper()
    train_mode = (train_mode_str == 'Y')
    prefs_dict["TRAIN_MODE"] = train_mode

    # Having stored all the prefs, add user to file
    update_prefs(prefs_dict, filename)
    # prefs_str = prefs_dict_to_prefs_str(prefs_dict)
    # with open(filename, "a") as file:
    #    file.write('\n' + prefs_str)

    # Finally, return the prefs dict
    return prefs_dict


def login_prompt(filename=DEFAULT_FILENAME):
    '''
    This takes one argument, a filename for a file of user preferences.

    If more than one user is found in the data file,
    prompt user to enter district id.
    If that ID is found in the data file, return that user's prefs.
    Otherwise, prompt to create new user (or prompt to re-enter).

    This function returns a dict of preferences:
        e.g. :
    {'user': 'smithj', 'function': 'sticky',
     'd_is_valid': True, 'train_mode': False}
    '''
    user_prefs = get_prefs_of_all_users(filename)
    user_list = get_list_of_users(user_prefs)
    login_id = input("Please enter district username " +
                     "(e.g. smithj) >").strip().upper()
    if login_id in user_list:
        return get_prefs_dict(login_id, user_prefs)
    else:
        # Make sure user want a new id, and didn't just make a typo!
        print(f"User {login_id} does not have saved preferences.")
        choice = 'invalid_choice'
        while choice not in ['Y', 'N']:
            choice = input(f"Create new user '{login_id}' ? (Y/N) >").upper()
        # If user made a typo, just call this function again recursively.
        if choice == 'N':
            return login_prompt(filename)
        # Otherwise, prompt user for preferences, add user to file,
        # and return preference dict
        elif choice == 'Y':
            return add_new_user_to_file(login_id, filename)


# Unit tests
if __name__ == "__main__":
    print("Testing get_prefs_of_all_users():")
    user_prefs = get_prefs_of_all_users()
    print(user_prefs)
    input("Pausing for visual inspection.")

    print("Testing get_username():")
    assert get_username('user=bob, function=sticky') == 'BOB'
    print("Success!\n\n")

    print("Testing get_list_of_users():")
    print(get_list_of_users(user_prefs))
    input("Pausing for visual inspection.")

    print("Testing logn_prompt():")
    print(login_prompt())
    input("Pausing for visual inspection.")
    print("Testing add_new_user_to_file():")
    new_dict = add_new_user_to_file("smithj", "test_prefs.txt")
    print(new_dict)
    input("Pausing for visual inspection. Look at file 'test_prefs.txt'")

    print("\n\nTesting get_prefs_dict(username, list_of_user_prefs)")
    new_dict = get_prefs_dict('smithj',
                          ['user=smithj,' +
                           'function=sticky,d_is_valid=True,train_mode=False'])
    print(new_dict)
    assert new_dict['USER'] == 'SMITHJ'
    assert new_dict['FUNCTION'] == 'STICKY'
    assert new_dict['D_IS_VALID'] is True
    assert new_dict['TRAIN_MODE'] is False
    new_dict = get_prefs_dict('jonesb', ['user=jonesb'])
    # Test default values
    assert new_dict['FUNCTION'] == 'PIECEWISE'
    assert new_dict['D_IS_VALID'] is True
    assert new_dict['TRAIN_MODE'] is True
    print("Success!\n\n")
    # Test prefs update
    print("Testing update_prefs()")
    new_smithj_dict = {'USER': 'SMITHJ',
                       'FUNCTION': 'PIECEWISE',
                       'D_IS_VALID': False,
                       'TRAIN_MODE': True}
    assert update_prefs(new_smithj_dict, "test_prefs.txt")
    user_prefs = get_prefs_of_all_users('test_prefs.txt')
    smithj_prefs_from_file = get_prefs_dict('smithj', user_prefs)
    print("new_smithj_dict: " + str(new_smithj_dict))
    print("smithj_prefs_from_file: " + str(smithj_prefs_from_file))
    assert new_smithj_dict == smithj_prefs_from_file
    print("Success!\n\n")
