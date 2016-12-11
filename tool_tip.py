#! /usr/bin/python3

import curses

class Tool_tip(object):
    """
    Generic class for creating a tool tip window for a snippet.
    """

    def __init__(self, y_pos, x_pos, y_size, x_size):
        self.win = None
        self.y_coord = y_pos
        self.x_coord = x_pos
        self.height = y_size
        self.width = x_size
        self.window_content = []
        self.active = False

    def add_to_window(self, new_addition):
        self.window_content.append(new_addition)

    def clear_window_content(self):
        self.window_content = []

    def activate(self):
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
        self.active = False

    def is_active(self):
        return self.active
