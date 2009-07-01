import events

class Conflict:
	def __init__(self, e, x, y):
		self.e, self.x, self.y = e, x, y

	def __str__(self):
		return repr('Element: %s: conflict at (%i, %i).' %
		            (repr(self.e), self.x, self.y))

class Attribute(object):
	def __init__(self, name):
		self.val = None
		self.name = name

	def __get__(self, obj, objtype = None):
		return self.val

	def __set__(self, obj, val):
		old_val = self.val
		obj.game.send_callbacks(events.AttrChange(obj, 'before', self.name, old_val, val))
		self.val = val
		obj.game.send_callbacks(events.AttrChange(obj, 'after', self.name, old_val, val))

class Element(object):
	conflicts_with = []
	supported_actions = {}
	def __init__(self, x, y, game = None, params = {}):
		# Default __init__ ignores params. To be used by subclasses
		self.x = x
		self.y = y
		# the list of other elements the element can be placed on
		self.conflicts_with = type(self).conflicts_with
		if game is not None:
			game.add(self)

	def __del__(self):
		if self.game is not None:
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

	def run_action(self, name, params = {}, calling_event = None):
		try:
			self.supported_actions[name](self, calling_event, params)
		except KeyError:
			pass

