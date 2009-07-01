import curses
from curses import COLOR_BLACK, COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE, COLOR_MAGENTA, COLOR_CYAN, COLOR_WHITE
import os

from element import *
from elements import *
from game import *
from parser import *

backgrounds = {Apple: COLOR_BLACK,        Wall: COLOR_MAGENTA,
               Teleport: COLOR_BLUE,      Teleend: COLOR_GREEN,
               Head: COLOR_BLACK,         Body: COLOR_BLACK,
               Diamond: COLOR_BLACK,      Passage: COLOR_BLACK,
               Rock: COLOR_BLACK,         Room: COLOR_CYAN}

foregrounds = {Apple: COLOR_GREEN,        Wall: COLOR_BLACK,
               Teleport: COLOR_BLACK,     Teleend: COLOR_BLACK,
               Head: COLOR_GREEN,         Body: COLOR_GREEN,
               Diamond: COLOR_RED,        Passage: COLOR_BLACK,
               Rock: COLOR_WHITE,         Room: COLOR_BLACK}

class Interface(object):
	def __init__(self, filename = "lvl"):
		self.load_level(filename)
		self.init_curses()
		self.prepare_colors()

	def __del__(self):
		self.end_curses()

	def load_level(self, filename):
		# FIXME: Fix this
		def findsnake(x):
			if x:
				return x[-1]
			else:
				return None
		self.game = parse_level(open(filename).read())
		self.game.snake = filter(lambda x: type(x) == Head, map(findsnake, self.game.map.values()))[0]

	def init_curses(self):
		self.stdscr = curses.initscr()
		curses.cbreak()
		self.pad = curses.newpad(self.game.size_y + 3, self.game.size_x + 3)
		self.pad.keypad(1)

	def end_curses(self):
		self.pad.keypad(0)
		curses.nocbreak()
		curses.endwin()

	def prepare_colors(self):
		self.color = {}
		curses.start_color()
		for fg in range(8):
			for bg in range(8):
				curses.init_pair(1 + 8*fg + bg, fg, bg)
				self.color[fg, bg] = curses.color_pair(1 + 8*fg + bg)

	def render_field(self, f):
		# FIXME: Do it well
		if len(f) == 0:
			return (' ', curses.A_NORMAL)
		elif len(f) == 1:
			e = f[-1]
			bg = backgrounds[type(e)]
			fg = foregrounds[type(e)]
		if len(f) > 1:
			e = f[-1]
			if(type(f[-2]) == Passage):
				bg = backgrounds[type(e)]
			else:
				bg = backgrounds[type(f[-2])]
			fg = foregrounds[type(e)]

		if type(e) == Apple:
			letter = 'a'
		elif type(e) == Wall:
			letter = '#'
		elif type(e) == Teleport:
			letter = str(e.num)
		elif type(e) == Teleend:
			letter = str(e.num)
		elif type(e) == Head:
			letter = '@'
		elif type(e) == Body:
			letter = 'o'
		elif type(e) == Diamond:
			letter = '%'
		elif type(e) == Passage:
			letter = ' '
		elif type(e) == Rock:
			letter = 'X'
		elif type(e) == Room:
			letter = 'R'
		else:
			letter = ' '

		return (letter, self.color[fg, bg])

	def refresh_window(self):
		for x in range(self.game.size_x):
			for y in range(self.game.size_y):
				self.pad.addch(y, x, *self.render_field(self.game.map[x,y]))
		# FIXME: Change this
		self.pad.refresh(0, 0,  0,0, self.game.size_y + 2, self.game.size_x + 2)

	def start(self):
		# FIXME: To move the snake, send actions or whatever to game
		self.refresh_window()
		while True:
			c = self.pad.getch()
			try:
				if c in [ord('l'), curses.KEY_RIGHT]:
					self.game.snake.move(self.game.snake.x + 1, self.game.snake.y)
				if c in [ord('h'), curses.KEY_LEFT]:
					self.game.snake.move(self.game.snake.x - 1, self.game.snake.y)
				if c in [ord('j'), curses.KEY_DOWN]:
					self.game.snake.move(self.game.snake.x, self.game.snake.y + 1)
				if c in [ord('k'), curses.KEY_UP]:
					self.game.snake.move(self.game.snake.x, self.game.snake.y - 1)
				if c in [ord('q')]:
					break;
				self.refresh_window()
			except Conflict:
				pass



interface = Interface("lvl")
interface.start()
del interface



