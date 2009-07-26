from event import *

class Move(Event):
	check_keys = ['from_field', 'to_field']

	def __init__(self, elem, before_after, from_field, to_field, condition = lambda x: True, query = False):
		Event.__init__(self, elem, before_after, condition, query)
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
	check_keys = ['attr_name', 'prev_value', 'next_value']

	def __init__(self, elem, before_after, attr_name, prev_value, next_value, condition = lambda x: True, query = False):
		Event.__init__(self, elem, before_after, condition, query)
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

class Create(Event):
	check_keys = []

	def __init__(self, before_after, elem = None, condition = lambda x: True, query = False):
		Event.__init__(self, elem, before_after, condition, query)

	def __str__(self):
		return "Element %s was added to the game" % repr(self.element)

	def hash_tuple(self):
		return (Create, self.before_after)

	def possible_hash_tuples(self):
		return [(Create, self.before_after)]

class Remove(Event):
	check_keys = []

	def __str__(self):
		return "Element %s was removed from the game" % repr(self.element)

	def hash_tuple(self):
		if self.element is not None:
			return (Remove, self.before_after, self.element)
		else:
			return (Remove, self.before_after)

	def possible_hash_tuples(self):
		return [(Remove, self.before_after),
		        (Remove, self.before_after, self.element)]
