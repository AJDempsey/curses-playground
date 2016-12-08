#! /usr/bin/python3

from enum import Enum
import curses

class Token_type(Enum):
	text = 1
	token = 2
	newline = 3
	list_start = 4
	list_end = 5

"""
Class to represent a snippet that has contains metadata with each token.

"""
class Snippet(object):

	def __init__(self, curses_screen):
		self.token_repr =\
		 	[\
				[ 	{"type": Token_type.text, "value":"if"},\
					{"type": Token_type.text, "value":"("},\
					{"type": Token_type.token, "value":"condition", "is_active":False, "is_editing":False},\
					{"type": Token_type.text, "value":")"},\
					{"type": Token_type.list_start, "value":"{"},\
					{"type": Token_type.newline, "value":"\n"},\
				],\
				[\
					{"type": Token_type.token, "value":"Your code here", "is_active":False, "is_editing":False},\
					{"type": Token_type.newline, "value":"\n"}
				],\
				[\
					{"type": Token_type.list_end, "value":"}"},\
					{"type": Token_type.newline, "value":"\n"}

				]\
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
		y, x = self.token_position[-1]
		if self.token_repr[y][x]["is_active"]:
			self.token_repr[y][x]["value"] = ""
			self.token_repr[y][x]["is_active"] = False
			self.token_repr[y][x]["is_editing"] = True
		if user_input != "KEY_BACKSPACE":
			self.token_repr[y][x]["value"] += user_input
		else:
			self.token_repr[y][x]["value"] = self.token_repr[y][x]["value"][:-1]
		self.update_screen()

	def update_screen(self):
		indentation_level = 0
		line_number = 0
		prefix = ""
		cursor_y = 0
		cursor_x = 0
		for line in self.token_repr:
			line_length = 0
			for token in line:
				token_string = ""
				if token["type"] == Token_type.list_end:
					indentation_level -= 4
				if line_length == 0:
					prefix = "\t"*indentation_level
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
			line_number += 1
			line_length = 0
		self.screen.move(cursor_y, cursor_x)
		self.screen.refresh()


	def __find_tokens(self):
		y_pos = 0
		x_pos = 0
		for line in self.token_repr:
			for token in line:
				if token["type"] == Token_type.token:
					self.token_position.append((y_pos, x_pos))
				x_pos += 1
			y_pos += 1
			x_pos = 0

	def highlight_next_token(self):
		next_token = self.token_position.pop(0)
		prev_token = self.token_position[-1]
		y, x = prev_token
		self.token_repr[y][x]["is_active"] = False
		self.token_repr[y][x]["is_editing"] = False
		y, x = next_token
		self.token_repr[y][x]["is_active"] = True
		self.token_repr[y][x]["is_editing"] = False
		self.token_position.append(next_token)

	def __str__(self):
		working_string = ""
		indentation_level = 0
		for line in self.token_repr:
			for token in line:
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
