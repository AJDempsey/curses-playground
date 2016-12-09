#! /usr/bin/python3

import sys
import curses
from curses import wrapper

from snippet import Snippet

def read_snippet_from_file(file_name):
    status = 1
    file_string = ""
    try:
        with open(file_name, "r") as f:
            file_string = f.read()
    except IOError as err:
        status = -1
        file_string = "{0}".format(err)
    return (status, file_string)

def user_loop(screen):
    test_snippet = Snippet(myscreen)
    test_snippet.update_screen()
    user_input = myscreen.getkey()
    while user_input != "\n":
        if user_input == "\t":
            test_snippet.move_to_next_edit_token()
        elif user_input == "KEY_BTAB":
            test_snippet.move_to_previous_edit_token()
        else:
            test_snippet.update_token_string(user_input)
        user_input = myscreen.getkey()

def main(myscreen):

    stdout_filename = open('debug.log', 'w')
    sys.stdout = stdout_filename

    curses.start_color()
    myscreen.clear()
    status, file_string = read_snippet_from_file("for-loop.snip")
    if status < 0:
        print("Problem reading the snippet")
        print(file_string)
        return
    working_list = file_string.split( "\n")
    line_num = 0
    if curses.has_colors():
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN) # Line is ok, passes validation?
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) # Line is not ok, doesn't pass validation?

    user_loop(myscreen, options, working_list)

    print(test_snippet)

if __name__ == '__main__':
    wrapper(main)
