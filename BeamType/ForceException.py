#Force Exception
class InputExceptionForceVal(Exception):
	def __init__(self, str):
		self.str = str

class InputExceptionForcePos(Exception):
	def __init__(self, str):
		self.str = str