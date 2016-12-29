"""
Tool tip addition to curses display

(not the best implementation)

Copyright (c) 2016 Anthony Dempsey, Colin Docherty
"""

#! /usr/bin/python3

import curses

class Tool_tip(object):
    """
    Generic class for creating a tool tip window for a snippet.
    """

    def __init__(self, y_pos, x_pos, y_size, x_size):
        """
        Constructor for the tool tip. Store data relevant to the tool tip
        """
        self.win = None
        self.y_coord = y_pos
        self.x_coord = x_pos
        self.height = y_size
        self.width = x_size
        self.window_content = []
        self.active = False

    def add_to_window(self, new_addition):
        """
        Add a new string to the window_content list.
        """
        self.window_content.append(new_addition)

    def clear_window_content(self):
        """
        Delete everything in the window_content list.
        """
        self.window_content = []

    def activate(self):
        """
        Create the window for the tool tip and activate it.
        """
        self.win = curses.newwin(self.height, self.width, self.y_coord, self.x_coord)
        self.win.border()
        self.win.clear()
        count = 0
        while count < len(self.window_content):
            self.win.addstr(count, 0, self.window_content[count], curses.color_pair(2))
            count += 1
        self.win.refresh()
        self.active = True

    def deactivate(self):
        """
        Reset tool tip to inactive so it can be cleaned up.
        """
        self.active = False

    def is_active(self):
        """
        Find out if tool tip is active or not.
        """
        return self.active
