from element import *

class Passage(Element):
	accepted_under = []

class Teleport(Element):
	accepted_under = [Passage]
	def __init__(self, x, y, params = {}):
		super(Teleport, self).__init__(x, y, params)
		self.num = int(params['n'])

class Teleend(Element):
	accepted_under = [Passage]
	def __init__(self, x, y, params = {}):
		super(Teleend, self).__init__(x, y, params)
		self.num = int(params['n'])

class Wall(Element):
	accepted_under = [Passage]

class Room(Element):
	accepted_under = [Passage]

class Apple(Element):
	accepted_under = [Passage, Room, Teleport, Teleend]

class Rock(Element):
	accepted_under = [Passage, Room]

class Diamond(Element):
	accepted_under = [Passage, Room]

class Body(Element):
	accepted_under = [Passage, Teleport, Teleend]

class Head(Element):
	accepted_under = [Passage, Teleport, Teleend]
	def __init__(self, x, y, params = {}):
		super(Head, self).__init__(x, y, params)
		self.expected_len = params['len']
		self.len = 0
