#! /usr/bin/python3

from enum import Enum
import curses

class Token_type(Enum):
	text = 1
	token = 2
	newline = 3
	list_start = 4
	list_end = 5

	def __str__(self):
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

"""
Class to represent a snippet that has contains metadata with each token.

"""
class Snippet(object):

	def __init__(self, curses_screen):
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
		self.token_position = []
		self.__find_tokens()
		self.highlight_next_token()
		self.screen = curses_screen
		self.is_user_input = False

	def move_to_next_edit_token(self):
		self.highlight_next_token()
		self.is_user_input = False
		self.update_screen()

	def update_token_string(self, user_input):
		self.is_user_input = True
		editing_token = self.token_position[-1]
		if self.token_repr[editing_token]["is_active"]:
			self.token_repr[editing_token]["value"] = ""
			self.token_repr[editing_token]["is_active"] = False
			self.token_repr[editing_token]["is_editing"] = True
		if user_input != "KEY_BACKSPACE":
			self.token_repr[editing_token]["value"] += user_input
		else:
			self.token_repr[editing_token]["value"] = self.token_repr[editing_token]["value"][:-1]
		self.update_screen()

	def update_screen(self):
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
				indentation_level -=4
			if line_length == 0:
				prefix = " "*indentation_level
				self.screen.addstr(line_number, line_length, token_string)
				line_length += len(prefix)
			if token["type"] == Token_type.token:
				token_string = "<"+token["value"]+">"
				if token["is_active"]:
					self.screen.addstr(line_number, line_length, token_string,\
						curses.color_pair(curses.COLOR_YELLOW))
					if not self.is_user_input:
						cursor_x = line_length
						cursor_y = line_number
				else:
					self.screen.addstr(line_number, line_length, token_string)
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


	def __find_tokens(self):
		index_of_editable = 0
		for token in self.token_repr:
			if token["type"] == Token_type.token:
				self.token_position.append(index_of_editable)
			index_of_editable += 1

	def highlight_next_token(self):
		next_token = self.token_position.pop(0)
		prev_token = self.token_position[-1]
		self.token_repr[prev_token]["is_active"] = False
		self.token_repr[prev_token]["is_editing"] = False
		self.token_repr[next_token]["is_active"] = True
		self.token_repr[next_token]["is_editing"] = False
		self.token_position.append(next_token)

	def __str__(self):
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
