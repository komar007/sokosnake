from element import *
from callback import *
import events

class Passage(Element):
	conflicts_with = []

class Wall(Element):
	conflicts_with = []

# For Head and Body
def action_stretch(self, event, params):
	if self.next is None:
		b = Body(self.x, self.y, self.game, {'prev': self})
		self.next = b
	else:
		self.next.run_action('stretch')

class Head(Element):
	conflicts_with = [Wall]

	def parse_params(self, params = {}):
		self.expected_len = int(params['len'])

	def post_init(self):
		self.len = 0
		self.next = None

	def action_move(self, event, params):
		if self.expected_len > self.len:
			self.run_action('stretch', {'prev': None})
		self.len += 1
		self.move(params['x'], params['y'])

	supported_actions = {'move': action_move, 'stretch': action_stretch}

class Body(Element):
	conflicts_with = [Wall, Head]

	def __init__(self, x, y, game = None, params = {}):
		Element.__init__(self, x, y, game, params)
		self.post_init()
	
	def parse_params(self, params = {}):
		self.prev = params['prev']

	def post_init(self):
		self.next = None
		self.game.add_callback(Callback(
				query = events.Move(self.prev, 'after', None, None),
				target = self,
				action = 'pull'))

	def action_pull(self, event, params):
		self.move(*event.from_field)


	supported_actions = {'pull': action_pull, 'stretch': action_stretch}

class Room(Element):
	conflicts_with = [Passage]

class Pushable(Element):
	def post_init(self):
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

	# FIXME: This is ugly
	def __init__(self, x, y, game = None, params = {}):
		Pushable.__init__(self, x, y, game, params)
		self.conflicts_with.append(Diamond)


class Apple(Element):
	conflicts_with = [Wall, Diamond]

	def post_init(self):
		self.game.add_callback(Callback(
				query = events.Move(self.game.snake, 'before', None, (self.x, self.y)),
				target = self,
				action = 'eat'))

	def action_eat(self, event, params):
		self.destroy()

	supported_actions = {'eat': action_eat}

class Teleport(Element):
	conflicts_with = [Wall, Diamond]
	def parse_params(self, params = {}):
		self.num = int(params['n'])
		self.to_x, self.to_y = int(params['x']), int(params['y'])

	def post_init(self):
		self.game.add_callback(Callback(
				query = events.Move(self.game.snake, 'after', None, (self.x, self.y)),
				target = self.game.snake,
				action = 'move',
				action_params = {'x': self.to_x, 'y': self.to_y}))

class Teleend(Element):
	conflicts_with = [Wall, Diamond]
	def parse_params(self, params = {}):
		self.num = int(params['n'])

class Rock(Pushable):
	conflicts_with = [Wall, Head, Body, Diamond, Teleport, Teleend, Apple]
