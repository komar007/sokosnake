import re

import logging

from game import *
from element import *
from elements import *

class ParseError:
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def element(letter, params, x, y, game):
	# FIXME: Remove any element definitions from parser
	ELEMENTS = {'_': Passage, 'W': Wall,   'S': Head,    'A': Apple,
	            'R': Room,    'K': Rock,   'D': Diamond, 'T': Teleport,
	            't': Teleend}
	try:
		return ELEMENTS[letter](x, y, game, parse_params(params))
	except KeyError:
		raise ParseError("Unrecognized element character: '%c' at position (%i, %i)." %
		                 (letter, x, y))

def parse_level(level_str):
	[header, map] = re.split(r'\n{2,}', level_str)
	[size_x, size_y] = [int(dim) for dim in re.split(r', *', header)]
	lvl = Game(size_x, size_y)
	for y, line in enumerate(re.split('\n', map.strip())):
		for x, token in enumerate(re.split(r'(?<!\\) +', line.strip())):
			for (letter, params) in re.findall(r'([a-zA-Z-_])(?:\(([^()]+)\))?',
			                                   re.sub(r'\\ ', ' ', token)):
				element(letter, params, x, y, lvl)
	return lvl

def parse_params(str):
	h = dict(re.findall(r'([^, ]+)=([^,]+)', str))
	return h
