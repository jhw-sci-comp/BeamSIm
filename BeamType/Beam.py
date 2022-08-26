from abc import ABC
import math
import numpy as np

#Beam
class Beam(ABC):
	def __init__(self, length, height, width):
		self.__length = length
		self.__height = height
		self.__width = width
		self.__young_modulus = 0.0

	def getLength(self):
		return self.__length

	def setLength(self, length):
		self.__length = length
		

	def getHeight(self):
		return self.__height

	def setHeight(self, height):
		self.__height = height

	def getWidth(self):
		return self.__width	

	def setWidth(self, width):
		self.__width = width

	def getYoungModulus(self):
		return self.__young_modulus

	def setYoungModulus(self, young_modulus):
		self.__young_modulus = young_modulus

	
	def calculateBendingMoment(self, x_var, force_var):
		pass

	def calculateShearForce(self, x_var, force_var):
		pass

	def calculateMomentofArea(self): 
		return self.__width * math.pow(self.__height, 3)/12.0

	def calculateDisplacement(self, x_var, force_var):
		pass

	def calculateDisplacementDerivative(self, x_var, force_var):
		pass
	


#Simply supported beam
class SimplySupportedBeam(Beam):
	def __init__(self, length, height, width):
		super().__init__(length, height, width)

	def calculateBendingMoment(self, x_var, force_var):		
		y = []
		for x in x_var:
			if (x >= 0) and (x <= force_var.getXPos()):
				y.append( force_var.getValue()*(self.getLength()-force_var.getXPos())*x/self.getLength() )
			elif (x > force_var.getXPos()) and (x <= self.getLength()):
				y.append( force_var.getValue()*force_var.getXPos()*(self.getLength()-x)/self.getLength() )
		return y


	def calculateShearForce(self, x_var, force_var):
		y = []
		for x in x_var:
			if (x >= 0) and (x <= force_var.getXPos()):
				y.append( force_var.getValue()*(self.getLength()-force_var.getXPos())/self.getLength() )
			elif (x > force_var.getXPos()) and (x <= self.getLength()):
				y.append( force_var.getValue()*(self.getLength()-force_var.getXPos())/self.getLength()-force_var.getValue() )
		return y

	
	def calculateDisplacement(self, x_var, force_var):
		y = []
		for x in x_var:
			if (force_var.getXPos() < np.finfo(float).eps) or (abs(force_var.getXPos() - self.getLength()) < np.finfo(float).eps): 
				y.append(0.0)
			else:
				if (x >= 0) and (x <= force_var.getXPos()):
					y.append( -force_var.getValue() * (self.getLength()-force_var.getXPos()) * x * (math.pow(self.getLength(), 2) - math.pow((self.getLength()-force_var.getXPos()),2) - math.pow(x,2))/(6 * self.getLength() * self.getYoungModulus() * 1000000000 * self.calculateMomentofArea()) )
				elif (x > force_var.getXPos()) and (x <= self.getLength()):
					y.append( -force_var.getValue() * (self.getLength()-force_var.getXPos()) * x * (math.pow(self.getLength(), 2) - math.pow((self.getLength()-force_var.getXPos()),2) - math.pow(x,2))/(6 * self.getLength() * self.getYoungModulus() * 1000000000 * self.calculateMomentofArea()) - (force_var.getValue() * math.pow(x - force_var.getXPos(),3))/(6 * self.getYoungModulus() * 1000000000 * self.calculateMomentofArea()) )
		return y


	#Ableitung-Test
	def calculateDisplacementDerivative(self, x_var, force_var):
		y = []
		for x in x_var:
			if (force_var.getXPos() < np.finfo(float).eps) or (abs(force_var.getXPos() - self.getLength()) < np.finfo(float).eps): 
				y.append(0.0)
			else:
				if (x >= 0) and (x <= force_var.getXPos()):
					y.append( -force_var.getValue() * (self.getLength()-force_var.getXPos()) * (math.pow(self.getLength(), 2) - math.pow((self.getLength()-force_var.getXPos()),2) - 3 * math.pow(x,2)) /(6 * self.getLength() * self.getYoungModulus() * 1000000000 * self.calculateMomentofArea()) )
				elif (x > force_var.getXPos()) and (x <= self.getLength()):
					y.append( -force_var.getValue() * (self.getLength()-force_var.getXPos()) * (math.pow(self.getLength(), 2) - math.pow((self.getLength()-force_var.getXPos()),2) - 3 * math.pow(x,2)) /(6 * self.getLength() * self.getYoungModulus() * 1000000000 * self.calculateMomentofArea()) - (force_var.getValue() * math.pow(x - force_var.getXPos(),2))/(2 * self.getYoungModulus() * 1000000000 * self.calculateMomentofArea()) )
		return y



#Cantilever beam
class CantileverBeam(Beam):
	def __init__(self, length, height, width):
		super().__init__(length, height, width)

	def calculateBendingMoment(self, x_var, force_var):
		y = []
		for x in x_var:
			y.append(force_var.getValue()*(self.getLength() - x))
		return y


	def calculateShearForce(self, x_var, force_var):		
		return [force_var.getValue(), force_var.getValue()]


	def calculateDisplacement(self, x_var, force_var):
		y = []
		for x in x_var:
			y.append(-force_var.getValue() * math.pow(x, 2) * (3 * self.getLength() - x)/(6 * self.getYoungModulus() * 1000000000 * self.calculateMomentofArea()))
		return y

	
	#Ableitung-Test
	def calculateDisplacementDerivative(self, x_var, force_var):
		y = []
		for x in x_var:
			y.append(-force_var.getValue() * x * (2 * self.getLength() - x)/(2 * self.getYoungModulus() * 1000000000 * self.calculateMomentofArea()))
		return y

