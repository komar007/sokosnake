class Level:
	def __init__(self, size_x, size_y):
		self.map = {}
		self.size_x, self.size_y = size_x, size_y
		for x in range(size_x):
			for y in range(size_y):
				self.map[x, y] = []
	
	def add(self, element):
		element.level = self
		self.map[element.x, element.y].append(element)

	def remove(self, element):
		element.level = None
		self.map[element.x, element.y].remove(element)

