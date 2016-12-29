"""
Base module for snippets that can be built upon to provide specific
snippet functionality.

Copyright (c) 2016 Anthony Dempsey, Colin Docherty
"""

#! /usr/bin/python3

from enum import Enum
import curses

class Token_type(Enum):
    """
    Enum class to describe the different types of tokens we've parsed.
    """

    text = 1
    token = 2
    newline = 3
    list_start = 4
    list_end = 5

    def __str__(self):
        """
        Convert Enum to a string representation.
        """

        if self.value == 1:
            return "text"
        elif self.value == 2:
            return "token"
        elif self.value == 3:
            return "new line"
        elif self.value == 4:
            return "list_start"
        elif self.value == 5:
            return "list_end"
        else:
            return "unkown"


class Snippet(object):
    """
    Class to represent a snippet that has contains metadata with each token.
    """

    def __init__(self, curses_screen):
        """
        Constructor for the class.
        The token_repr in other classes should parse a file containing either:
        i) A token representation in xml
        or
        ii) A normal string that the snippet class itself will parse into a token stream
        """

        self.token_repr =\
             [\
                 {"type": Token_type.text, "value":"if"},\
                {"type": Token_type.text, "value":"("},\
                {"type": Token_type.token, "value":"condition", "is_active":False, "is_editing":False},\
                {"type": Token_type.text, "value":")"},\
                {"type": Token_type.list_start, "value":"{"},\
                {"type": Token_type.newline, "value":"\n"},\
                {"type": Token_type.token, "value":"Your code here", "is_active":False, "is_editing":False},\
                {"type": Token_type.newline, "value":"\n"},\
                {"type": Token_type.list_end, "value":"}"},\
                {"type": Token_type.newline, "value":"\n"}\
            ]
        self.token_position = [] # List of editable token positions in token_repr.
        self.current_token = -1 # The current index in token_repr for the token we're editing.
        self.__find_tokens() # Populate token_position.
        self.highlight_token(1) # Highlight the first token in the token string that we can edit.
        self.screen = curses_screen
        self.is_user_input = False
        self.error_tool_tip = None

    def move_to_next_edit_token(self):
        """
        Move forward one edit token.
        """
        self.__move_to_different_edit_token(1)

    def move_to_previous_edit_token(self):
        """
        Move back one edit token.
        """
        self.__move_to_different_edit_token(-1)

    def __move_to_different_edit_token(self, direction):
        """
        Generic movement function to reduce code duplication.
        """
        self.highlight_token(direction)
        self.is_user_input = False
        self.update_screen()

    def update_token_string(self, user_input):
        """
        Update the contents of the currently editable token.

        Each time the user comes to the token it is wiped out and then evey
        keypress captured is added to the token's value. Every key except
        <enter>, <shift>+<tab>, and <tab> will be added. This means strange
        strings can appear if the user isn't careful (usually special keys).
        """

        self.is_user_input = True
        if self.token_repr[self.current_token]["is_active"]:
            self.token_repr[self.current_token]["value"] = ""
            self.token_repr[self.current_token]["is_active"] = False
            self.token_repr[self.current_token]["is_editing"] = True
        if user_input != "KEY_BACKSPACE":
            self.token_repr[self.current_token]["value"] += user_input
        else:
            self.token_repr[self.current_token]["value"] = \
                self.token_repr[self.current_token]["value"][:-1]
        self.update_screen()

    def update_screen(self):
        """
        This is the heavy lifting function that traverses the data structure
        and updates the displayed string based on the contents of each entry
        in the structure.

        The general algorithm is very naive, it clears the screen and then walks
        the whole data structure updating the screen with the contents of each
        index. It does this for every valid keypress. Improvements on the
        algorithm can be done later.
        """

        self.screen.clear()
        indentation_level = 0
        line_number = 0
        prefix = ""
        cursor_y = 0
        cursor_x = 0
        line_length = 0
        for token in self.token_repr:
            if token["type"] == Token_type.newline:
                line_number += 1
                line_length = 0
                continue
            token_string = ""
            if token["type"] == Token_type.list_end:
                indentation_level -= 4
            if line_length == 0:
                prefix = " "*indentation_level
                self.screen.addstr(line_number, line_length, token_string)
                line_length += len(prefix)
            if token["type"] == Token_type.token:
                token_string = "<"+token["value"]+">"
                if token["is_active"]:
                    self.screen.addstr(line_number, line_length, token_string,\
                        curses.A_REVERSE)
                    if not self.is_user_input:
                        cursor_x = line_length
                        cursor_y = line_number
                else:
                    self.screen.addstr(line_number, line_length, token_string,\
                        curses.A_UNDERLINE)
                if self.is_user_input and token["is_editing"]:
                    cursor_x = line_length + len(token["value"]) + 1
                    cursor_y = line_number
                line_length += len(token_string)
                token_string = " "
                self.screen.addstr(line_number, line_length, token_string)
            else:
                token_string += token["value"]+" "
                self.screen.addstr(line_number, line_length, token_string)
            line_length += len(token_string)
            if token["type"] == Token_type.list_start:
                indentation_level += 4
        self.screen.move(cursor_y, cursor_x)
        self.screen.refresh()
        if self.error_tool_tip is not None and self.error_tool_tip.is_active():
            self.error_tool_tip.activate()


    def __find_tokens(self):
        """
        Find the index of all tokens that the user needs to modify and store
        them in a list.
        """

        index_of_editable = 0
        for token in self.token_repr:
            if token["type"] == Token_type.token:
                self.token_position.append(index_of_editable)
            index_of_editable += 1
        if self.current_token > -1:
            # Find index of the currently highlighted token in our regenerated list.
            # Remove that token index from the list and reorganise it so that everything
            # before the index is now at the end of the list.
            # The index will be added back into the list at the next navigation jump.
            index = self.token_position.index(self.current_token)
            self.token_position = self.token_position[index+1:] + self.token_position[:index]

    def highlight_token(self, direction):
        """
        Highlight the next token that can be edited, the next token is
        defined by the direction argument.
        This function marks the token so it can be highlighted on the next
        screen update.
        We store the index of the highlighted token in self.current_token for
        use in other functions and to make finding the next token easier.
        The current token is added to one end of the list and the next token to
        highlight is taken from the other end.
        """

        if self.current_token == -1:
            self.current_token = self.token_position.pop(0)
            self.token_repr[self.current_token]["is_active"] = True
            self.token_repr[self.current_token]["is_editing"] = False
            return
        if direction > 0:
            prev_token = self.current_token
            self.current_token = self.token_position.pop(0)
            self.token_position.append(prev_token)
        elif direction < 0:
            prev_token = self.current_token
            self.current_token = self.token_position.pop()
            self.token_position.insert(0, prev_token)
        self.token_repr[prev_token]["is_active"] = False
        self.token_repr[prev_token]["is_editing"] = False
        self.token_repr[self.current_token]["is_active"] = True
        self.token_repr[self.current_token]["is_editing"] = False

    def  add_error_tool_tip(self, new_tool_tip):
        """
        When an unkown key is pressed we want the user to know that we don't understand.
        This adds a tooltip to the screen and keeps it there over screen refreshes.
        """

        if self.error_tool_tip is not None:
            del self.error_tool_tip
        self.error_tool_tip = new_tool_tip
        self.error_tool_tip.activate()

    def remove_error_tool_tip(self):
        """
        Delete an exisiting tool tip from the class and therefore the screen.
        """
        self.error_tool_tip = None

    def insert_new_edit_token(self):
        """
        For snippets without a defined data model the user should not be limited to only
        the code in the defined snippet. They should be able to add their own lines and modify
        them at will.
        """

        new_token = {"type": Token_type.token, "value":"Your code here", "is_active":False,\
                    "is_editing":False}
        line_index, _ = self.screen.getyx()
        number_of_newlines = 0
        insert_index = 0
        for token in self.token_repr:
            if token["type"] == Token_type.newline:
                number_of_newlines += 1
            insert_index += 1
            if number_of_newlines -1 == line_index:
                break
        self.token_repr.insert(insert_index, new_token)
        new_token = {"type": Token_type.newline, "value":"\n"}
        self.token_repr.insert(insert_index+1, new_token)
        self.token_position = []
        self.__find_tokens()
        self.update_screen()

    def validate_line(self, line_number):
        """
        Validate one line of the snippet if there is a data model available
        """
        pass

    def __str__(self):
        """
        Convert the snippet into a human readable string.
        Will print out what ever is currently contained in each token.
        """

        working_string = ""
        indentation_level = 0
        for token in self.token_repr:
            if token["type"] == Token_type.text:
                working_string += ("\t"*indentation_level)+str(token["value"])+" "
            elif token["type"] == Token_type.token:
                working_string += ("\t"*indentation_level)+"<"+str(token["value"])+"> "
            else:
                if token["type"] == Token_type.list_end:
                    indentation_level -= 1
                working_string += ("\t"*indentation_level)+str(token["value"])
                if token["type"] == Token_type.list_start:
                    indentation_level += 1
        return working_string
