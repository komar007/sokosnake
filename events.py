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

	def __str__(self):
		return "Element %s moved from %s to %s!" % tuple([repr(x) for x in
		       [self.element, self.from_field, self.to_field]])

class AttrChange(Event):
	def __init__(self, elem, type, attr_name, prev_value, cur_value):
		Event.__init__(self, elem, type)
		self.attr_name = attr_name
		self.prev_value, self.cur_value = prev_value, cur_value
	
	def __str__(self):
		return "Attribute %s in element %s changed from %s to %s!" % tuple([repr(x) for x in
		       [self.attr_name, self.element, self.prev_value, self.cur_value]])
