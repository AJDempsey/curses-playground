#! /usr/bin/python3

import curses
from curses import wrapper

TAB_WIDTH = 8

def main(myscreen):
    myscreen.clear()
    
    #myscreen.border(0)
    myscreen.addstr(12, 0, "Python curses in action!")
    myscreen.addstr(13, TAB_WIDTH, "A new line of text?!")
    myscreen.refresh()
    myscreen.getch()

    curses.endwin()

if __name__ == '__main__':
    wrapper(main)
