import events
from attribute import Attribute
from game import Conflict

class Element(object):
	conflicts_with = []
	supported_actions = {}
	def __init__(self, x, y, game = None, params = {}):
		# Default __init__ ignores params. To be used by subclasses
		self.x = x
		self.y = y
		self.conflicts_with = type(self).conflicts_with
		if game is not None:
			game.add(self)
		self.parse_params(params)

	def __del__(self):
		if self.game is not None:
			self.game.remove(self)
	
	def destroy(self):
		if self.in_game():
			self.game.remove(self)

	def in_game(self):
		return self.game is not None

	def move(self, x, y):
		# If the element can be placed on all of the elements...
		game = self.game
		game.send_callbacks(events.Move(self, 'before',
			from_field = (self.x, self.y), to_field = (x, y)))
		if not any(self.conflict(x) for x in self.game.map[x, y]):
			game.remove(self)
			old_x, old_y = self.x, self.y
			self.x, self.y = x, y
			game.add(self)
			game.send_callbacks(events.Move(self, 'after',
				from_field = (old_x, old_y), to_field = (self.x, self.y)))
		else:
			raise Conflict(self, x, y)

	def conflict(self, obj):
		return type(obj) in self.conflicts_with or type(self) in obj.conflicts_with

	def run_action(self, name, params = {}, calling_event = None):
		try:
			if self.in_game():
				self.supported_actions[name](self, calling_event, params)
		except KeyError:
			pass

	def parse_params(self, params = {}):
		for (key, val) in zip(params.keys(), params.values()):
			self.__dict__[key] = self.parse_param(val)
		
	def parse_param(self, param):
		try:
			p = param
			p = float(param)
			p = int(param)
		except (ValueError, TypeError):
			pass
		return p

	def post_init(self):
		pass

