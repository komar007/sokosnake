from game import Game
from elements import *
from parser import Parser

Right = (1,0)
Down = (0,1)
Left = (-1,0)
Up = (0,-1)

class Sokosnake(Game):
	element_hash = {'_': Passage, 'W': Wall,   'S': Head,    'A': Apple,
	                'R': Room,    'K': Rock,   'D': Diamond, 'T': Teleport,
	                't': Teleend}

	def __init__(self, level_str):
		parser = Parser(self.element_hash)
		size_x, size_y = parser.load(open(level_str).read())
		Game.__init__(self, size_x, size_y)
		for element in parser.parse():
			self.add(element)
		self.snake = self.find_element(lambda e: type(e) == Head)[0]
		self.points = 0
		self.diamonds = 0
		self.diamonds_all = len(self.find_element(lambda e: type(e) == Diamond))
		self.post_initialize()

	def step(self, dir):
		target_field = (self.snake.x + dir[0], self.snake.y + dir[1])
		self.snake.run_action('move', {'field': target_field})
