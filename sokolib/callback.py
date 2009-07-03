import events

class Callback(object):
	__slots__ = ['query', 'action']

	def __init__(self, query, action):
		self.query = query
		self.action = action

	def run(self, event):
		self.action.run(event)

	def match(self, event):
		return self.query.match(event)
