# FIXME: CRAP, CRAP, CRAP

import curses
from curses import COLOR_BLACK, COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE, COLOR_MAGENTA, COLOR_CYAN, COLOR_WHITE
import os
import sys

from elements import *
from sokosnake import *

backgrounds = {Apple: COLOR_BLACK,        Wall: COLOR_MAGENTA,
               Teleport: COLOR_BLUE,      Teleend: COLOR_GREEN,
               Head: COLOR_BLACK,         Body: COLOR_BLACK,
               Diamond: COLOR_BLACK,      Passage: COLOR_BLACK,
               Rock: COLOR_BLACK,         Room: COLOR_CYAN,
			   Hole: COLOR_RED,           Gate: COLOR_GREEN}

foregrounds = {Apple: COLOR_GREEN,        Wall: COLOR_BLACK,
               Teleport: COLOR_BLACK,     Teleend: COLOR_BLACK,
               Head: COLOR_YELLOW,        Body: COLOR_GREEN,
               Diamond: COLOR_RED,        Passage: COLOR_BLACK,
               Rock: COLOR_WHITE,         Room: COLOR_BLACK,
			   Hole: COLOR_BLACK,         Gate: COLOR_RED}

class Interface(object):
	def __init__(self, filename = "lvl"):
		self.load_level(filename)
		self.init_curses()
		self.prepare_colors()

	def __del__(self):
		self.end_curses()

	def load_level(self, filename):
		self.game = Sokosnake(filename)

	def init_curses(self):
		self.stdscr = curses.initscr()
		curses.cbreak()
		self.pad = curses.newpad(max(self.game.size_y + 3, 20), max(self.game.size_x + 3, 20))
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
			if e.q:
				letter = '?'
			else:
				letter = str(e.n)
		elif type(e) == Teleend:
			letter = str(e.n)
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
		elif type(e) == Hole:
			letter = 'H'
		elif type(e) == Gate:
			if e.open:
				letter = 'G'
			else: 
				letter = '#'
				bg = backgrounds[Wall]
				fg = foregrounds[Wall]
		else:
			letter = ' '

		return (letter, self.color[fg, bg])

	def refresh_window(self):
		for x in range(self.game.size_x):
			for y in range(self.game.size_y):
				self.pad.addch(y, x, *self.render_field(self.game.map[x,y]))
		self.pad.addstr(self.game.size_y + 1, 0, "points: %i\ndiamonds: %i / %i" % (self.game.points, self.game.diamonds, self.game.diamonds_all))
		# FIXME: Change this
		self.pad.refresh(0, 0,  0,0, max(self.game.size_y + 2, 20), max(self.game.size_x + 2, 20))

	def start(self):
		# FIXME: To move the snake, send actions or whatever to game
		self.refresh_window()
		self.moves = ""
		while True:
			c = self.pad.getch()
			try:
				if c in [ord('l'), curses.KEY_RIGHT]:
					self.game.step(Right)
					self.moves += 'r'
				if c in [ord('h'), curses.KEY_LEFT]:
					self.game.step(Left)
					self.moves += 'l'
				if c in [ord('j'), curses.KEY_DOWN]:
					self.game.step(Down)
					self.moves += 'd'
				if c in [ord('k'), curses.KEY_UP]:
					self.game.step(Up)
					self.moves += 'u'
				if c in [ord('q')]:
					break;
				self.refresh_window()
			except Conflict:
				pass
			except GameOver:
				return "You won"

	def play(self, moves):
		# FIXME: To move the snake, send actions or whatever to game
		self.refresh_window()
		for c in moves:
			try:
				if c == 'r':
					self.game.step(Right)
				if c == 'l':
					self.game.step(Left)
				if c == 'd':
					self.game.step(Down)
				if c == 'u':
					self.game.step(Up)
				self.refresh_window()
			except Conflict:
				pass
			except GameOver:
				self.refresh_window()
				return "You won"
			#os.system("sleep 0.25")



interface = Interface(sys.argv[1])

if len(sys.argv) == 3:
	msg = interface.play(open(sys.argv[2]).read())
	interface.start()
	os.system("sleep 1")
else:
	msg = interface.start()
	m = interface.moves
del interface
print msg
if len(sys.argv) != 3:
	print m
if msg is None:
	sys.exit(-1)
else:
	sys.exit(0)
