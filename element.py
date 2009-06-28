class Element(object):
	def __init__(self, x, y, params = {}):
		self.x = x
		self.y = y
		# Default __init__ ignores params. To be used by subclasses

	def __del__(self):
		if self.level is not None:
			self.level.remove(self)

	def move(self, x, y):
		level = self.level
		level.remove(self)
		self.x, self.y = x, y
		level.add(self)

