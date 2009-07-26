import events
from callback import Callback

class Conflict:
	def __init__(self, e, x, y):
		self.e, self.x, self.y = e, x, y

	def __str__(self):
		return repr('Element: %s: conflict at (%i, %i).' %
		            (repr(self.e), self.x, self.y))

class Game(object):
	def __init__(self, size_x, size_y):
		self.map = {}
		self.elements = []
		self.size_x, self.size_y = size_x, size_y
		for x in range(size_x):
			for y in range(size_y):
				self.map[x, y] = []
		self.callbacks = {}
	
	def add(self, element):
		self.send_callbacks(events.Create('before', element))
		element.game = self
		self.map[element.x, element.y].append(element)
		self.elements.append(element)
		self.send_callbacks(events.Create('after', element))

	def post_initialize(self):
		for element in self.elements:
			element.post_init()

	def find_elements(self, func):
		return filter(func, self.elements)

	def find_element(self, func):
		return self.find_elements(func)[0]

	def remove(self, element):
		self.send_callbacks(events.Remove(element, 'before'))
		element.game = None
		self.map[element.x, element.y].remove(element)
		self.elements.remove(element)
		self.send_callbacks(events.Remove(element, 'after'))

	def send_callbacks(self, event):
		for key in event.possible_hash_tuples():
			if not self.callbacks.has_key(key):
				continue
			for callback in self.callbacks[key]:
				if callback.match(event):
					callback.run(event)

	def add_callback(self, callback):
		try:
			self.callbacks[callback.query.hash_tuple()].append(callback)
		except KeyError:
			self.callbacks[callback.query.hash_tuple()] = [callback]

	def connect(self, query, action):
		c = Callback(query = query, action = action)
		self.add_callback(c)

	def event(self, element, before_after, type,
	           from_field = None, to_field = None,
	           attr_name = None, prev_val = None, next_val = None,
			   condition = lambda x: True):
		"""Create a generic event query

		Example::
		
			game.event(Any, 'before', Move, to_field = self.pos)
			
		will create a query which will trigger an action before each time
		any element moves into the field with self"""
		if type == events.Move:
			return events.Move(element, before_after, from_field, to_field, condition, query = True)
		elif type == events.AttrChange:
			return events.AttrChange(element, before_after, attr_name, prev_val, next_val, condition, query = True) 
