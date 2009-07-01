import events

class Callback(object):
	__slots__ = ['query', 'filter', 'action', 'caller', 'target', 'action_params']

	def __init__(self, query, filter, caller, target, action, action_params = {}):
		self.query, self.filter = query, filter
		self.caller, self.target = caller, target
		self.action, self.action_params = action, action_params

	def run(self):
		self.target.action(self.action, self.caller, self.action_params)

	def match(self, event):
		return self.query.match(event) and self.filter(event.element)


