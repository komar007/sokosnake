import events
from callback import Callback

class Conflict:
	def __init__(self, e, x, y):
		self.e, self.x, self.y = e, x, y

	def __str__(self):
		return repr('Element: %s: conflict at (%i, %i).' %
		            (repr(self.e), self.x, self.y))

class Game:
	def __init__(self, size_x, size_y):
		self.map = {}
		self.elements = []
		self.size_x, self.size_y = size_x, size_y
		for x in range(size_x):
			for y in range(size_y):
				self.map[x, y] = []
		self.callbacks = {}
	
	def add(self, element):
		element.game = self
		self.map[element.x, element.y].append(element)
		self.elements.append(element)

	def find_element(self, func):
		return filter(func, self.elements)

	def remove(self, element):
		element.game = None
		self.map[element.x, element.y].remove(element)
		self.elements.remove(element)

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
