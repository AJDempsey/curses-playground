#! /usr/bin/python3

import sys
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
    y, x = curses.getsyx()
    cursor_x = x
    if y > len(line_list):
        return y, x
    for line in line_list[y:]:
        print("y: "+str(y)+" x: "+str(x)+" bounding char is "+bounding_char)
        if x > len(line):
            x = 0
        x = line.find(bounding_char, x)
        if x == cursor_x:
            x = line.find(bounding_char, x+1)
        print("Found "+bounding_char+" at y "+str(y)+" x "+str(x))
        if x < 0:
            x = 0
        else:
            break
        y += 1
    return (y, x)

def highlight_next_template(screen, options, working_list):
    y, x = find_next_bound(working_list, "<")
    screen.move(y, x)
    screen.refresh()
    end_y, end_x = find_next_bound(working_list, ">")

    if y >= len(working_list) or end_x + 1 > len(working_list[y]):
        return y, x
    overwrite_string = working_list[y][x:end_x+1]
    # Highlight the current template we're editing.
    screen.addnstr(y, x, overwrite_string, (end_x - x+1), curses.color_pair(curses.COLOR_YELLOW))
    screen.move(y, x)
    win = options['win']
    win.mvwin(y, x)
    screen.refresh()
    win.refresh()

def user_loop(screen, options, working_list):
    next_char = screen.getkey()

    while next_char != "\n":
        # Build the text string using new characters
        string = options['txt']
        string = string + next_char
        print("Next char: "+next_char)

        # A <tab> is used to move to the next template
        if next_char == "\t":
            highlight_next_template(screen, options, working_list)

        # Otherwise we refresh the window with the text
        else:
            win = options['win']
            win.addnstr(0, 0, string, len(string))
            win.refresh()
            screen.refresh()
            options['txt'] = string
            next_char = screen.getkey()

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

    # Create the options window
    win = curses.newwin(6, 6, 1, 10)
    options = {}
    options['win'] = win
    options['txt'] = ''

    highlight_next_template(myscreen, options, working_list)
    user_loop(myscreen, options, working_list)
    curses.endwin()
    #print( str(y)+" "+str(x))
    #print( str(end_y)+" "+str(end_x))
    #print(overwrite_string)

if __name__ == '__main__':
    wrapper(main)
