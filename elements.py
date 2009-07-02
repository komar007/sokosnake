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

	def post_init(self):
		self.real_len = 0
		self.next = None

	def action_move(self, event, params):
		if self.len > self.real_len:
			self.run_action('stretch', {'prev': None})
		self.real_len += 1
		self.move(*params['field'])

	supported_actions = {'move': action_move, 'stretch': action_stretch}

class Body(Element):
	conflicts_with = [Wall, Head]

	def __init__(self, x, y, game = None, params = {}):
		Element.__init__(self, x, y, game, params)
		self.post_init()
	
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

	def post_init(self):
		self.game.add_callback(Callback(
				query = events.Move(None, 'after', None, (self.x, self.y)),
				target = self,
				action = 'diamond',
				action_params = {'dir': 'in'},
				filter = lambda ev: type(ev.element) == Diamond))
		self.game.add_callback(Callback(
				query = events.Move(None, 'after', (self.x, self.y), None),
				target = self,
				action = 'diamond',
				action_params = {'dir': 'out'},
				filter = lambda ev: type(ev.element) == Diamond))

	def action_diamond(self, event, params):
		if params['dir'] == 'in':
			self.game.diamonds += 1
		else:
			self.game.diamonds -= 1

	supported_actions = {'diamond': action_diamond}

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
		self.game.snake.run_action('stretch')
		self.game.points += 10
		self.destroy()

	supported_actions = {'eat': action_eat}

class Teleport(Element):
	conflicts_with = [Wall, Diamond]

	def post_init(self):
		self.game.add_callback(Callback(
				query = events.Move(self.game.snake, 'after', None, (self.x, self.y)),
				target = self.game.snake,
				action = 'move',
				action_params = {'field': (self.to_x, self.to_y)}))

class Teleend(Element):
	conflicts_with = [Wall, Diamond]

class Rock(Pushable):
	conflicts_with = [Wall, Head, Body, Diamond, Teleport, Teleend, Apple]
