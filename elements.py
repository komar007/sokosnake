from element import *
from callback import *
import events

class Passage(Element):
	conflicts_with = []

class Wall(Element):
	conflicts_with = []

class Head(Element):
	conflicts_with = [Wall]

	def __init__(self, x, y, game = None, params = {}):
		Element.__init__(self, x, y, game, params)
		self.game.snake = self

	def action_move(self, event, params):
		print "asdasdasd"
		self.move(params['x'], params['y'])

	supported_actions = {'move': action_move}

class Body(Element):
	conflicts_with = [Wall, Head]

class Room(Element):
	conflicts_with = [Passage]


class Pushable(Element):
	def __init__(self, x, y, game = None, params = {}):
		Element.__init__(self, x, y, game, params)
		self.game.add_callback(Callback(
				query = events.Move(self.game.snake, 'before', None, None),
				target = self,
				action = 'push',
				filter = lambda ev: ev.to_field == (self.x, self.y)))

	def action_push(self, event, params):
		self.move(self.x + event.to_field[0] - event.from_field[0],
		          self.y + event.to_field[1] - event.from_field[1])

	supported_actions = {'push': action_push}

class Diamond(Pushable):
	conflicts_with = [Wall, Head, Body]

	def __init__(self, x, y, game = None, params = {}):
		Pushable.__init__(self, x, y, game, params)
		self.conflicts_with.append(Diamond)


class Apple(Element):
	conflicts_with = [Wall]

class Teleport(Element):
	conflicts_with = [Wall, Diamond]
	def __init__(self, x, y, game = None, params = {}):
		Element.__init__(self, x, y, game, params)
		self.num = int(params['n'])

		self.game.add_callback(Callback(
				query = events.Move(self.game.snake, 'after', None, (self.x, self.y)),
				target = self.game.snake,
				action = 'move',
				action_params = {'x': 7, 'y': 6}))

class Teleend(Element):
	conflicts_with = [Wall, Diamond]
	def __init__(self, x, y, game = None, params = {}):
		Element.__init__(self, x, y, game, params)
		self.num = int(params['n'])

class Rock(Pushable):
	conflicts_with = [Wall, Head, Body, Diamond, Teleport, Teleend, Apple]
