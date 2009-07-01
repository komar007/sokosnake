import events
from callback import *

class Game:
	def __init__(self, size_x, size_y):
		self.map = {}
		self.size_x, self.size_y = size_x, size_y
		for x in range(size_x):
			for y in range(size_y):
				self.map[x, y] = []
		self.callbacks = {}
	
	def add(self, element):
		element.game = self
		self.map[element.x, element.y].append(element)

	def remove(self, element):
		element.game = None
		self.map[element.x, element.y].remove(element)

	def send_callbacks(self, event):
		for key in event.possible_hash_tuples():
			if not self.callbacks.has_key(key):
				continue
			for callback in self.callbacks[key]:
				if callback.match(event):
					callback.run(event)



	def add_callback(self, callback):
		if self.callbacks.has_key(callback.query.hash_tuple()):
			self.callbacks[callback.query.hash_tuple()].append(callback)
		else:
			self.callbacks[callback.query.hash_tuple()] = [callback]
