Any = None

class Event(object):
	check_keys = ['element', 'before_after']

	def __init__(self, elem, before_after, condition = lambda x: True, query = False):
		self.element = elem
		self.condition = condition
		self.check_keys = Event.check_keys + self.check_keys
		if before_after in ['before', 'after']:
			self.before_after = before_after
		else:
			raise TypeError("Event before_after must be either 'before' or 'after', not: '%s'" %
					repr(before_after))

	def match(self, event):
		return all(self.__dict__[key] is None or self.__dict__[key] == event.__dict__[key] for key
				in self.check_keys) and self.condition(event)

	def hash_tuple(self):
		pass

	def possible_hash_tuples(self):
		pass
