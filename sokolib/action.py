class Action:
	__slots__ = ['target', 'name', 'params']

	def __init__(self, target, name, params = {}):
		self.target = target
		self.name = name
		self.params = params

	def run(self, calling_event = None):
		if self.target.in_game():
			try:
				self.target.supported_actions[self.name](self.target, calling_event, self.params)
			except KeyError:
				pass

class ActionReceiver(object):
	def action(self, name, params = {}):
		return Action(self, name, params)
