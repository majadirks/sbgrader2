# -*- coding: utf-8 -*-
"""
Matthew Dirks
MET CS 521
Due date: 10/19/2019
Final Project
Description: This program calculates student grades under a Standards-Based
system and generates grade reports.
This module loads dummy data and displays a user interface
to interact with the data.
"""

# Import modules
import simple_interface as si

# Main code: run an interface.
if __name__ == "__main__":
    cp = si.load_sample_classperiod()
    si.main_menu(cp)
