#! /usr/bin/python3

import curses
from curses import wrapper

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

def main(myscreen):
    myscreen.clear()
    status, file_string = read_snippet_from_file("for-loop.snip")
    if status < 0:
        print("Problem reading the snippet")
        print(file_string)
        return
    #myscreen.border(0)
    file_string_list = file_string.split( "\n")
    line_num = 0
    for line in file_string_list:
        myscreen.addstr(line_num, 0, line)
        line_num += 1
    myscreen.move(0,0)
    myscreen.refresh()
    myscreen.getch()

    curses.endwin()

if __name__ == '__main__':
    wrapper(main)
