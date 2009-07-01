from element import *

class Passage(Element):
	conflicts_with = []

class Wall(Element):
	conflicts_with = []

class Head(Element):
	conflicts_with = [Wall]
	def __init__(self, x, y, params = {}):
		Element.__init__(self, x, y, params)
		self.expected_len = params['len']
		self.len = 0

class Body(Element):
	a = Attribute("attr")
	conflicts_with = [Wall, Head]

class Room(Element):
	conflicts_with = [Passage]

class Diamond(Element):
	conflicts_with = [Wall, Head, Body]

class Apple(Element):
	conflicts_with = [Wall]

class Teleport(Element):
	conflicts_with = [Wall, Diamond]
	def __init__(self, x, y, params = {}):
		Element.__init__(self, x, y, params)
		self.num = int(params['n'])

class Teleend(Element):
	conflicts_with = [Wall, Diamond]
	def __init__(self, x, y, params = {}):
		Element.__init__(self, x, y, params)
		self.num = int(params['n'])

class Rock(Element):
	conflicts_with = [Head, Body, Diamond, Teleport, Teleend, Apple]


