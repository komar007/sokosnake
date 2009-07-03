import re

class ParseError:
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class Parser:
	def __init__(self, element_hash):
		self.element_hash = element_hash

	def create_element(self, letter, x, y, params):
		try:
			klass = self.element_hash[letter]
			return klass(x, y, None, self.parse_params(params))
		except KeyError:
			raise ParseError("Unrecognized element character: '%c' at position (%i, %i)." %
							 (letter, x, y))

	def load(self, level_str):
		[self.header, self.map] = re.split(r'\n{2,}', level_str)
		[self.size_x, self.size_y] = [int(dim) for dim in re.split(r', *', self.header)]
		return (self.size_x, self.size_y)
	
	def parse(self):
		for y, line in enumerate(re.split('\n', self.map.strip())):
			for x, token in enumerate(re.split(r'(?<!\\) +', line.strip())):
				for (letter, params) in re.findall(r'([a-zA-Z-_])(?:\(([^()]+)\))?',
												   re.sub(r'\\ ', ' ', token)):
					yield self.create_element(letter, x, y, params)

	def parse_params(self, str):
		h = dict(re.findall(r'([^, ]+)=([^,]+)', str))
		return h
