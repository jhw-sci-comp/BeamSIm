from tkinter import * 
import numpy as np
import math


class Canvas_Beam(Canvas):
	def __init__(self, master_window_var, parent_widget_var, tabControl):
		self.__master_window = master_window_var
		self.__parent_widget = parent_widget_var
		self.__tabControl = tabControl
		
		self.__master_window.update_idletasks()
		canvas_width  = 4 * self.__master_window.winfo_width()/5
		#canvas_height = self.__master_window.winfo_height()/4
		canvas_height = self.__master_window.winfo_height()

		super().__init__(self.__parent_widget, bg = "white", height = canvas_height, width = canvas_width)


	def getParent_widget(self):
		return self.__parent_widget


	def transformCoord2(self, coord_tuple):
		transformed_coord = (coord_tuple[0] + 0.1 * self.winfo_width(), self.winfo_height()/2.0 - coord_tuple[1])
		return transformed_coord




	def canv_draw(self, beam_obj_var, force_obj_var):				
			
		#if (self.__parent_widget.getFrame_control_panel().getButton_ok_clicked() == False) and (self.__parent_widget.getFrame_control_panel().getSsb_selected() == True):
		if (self.__tabControl.getFrame_control_panel().getButton_ok_clicked() == False) and (self.__tabControl.getFrame_control_panel().getSsb_selected() == True):
			x0y0 = self.transformCoord2((0.0, 0.0))
			x1y1 = self.transformCoord2((0.8 * self.winfo_width(), beam_obj_var.getHeight() * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			self.create_rectangle(x0y0, x1y1, outline="grey", dash = (1,1))


			x = np.arange(0.0, beam_obj_var.getLength(), 0.01)
			x = np.append(x, beam_obj_var.getLength())

			y = beam_obj_var.calculateDisplacement(x, force_obj_var)
			y_div = beam_obj_var.calculateDisplacementDerivative(x, force_obj_var)
			control_points = [(0.1 * self.winfo_width(), self.winfo_height()/2)]
		
		
			for i in range(0, len(x)-1):
				#if((y_div[i] - y_div[i+1]) == 0.0):
				if((y_div[i] - y_div[i+1]) < np.finfo(float).eps):
					x_p = (x[i] + x[i+1])/2.0
				else:					
					x_p = (y[i+1] - y[i] + y_div[i] * x[i] - y_div[i+1] * x[i+1])/(y_div[i] - y_div[i+1]) 
				y_p = y_div[i+1] * (x_p - x[i+1]) + y[i+1]
				control_points.append((x_p * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-y_p * 0.8 * self.winfo_width()/beam_obj_var.getLength())))
			control_points.append((x[len(x)-1] * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-y[len(x)-1] * 0.8 * self.winfo_width()/beam_obj_var.getLength())))
				
			self.create_line(control_points, smooth=1)

			

			#linke Seite
			x_up_left = x[0] - beam_obj_var.getHeight() * y_div[0]
			#if y_div[0] == 0.0:
			if y_div[0] < np.finfo(float).eps:
				y_up_left = y[0] + beam_obj_var.getHeight()
			else:
				y_up_left = (x[0] - x_up_left)/y_div[0] + y[0]
			self.create_line((x[0] * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-y[0] * 0.8 * self.winfo_width()/beam_obj_var.getLength())), (x_up_left * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 - (y_up_left * 0.8 * self.winfo_width()/beam_obj_var.getLength())))

			#rechte Seite
			x_up_right = x[len(x)-1] - beam_obj_var.getHeight() * y_div[len(x)-1]
			#if y_div[len(x)-1] == 0.0:
			if y_div[len(x)-1] < np.finfo(float).eps:
				y_up_right = y[len(x)-1] + beam_obj_var.getHeight()
			else:
				y_up_right = (x[len(x)-1] - x_up_right)/y_div[len(x)-1] + y[len(x)-1]
			self.create_line((x[len(x)-1] * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-y[len(x)-1] * 0.8 * self.winfo_width()/beam_obj_var.getLength())), (x_up_right * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 - (y_up_right * 0.8 * self.winfo_width()/beam_obj_var.getLength())))
			
			
			#j=0
			#k=0

			#obere Balkenfläche
			x_up = [x_up_left]
			y_up = [y_up_left]
			for i in range(1, len(x)-1):
				x_up = np.append(x_up, x[i] - beam_obj_var.getHeight() * y_div[i])				
				#if y_div[i] == 0.0:
				if y_div[i] < np.finfo(float).eps:
					#j=j+1
					y_up = np.append(y_up, y[i] + beam_obj_var.getHeight())
				else:
					#k=k+1
					y_up = np.append(y_up, (x[i] - x_up[i])/y_div[i] + y[i])
					#print("y_div[i]: ", y_div[i], " eps: ", np.finfo(float).eps)
				
			x_up = np.append(x_up, x_up_right)
			y_up = np.append(y_up, y_up_right)
			

			#print("j: ",j)
			#print("k: ",k)

			#print("x_up: ", x_up)
			#print("y: ", y)
			#print("y_up: ", y_up)

			#print("y_div: ", y_div)

			
			control_points = [(x_up[0] * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-y_up[0] * 0.8 * self.winfo_width()/beam_obj_var.getLength()))]
			for i in range(0, len(x_up)-1):
				#if((y_div[i] - y_div[i+1]) == 0.0):
				if((y_div[i] - y_div[i+1]) < np.finfo(float).eps):
					x_p = (x_up[i] + x_up[i+1])/2.0
				else:
					x_p = (y_up[i+1] - y_up[i] + y_div[i] * x_up[i] - y_div[i+1] * x_up[i+1])/(y_div[i] - y_div[i+1]) 
				y_p = y_div[i+1] * (x_p - x_up[i+1]) + y_up[i+1]
				control_points.append((x_p * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-y_p * 0.8 * self.winfo_width()/beam_obj_var.getLength())))
			control_points.append((x_up[len(x_up)-1] * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-y_up[len(x_up)-1] * 0.8 * self.winfo_width()/beam_obj_var.getLength())))
				
			self.create_line(control_points, smooth=1)			

			
			a = self.transformCoord2((-0.12 * 0.8 * self.winfo_width()/beam_obj_var.getLength(), -0.2 * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			b = self.transformCoord2((0.12 * 0.8 * self.winfo_width()/beam_obj_var.getLength(), -0.2 * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			c = self.transformCoord2((0.0, 0.0))
			self.create_polygon(a, b, c, fill = "grey60", outline = "black")			
			
			
			d = self.transformCoord2((-0.18 * 0.8 * self.winfo_width()/beam_obj_var.getLength(), -0.22 * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			e = self.transformCoord2((0.18 * 0.8 * self.winfo_width()/beam_obj_var.getLength(), -0.2 * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			self.create_rectangle(d, e, fill = "black")
			for i in range(1,13):
				f = self.transformCoord2(((-0.21 + i * 0.03) * 0.8 * self.winfo_width()/beam_obj_var.getLength(),-0.27 * 0.8 * self.winfo_width()/beam_obj_var.getLength())) 
				g = self.transformCoord2(((-0.18 + i * 0.03) * 0.8 * self.winfo_width()/beam_obj_var.getLength(),-0.22 * 0.8 * self.winfo_width()/beam_obj_var.getLength())) 				
				self.create_line(f, g)
		

			a = self.transformCoord2(((beam_obj_var.getLength() - 0.12) * 0.8 * self.winfo_width()/beam_obj_var.getLength(), -0.2 * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			b = self.transformCoord2(((beam_obj_var.getLength() + 0.12) * 0.8 * self.winfo_width()/beam_obj_var.getLength(), -0.2 * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			c = self.transformCoord2((0.8 * self.winfo_width(), 0.0))
			self.create_polygon(a,b,c, fill = "grey60", outline = "black")

			
			d = self.transformCoord2(((beam_obj_var.getLength() - 0.18) * 0.8 * self.winfo_width()/beam_obj_var.getLength(), -0.22 * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			e = self.transformCoord2(((beam_obj_var.getLength() + 0.18) * 0.8 * self.winfo_width()/beam_obj_var.getLength(), -0.2 * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			self.create_rectangle(d, e, fill="black")
			for i in range(1,13):
				f = self.transformCoord2(((beam_obj_var.getLength()-0.21 + i * 0.03) * 0.8 * self.winfo_width()/beam_obj_var.getLength(),-0.27 * 0.8 * self.winfo_width()/beam_obj_var.getLength())) 
				g = self.transformCoord2(((beam_obj_var.getLength()-0.18 + i * 0.03) * 0.8 * self.winfo_width()/beam_obj_var.getLength(),-0.22 * 0.8 * self.winfo_width()/beam_obj_var.getLength())) 				
				self.create_line(f, g)
			
			
			#Kraft zeichnen			
			a = self.transformCoord2(((force_obj_var.getXPos() - 0.03) * 0.8 * self.winfo_width()/beam_obj_var.getLength(), (beam_obj_var.getHeight() + 0.12) * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			b = self.transformCoord2(((force_obj_var.getXPos() + 0.03) * 0.8 * self.winfo_width()/beam_obj_var.getLength(), (beam_obj_var.getHeight() + 0.12) * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			c = self.transformCoord2((force_obj_var.getXPos() * 0.8 * self.winfo_width()/beam_obj_var.getLength(), beam_obj_var.getHeight() * 0.8 * self.winfo_width()/beam_obj_var.getLength()))		
			self.create_polygon(a, b, c, fill = "green", outline = "green")

			d = self.transformCoord2(((force_obj_var.getXPos() - 0.005) * 0.8 * self.winfo_width()/beam_obj_var.getLength(), (beam_obj_var.getHeight() + 0.12) * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			e = self.transformCoord2(((force_obj_var.getXPos() + 0.005) * 0.8 * self.winfo_width()/beam_obj_var.getLength(), (beam_obj_var.getHeight() + 0.24) * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			self.create_rectangle(d, e,fill="green", outline="green")

		#elif (self.__parent_widget.getFrame_control_panel().getButton_ok_clicked() == False) and (self.__parent_widget.getFrame_control_panel().getCb_selected() == True):
		elif (self.__tabControl.getFrame_control_panel().getButton_ok_clicked() == False) and (self.__tabControl.getFrame_control_panel().getCb_selected() == True):
			#x0y0 = (0.1 * self.winfo_width(), self.winfo_height()/2)
			#x1y1 = (0.9 * self.winfo_width(), self.winfo_height()/2 - beam_obj_var.getHeight() * 0.8 * self.winfo_width()/beam_obj_var.getLength())
			#self.create_rectangle(x0y0, x1y1, outline="grey", dash = (1,1))

			x0y0 = self.transformCoord2((0.0, 0.0))
			x1y1 = self.transformCoord2((0.8 * self.winfo_width(), beam_obj_var.getHeight() * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			self.create_rectangle(x0y0, x1y1, outline="grey", dash = (1,1))

			x = np.arange(0.0, beam_obj_var.getLength(), 0.01)
			x = np.append(x, beam_obj_var.getLength())

			y = beam_obj_var.calculateDisplacement(x, force_obj_var)
			y_div = beam_obj_var.calculateDisplacementDerivative(x, force_obj_var)
			control_points = [(0.1 * self.winfo_width(), self.winfo_height()/2 - (beam_obj_var.getHeight() * 0.8 * self.winfo_width()/beam_obj_var.getLength()))]

			for i in range(0, len(x)-1):
				if((y_div[i] - y_div[i+1]) == 0.0):
					x_p = (x[i] + x[i+1])/2.0
				else:
					x_p = (y[i+1] - y[i] + y_div[i] * x[i] - y_div[i+1] * x[i+1])/(y_div[i] - y_div[i+1]) 
				y_p = y_div[i+1] * (x_p - x[i+1]) + y[i+1]				
				control_points.append((x_p * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-(y_p + beam_obj_var.getHeight()) * 0.8 * self.winfo_width()/beam_obj_var.getLength())))
			control_points.append((x[len(x)-1] * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-(y[len(x)-1] + beam_obj_var.getHeight()) * 0.8 * self.winfo_width()/beam_obj_var.getLength())))
				
			self.create_line(control_points, smooth=1)
			

			#rechte Seite
			x_lower_right = x[len(x)-1] + beam_obj_var.getHeight() * y_div[len(x)-1]
			if y_div[len(x)-1] < np.finfo(float).eps:
				y_lower_right = y[len(x)-1] - beam_obj_var.getHeight()
			else:
				y_lower_right = (x[len(x)-1] - x_lower_right)/y_div[len(x)-1] + y[len(x)-1]
			self.create_line((x[len(x)-1] * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-(y[len(x)-1] + beam_obj_var.getHeight()) * 0.8 * self.winfo_width()/beam_obj_var.getLength())), (x_lower_right * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 - ((y_lower_right + beam_obj_var.getHeight()) * 0.8 * self.winfo_width()/beam_obj_var.getLength())))

			
			#untere Balkenfläche
			x_lower = [x[0]]
			y_lower = [-beam_obj_var.getHeight()]
			for i in range(1, len(x)-1):
				x_lower = np.append(x_lower, x[i] + beam_obj_var.getHeight() * y_div[i])				
				#if y_div[i] == 0.0:
				if y_div[i] < np.finfo(float).eps:
					y_lower = np.append(y_lower, y[i] - beam_obj_var.getHeight())
				else:
					y_lower = np.append(y_lower, (x[i] - x_lower[i])/y_div[i] + y[i])
				
			x_lower = np.append(x_lower, x_lower_right)
			y_lower = np.append(y_lower, y_lower_right)			
			
						
			control_points = [(x_lower[0] * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-(y_lower[0] + beam_obj_var.getHeight()) * 0.8 * self.winfo_width()/beam_obj_var.getLength()))]
			for i in range(0, len(x_lower)-1):
				#if((y_div[i] - y_div[i+1]) == 0.0):
				if((y_div[i] - y_div[i+1]) < np.finfo(float).eps):
					x_p = (x_lower[i] + x_lower[i+1])/2.0
				else:
					x_p = (y_lower[i+1] - y_lower[i] + y_div[i] * x_lower[i] - y_div[i+1] * x_lower[i+1])/(y_div[i] - y_div[i+1]) 				
				y_p = y_div[i+1] * (x_p - x_lower[i+1]) + y_lower[i+1]
				control_points.append((x_p * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-(y_p + beam_obj_var.getHeight()) * 0.8 * self.winfo_width()/beam_obj_var.getLength())))
			control_points.append((x_lower[len(x_lower)-1] * 0.8 * self.winfo_width() /beam_obj_var.getLength() + 0.1 * self.winfo_width(), self.winfo_height()/2 + (-(y_lower[len(x_lower)-1] + beam_obj_var.getHeight()) * 0.8 * self.winfo_width()/beam_obj_var.getLength())))
						
			self.create_line(control_points, smooth=1)

			
			#a = (0.095 * self.winfo_width(), self.winfo_height()/2 + 0.2 * 0.8 * self.winfo_width()/beam_obj_var.getLength())
			#b = (0.1 * self.winfo_width(), self.winfo_height()/2 - (beam_obj_var.getHeight() + 0.2) * 0.8 * self.winfo_width()/beam_obj_var.getLength())

			a = self.transformCoord2((-0.005 * self.winfo_width(), (beam_obj_var.getHeight() + 0.2) * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			b = self.transformCoord2((0.0, -0.2 * 0.8 * self.winfo_width()/beam_obj_var.getLength()))
			self.create_rectangle(a, b, fill = "black")

			for i in range(1, math.ceil((beam_obj_var.getHeight() + 0.4)/0.05)):
				f = (0.085 * self.winfo_width(), self.winfo_height()/2 - (beam_obj_var.getHeight() + 0.25 - i * 0.05) * 0.8 * self.winfo_width()/beam_obj_var.getLength())
				g = (0.095 * self.winfo_width(), self.winfo_height()/2 - (beam_obj_var.getHeight() + 0.2 - i * 0.05) * 0.8 * self.winfo_width()/beam_obj_var.getLength())
				self.create_line(f, g)
			
			x0y0 = ( 0.901 * self.winfo_width(), self.winfo_height()/2 - (beam_obj_var.getHeight() + 0.25) * 0.8 * self.winfo_width()/beam_obj_var.getLength())
			x1y1 = ( 0.899 * self.winfo_width(), self.winfo_height()/2 - (beam_obj_var.getHeight() + 0.45) * 0.8 * self.winfo_width()/beam_obj_var.getLength())
			self.create_rectangle(x0y0, x1y1, fill = "green", outline = "green")

			c = (0.908 * self.winfo_width(), self.winfo_height()/2 - (beam_obj_var.getHeight() + 0.25) * 0.8 * self.winfo_width()/beam_obj_var.getLength())
			d = (0.892 * self.winfo_width(), self.winfo_height()/2 - (beam_obj_var.getHeight() + 0.25) * 0.8 * self.winfo_width()/beam_obj_var.getLength())
			e = (0.9 * self.winfo_width(), self.winfo_height()/2 - beam_obj_var.getHeight() * 0.8 * self.winfo_width()/beam_obj_var.getLength())
			self.create_polygon(c, d, e, fill = "green", outline = "green")


	def canv_redraw(self, event, beam_obj, force_obj):
		#global beam
		#global force

		self.delete("all")	
		self.__master_window.update_idletasks()
		#self.config(width=4*self.__master_window.winfo_height()/5, height=self.__master_window.winfo_height()/4)
		self.config(width=4*self.__master_window.winfo_height()/5, height=self.__master_window.winfo_height())

		if (self.__tabControl.getFrame_control_panel().getButton_ok_clicked() == True):
			self.__tabControl.getFrame_control_panel().setButton_ok_clicked(False)
			#self.canv_draw(beam, force)
			self.canv_draw(beam_obj, force_obj)	
			self.__tabControl.getFrame_control_panel().setButton_ok_clicked(True)
		