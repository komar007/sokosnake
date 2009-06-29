class Conflict:
	def __init__(self, e, x, y):
		self.e, self.x, self.y = e, x, y

	def __str__(self):
		return repr('Element: %s: conflict at (%i, %i).' %
		            (repr(self.e), self.x, self.y))

class Element(object):
	accepted_under = []
	def __init__(self, x, y, params = {}):
		# Default __init__ ignores params. To be used by subclasses
		self.x = x
		self.y = y
		# the list of other elements the element can be placed on
		self.accepted_under = type(self).accepted_under

	def __del__(self):
		if self.level is not None:
			self.level.remove(self)

	def move(self, x, y):
		# If the element can be placed on all of the elements...
		if all(self.accepts_under(x) for x in self.level.map[x, y]):
			level = self.level
			level.remove(self)
			self.x, self.y = x, y
			level.add(self)
		else:
			raise Conflict(self, x, y)

	def accepts_under(self, obj):
		return type(obj) in self.accepted_under

