class Event(object):
	def __init__(self, elem, type):
		self.element = elem
		if type in ['before', 'after']:
			self.type = type
		else:
			raise TypeError("Event type must be either 'before' or 'after'")

class Move(Event):
	def __init__(self, elem, type, from_field, to_field):
		Event.__init__(self, elem, type)
		self.from_field = from_field
		self.to_field = to_field

class AttrChange(Event):
	def __init__(self, elem, type, attr_name, prev_value, cur_value):
		Event.__init__(self, elem, type)
		self.attr_name = attr_name
		self.prev_value, self.cur_value = prev_value, cur_value
