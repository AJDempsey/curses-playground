#! /usr/bin/python3
"""
An example of how to use a snippet class to provide structure for cli commands
that code can be added to,

Copyright (c) 2016 Anthony Dempsey, Colin Docherty
"""

import sys
import curses
from curses import wrapper
import time
import threading
import argparse

import tool_tip
from snippet import Snippet

def read_snippet_from_file(file_name):
    """
    Read user snippet from file.
    """
    status = 1
    file_string = ""
    try:
        with open(file_name, "r") as file_handle:
            file_string = file_handle.read()
    except IOError as err:
        status = -1
        file_string = "{0}".format(err)
    return (status, file_string)

def display_tool_tip(tool_tip_window, main_window):
    """
    Activate the tool tip, replace it if one already exists.
    """
    time.sleep(2)
    tool_tip_window.deactivate()
    main_window.remove_error_tool_tip()
    del tool_tip_window
    main_window.update_screen()

def user_loop(screen, tool_tip_thread):
    """
    This function is where most of the work happens. This is where all the user input is processed.
    """
    test_snippet = Snippet(screen)
    test_snippet.update_screen()
    user_input = screen.getkey()
    while user_input != "\n":
        if user_input == "\t":
            test_snippet.move_to_next_edit_token()
        elif user_input == "KEY_BTAB":
            test_snippet.move_to_previous_edit_token()
        elif user_input == "KEY_IC":
            test_snippet.insert_new_edit_token()
        elif user_input[:3] == "KEY" and user_input != "KEY_BACKSPACE":
            tool_tip_string = "Key stroke {} not recognized".format(user_input)
            # We don't need the x variable of the screen size, so ignore it.
            y_coord, _ = screen.getmaxyx()
            tt_instance = tool_tip.Tool_tip(y_coord -1, 0, 1, len(tool_tip_string)+1)
            tt_instance.add_to_window(tool_tip_string)
            tt_instance.activate()
            tool_tip_thread = threading.Thread(target=display_tool_tip,\
                    args=(tt_instance, test_snippet))
            tool_tip_thread.start()
            test_snippet.add_error_tool_tip(tt_instance)
            test_snippet.update_screen()
        else:
            test_snippet.update_token_string(user_input)
        user_input = screen.getkey()
    print(test_snippet)

def main(myscreen, tool_tip_thread, snippet_file):
    """
    Main function to initialise curses and call the user function.
    """

    stdout_filename = open('debug.log', 'w')
    sys.stdout = stdout_filename

    curses.start_color()
    myscreen.clear()
    status = 0
    if snippet_file is not None:
        status, file_string = read_snippet_from_file(snippet_file)
    if status < 0:
        print("Problem reading the snippet")
        print(file_string)
        return
    if curses.has_colors():
        # Line is ok, passes validation?
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        # Line is not ok, doesn't pass validation?
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)

    user_loop(myscreen, tool_tip_thread)

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description=\
        "Example program showing how to use a snippet.\n"+\
        "Navigating a snippet is easy:\n"+\
        "Tab - Move to next editable template.\n"+\
        "Shift + Tab - Move to previous editable template.\n"+\
        "Insert - Add new editable token under the current line.\n"+\
        "Enter - Execute the snippet as it currently exists and exit.",\
        formatter_class=argparse.RawTextHelpFormatter)
    PARSER.add_argument("--snippet-file")
    ARGS = PARSER.parse_args()
    TOOL_TIP_THREAD = None
    if ARGS.snippet_file is None:
        print("No snippet file given, exiting.")
        exit()
    wrapper(main, TOOL_TIP_THREAD, ARGS.snippet_file)
    if TOOL_TIP_THREAD is not None:
        TOOL_TIP_THREAD.join()
