from sokolib.element import *
from sokolib.callback import *
from sokolib.event import *
from sokolib.events import *

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
		self.next.action('stretch').run()

class Head(Element):
	conflicts_with = [Wall]

	def post_init(self):
		self.real_len = 0
		self.next = None

	def action_move(self, event, params):
		if self.len > self.real_len:
			self.action('stretch', {'prev': None}).run()
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
		self.game.connect(self.prev.event('after', Move), self.action('pull'))

	def action_pull(self, event, params):
		self.move(*event.from_field)


	supported_actions = {'pull': action_pull, 'stretch': action_stretch}

class Room(Element):
	conflicts_with = [Passage]

	def post_init(self):
		self.game.connect(self.game.event(Any, 'after', Move, to_field = (self.x, self.y), condition = lambda ev: type(ev.element) == Diamond), self.action('diamond', {'dir': 'in'}))

		self.game.connect(self.game.event(Any, 'after', Move, from_field = (self.x, self.y), condition = lambda ev: type(ev.element) == Diamond), self.action('diamond', {'dir': 'out'}))

	def action_diamond(self, event, params):
		if params['dir'] == 'in':
			self.game.diamonds += 1
		else:
			self.game.diamonds -= 1

	supported_actions = {'diamond': action_diamond}

class Pushable(Element):
	def post_init(self):
		snake = self.game.snake
		self.game.connect(snake.event('before', Move, condition = lambda ev: ev.to_field == (self.x, self.y)), self.action('push'))

	def action_push(self, event, params):
		self.move(self.x + event.to_field[0] - event.from_field[0],
		          self.y + event.to_field[1] - event.from_field[1])

	supported_actions = {'push': action_push}

class Diamond(Pushable):
	def post_init(self):
		self.conflicts_with = [Wall, Head, Body, Diamond]
		Pushable.post_init(self)

class Apple(Element):
	conflicts_with = [Wall, Diamond]

	def post_init(self):
		snake = self.game.snake
		self.game.connect(snake.event('before', Move, to_field = (self.x, self.y)), self.action('eat'))

	def action_eat(self, event, params):
		self.game.snake.action('stretch').run()
		self.game.points += 10
		self.destroy()

	supported_actions = {'eat': action_eat}

class Teleport(Element):
	conflicts_with = [Wall, Diamond]

	def post_init(self):
		self.teleend = self.game.find_element(lambda e: type(e) == Teleend and e.n == self.n)
		snake = self.game.snake
		self.game.connect(snake.event('after', Move, to_field = (self.x, self.y)), snake.action('move', {'field': (self.teleend.x, self.teleend.y)}))

class Teleend(Element):
	conflicts_with = [Wall]

class Rock(Pushable):
	def post_init(self):
		self.conflicts_with = [Wall, Head, Body, Diamond, Teleport, Teleend, Apple, Rock]
		Pushable.post_init(self)
