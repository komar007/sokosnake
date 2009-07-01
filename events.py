class Event(object):
	def __init__(self, elem, before_after, query = False):
		self.element = elem
		if before_after in ['before', 'after']:
			self.before_after = before_after
		else:
			raise TypeError("Event before_after must be either 'before' or 'after'")

	def match(self, event):
		return all(val is None or val == event.__dict__[key] for key, val in
				zip(self.__dict__.keys(), self.__dict__.values()))

	def hash_tuple(self):
		pass

	def possible_hash_tuples(self):
		pass
	
class Move(Event):
	def __init__(self, elem, before_after, from_field, to_field, query = False):
		Event.__init__(self, elem, before_after, query)
		self.from_field = from_field
		self.to_field = to_field

	def __str__(self):
		return "Element %s moved from %s to %s!" % tuple([repr(x) for x in
		       [self.element, self.from_field, self.to_field]])

	def hash_tuple(self):
		if all(x is None for x in [self.to_field, self.from_field, self.element]):
			raise TypeError("At least one of from_field, to_field, element must be set!")

		if self.element is not None:
			return (Move, self.before_after, self.element)

		if self.to_field is not None:
			x, y = self.to_field
			from_to = 'to'
		else:
			x, y = self.from_field
			from_to = 'from'

		return (Move, self.before_after, from_to, x, y)
	
	def possible_hash_tuples(self):
		return [(Move, self.before_after, self.element),
		        (Move, self.before_after, 'from', self.from_field[0], self.from_field[1]),
		        (Move, self.before_after, 'to', self.to_field[0], self.to_field[1])]


class AttrChange(Event):
	def __init__(self, elem, before_after, attr_name, prev_value, next_value, query = False):
		Event.__init__(self, elem, before_after, query)
		self.attr_name = attr_name
		self.prev_value, self.next_value = prev_value, next_value
	
	def __str__(self):
		return "Attribute %s in element %s changed from %s to %s!" % tuple([repr(x) for x in
		       [self.attr_name, self.element, self.prev_value, self.next_value]])

	def hash_tuple(self):
		if self.element is not None:
			if self.attr_name is not None:
				return (AttrChange, self.before_after, self.element, self.attr_name)
			else:
				return (AttrChange, self.before_after, self.element)
		else:
			raise TypeError("AttrChange currently does not support queries without explicit element")
	
	def possible_hash_tuples(self):
		return [(AttrChange, self.before_after, self.element),
		        (AttrChange, self.before_after, self.element, self.attr_name)]
