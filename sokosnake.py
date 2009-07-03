from sokolib.game import Game
from sokolib.parser import Parser
from sokolib.action import *

from elements import *

Right = (1,0)
Down = (0,1)
Left = (-1,0)
Up = (0,-1)

class GameOver:
	def __init__(self, val):
		self.val = val
	def __str__(self):
		return self.val

class Sokosnake(Game):
	element_hash = {'_': Passage, 'W': Wall,   'S': Head,    'A': Apple,
	                'R': Room,    'K': Rock,   'D': Diamond, 'T': Teleport,
	                't': Teleend}

	def __init__(self, level_file):
		parser = Parser(self.element_hash)
		size_x, size_y = parser.load(open(level_file).read())
		Game.__init__(self, size_x, size_y)
		for element in parser.parse():
			self.add(element)
		self.snake = self.find_element(lambda e: type(e) == Head)
		self.points = 0
		self._diamonds = 0
		self.diamonds_all = len(self.find_elements(lambda e: type(e) == Diamond))
		self.post_initialize()

	def get_diamonds(self):
		return self._diamonds

	def set_diamonds(self, val):
		self._diamonds = val
		if self._diamonds == self.diamonds_all:
			raise GameOver("You won!")

	diamonds = property(get_diamonds, set_diamonds)

	def step(self, dir):
		target_field = (self.snake.x + dir[0], self.snake.y + dir[1])
		Action(self.snake, 'move', {'field': target_field}).run()
