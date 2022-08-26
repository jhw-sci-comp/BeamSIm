#Beam Exception 
class InputExceptionBeamMeasurements(Exception):
	def __init__(self, str):
		self.str = str


class InputExceptionBeamYoungModul(Exception):
	def __init__(self, str):
		self.str = str