from element import *

class Passage(Element):
	def __init__(self, x, y, params = {}):
		super(Passage, self).__init__(x, y, params)
		self.accepted_under = []

class Wall(Element):
	def __init__(self, x, y, params = {}):
		super(Wall, self).__init__(x, y, params)
		self.accepted_under = [Passage]

class Apple(Element):
	def __init__(self, x, y, params = {}):
		super(Apple, self).__init__(x, y, params)
		self.accepted_under = [Passage, Room, Teleport, Teleend]

class Room(Element):
	def __init__(self, x, y, params = {}):
		super(Room, self).__init__(x, y, params)
		self.accepted_under = [Passage]

class Rock(Element):
	def __init__(self, x, y, params = {}):
		super(Rock, self).__init__(x, y, params)
		self.accepted_under = [Passage, Room]

class Diamond(Element):
	def __init__(self, x, y, params = {}):
		super(Diamond, self).__init__(x, y, params)
		self.accepted_under = [Passage, Room]

class Teleport(Element):
	def __init__(self, x, y, params = {}):
		super(Teleport, self).__init__(x, y, params)
		self.accepted_under = [Passage]
		self.num = int(params['n'])

class Teleend(Element):
	def __init__(self, x, y, params = {}):
		super(Teleend, self).__init__(x, y, params)
		self.accepted_under = [Passage]
		self.num = int(params['n'])

class Head(Element):
	def __init__(self, x, y, params = {}):
		super(Head, self).__init__(x, y, params)
		self.accepted_under = [Passage, Teleport, Teleend]
		self.expected_len = params['len']
		self.len = 0

class Body(Element):
	def __init__(self, x, y, params = {}):
		super(Body, self).__init__(x, y, params)
		self.accepted_under = [Passage, Teleport, Teleend]
