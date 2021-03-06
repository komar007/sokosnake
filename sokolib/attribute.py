import events

class Attribute(object):
	def __init__(self, name):
		self.val = None
		self.name = name

	def __get__(self, obj, objtype = None):
		# FIXME: This is a common value for all elements with this attribute! Fix this error!
		return self.val

	def __set__(self, obj, val):
		old_val = self.val
		obj.game.send_callbacks(events.AttrChange(obj, 'before', self.name, old_val, val))
		self.val = val
		obj.game.send_callbacks(events.AttrChange(obj, 'after', self.name, old_val, val))

