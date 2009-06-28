from element import *

class Passage(Element):
	pass

class Wall(Element):
	pass

class Apple(Element):
	pass

class Room(Element):
	pass

class Rock(Element):
	pass

class Diamond(Element):
	pass

class Teleport(Element):
	pass

class Teleend(Element):
	pass

class Head(Element):
	def __init__(self, x, y, params = {}):
		super(Head, self).__init__(x, y, params)
		self.expected_len = params['len']
		self.len = 0

class Body(Element):
	pass
