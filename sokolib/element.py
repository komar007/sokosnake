import events
from attribute import Attribute
from game import Conflict
from action import Action, ActionReceiver

class Element(ActionReceiver):
	conflicts_with = []
	supported_actions = {}
	def __init__(self, x, y, game = None, params = {}):
		# Default __init__ ignores params. To be used by subclasses
		self.x, self.y = x, y
		self.conflicts_with = list(type(self).conflicts_with)
		if game is not None:
			game.add(self)
		self.parse_params(params)

	def __del__(self):
		destroy(self)
	
	def in_game(self):
		return self.game is not None

	def destroy(self):
		if self.in_game():
			self.game.remove(self)

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


	def parse_params(self, params = {}):
		for (key, val) in zip(params.keys(), params.values()):
			self.__dict__[key] = self.parse_param(val)
		
	def parse_param(self, param):
		p = param
		try:
			p = float(param)
			p = int(param)
		except (ValueError, TypeError):
			pass
		return p

	def event(self, before_after, type,
	           from_field = None, to_field = None,
	           attr_name = None, prev_val = None, next_val = None,
			   condition = lambda x: True):
		"""Create an event query with element parameter set to self

		Example::
		
			snake.event('before', Move, to_field = self.pos)
			
		will create a query which will trigger an action before each time
		element *snake* moves into the field with self"""
		if type == events.Move:
			return events.Move(self, before_after, from_field, to_field, condition, query = True)
		elif type == events.AttrChange:
			return events.AttrChange(self, before_after, attr_name, prev_val, next_val, condition, query = True) 

	def post_init(self):
		pass

