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

"""
def get_lines(filename="user_prefs.txt"):
    '''
    DEPRECATED: This function isn't needed.
    Read in a data file and get a list of lines.
    Ignore any lines that start with '#'
    Return that list.
    '''
    lines = []
    with open(filename, "r") as datafile:
        next_line = datafile.readline()
        while next_line:
            to_append = next_line.strip()
            # Ignore any comment lines or blank lines
            # The order for the 'or' is important:
            # first check for blank line, or else to_append[0] could
            # cause an error.
            if to_append == '' or to_append[0] == '#':
                next_line = datafile.readline()
                continue
            lines.append(to_append)
            next_line = datafile.readline()
    return lines
"""


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
    '''
    prefs_string = prefs_string.upper()
    search = pref.upper() + '='
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
    '''
    pref = pref.upper()
    prefs_str = prefs_str.upper()
    bool_str = get_pref_val(prefs_str, pref).strip()
    if bool_str == 'TRUE':
        bool_val = True
    elif bool_str == 'FALSE':
        bool_val = False
    else:
        print(f"Error: invalid value for {pref} in")
        print(prefs_str)
        sys.exit()
    return bool_val


def prefs_dict(username, list_of_user_prefs):
    '''
    This function takes a username for a user whose prefs are in
    list_of_user_prefs. It returns a dict of those preferences and
    the username, e.g.
    {'user': 'smithj', 'function': 'sticky',
     'd_is_valid': True, 'train_mode': False}
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
    # Add function to dict (value is String type)
    prefs_dict['FUNCTION'] = get_pref_val(user_prefs_str, 'FUNCTION')
    # Add d_is_valid to dict (value is Bool type)
    prefs_dict['D_IS_VALID'] = get_bool_from_prefs_str(user_prefs_str,
                                                       'D_IS_VALID')
    # Add train_mode to dict
    prefs_dict['TRAIN_MODE'] = get_bool_from_prefs_str(user_prefs_str,
                                                       'TRAIN_MODE')
    return prefs_dict

  
def add_new_user_to_file(login_id, filename=DEFAULT_FILENAME):
    '''
    This function takes a login id and a filename.
    It prompts the user to choose preferences,
    and then adds the new user to the file.
    The function returns a dict of the new user's preferences.
    e.g. :
    {'user': 'smithj', 'function': 'sticky',
     'd_is_valid': True, 'train_mode': False}
    '''
    # Get user name
    user = input("Please enter new username >")
    # Get function
    print("Please specify overall grade function")
    valid_functions = ['SIMPLE', 'PIECEWISE', 'STICKY']
    function = 'invalid_choice'
    while function not in valid_functions:
        print("Valid choices are: " + str(valid_functions))
        function = input(" >").upper().strip()
    # Is D valid?
    d_is_valid_str = 'invalid_choice'
    while d_is_valid_str not in ['Y', 'N']:
        d_is_valid_str = input("Is D a valid grade? (Y/N) >").strip().upper()
    d_is_valid = (d_is_valid_str == 'Y')
    # Train mode?
    # TODO


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
        return prefs_dict(login_id, user_prefs)
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
if __name__=="__main__":
    print("Testing get_prefs_of_all_users():")
    user_prefs = get_prefs_of_all_users()
    print(user_prefs)
    input("Pausing for visual inspection.")

    
    print("Testing get_username():")
    assert get_username('user=bob, function=sticky') == 'BOB'
    print("Success.")
    
    print("Testing get_list_of_users():")
    print(get_list_of_users(user_prefs))
    input("Pausing for visual inspection.")

    print("Testing logn_prompt():")
    print(login_prompt())
    input("Pausing for visual inspection.")