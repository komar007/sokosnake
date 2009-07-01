import events

class Callback(object):
	__slots__ = ['query', 'filter', 'action', 'target', 'action_params']

	def __init__(self, query, target, action, action_params = {}, filter = lambda x: True):
		self.query, self.filter = query, filter
		self.target, self.action, self.action_params = target, action, action_params

	def run(self, event):
		self.target.run_action(self.action, self.action_params, event)

	def match(self, event):
		return self.query.match(event) and self.filter(event)
