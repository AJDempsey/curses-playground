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

def find_next_bound(line_list, bounding_char):
    y = 0
    x = 0
    for line in line_list:
        x = line.find(bounding_char)
        if x < 0:
            x = 0
        else:
            break
        y += 1
    return (y, x)


def main(myscreen):
    curses.start_color()
    myscreen.clear()
    status, file_string = read_snippet_from_file("for-loop.snip")
    if status < 0:
        print("Problem reading the snippet")
        print(file_string)
        return
    #myscreen.border(0)
    working_list = file_string.split( "\n")
    line_num = 0
    # Yellow is now gray, go figure
    curses.init_color(curses.COLOR_YELLOW, 240, 240, 240)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN) # Line is ok, passes validation?
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED) # Line is not ok, doesn't pass validation?
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW) # Highlight template to edit

    for line in working_list:
        myscreen.addstr(line_num, 0, line)
        line_num += 1
    y, x = find_next_bound(working_list, "<")
    end_y, end_x = find_next_bound(working_list, ">")

    overwrite_string = working_list[y][x:end_x+1]
    # Highlight the current template we're editing.
    myscreen.addnstr(y, x, overwrite_string, (end_x - x+1), curses.color_pair(curses.COLOR_YELLOW))
    myscreen.move(y, x)
    myscreen.refresh()
    myscreen.getch()

    curses.endwin()
    #print( str(y)+" "+str(x))
    #print( str(end_y)+" "+str(end_x))
    #print(overwrite_string)

if __name__ == '__main__':
    wrapper(main)
