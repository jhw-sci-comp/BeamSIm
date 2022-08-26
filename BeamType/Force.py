#Force
class Force:
	def __init__(self, value, x_pos):
		self.__value = value    #value of force in N
		self.__x_pos = x_pos    #position of force relative to the beam length

	def getValue(self):
		return self.__value

	def setValue(self, val):
		self.__value = val

	def getXPos(self):
		return self.__x_pos

	def setXPos(self, x_Pos):
		self.__x_pos = x_Pos