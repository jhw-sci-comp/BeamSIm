from tkinter import * 
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class Canvas_Plot(FigureCanvasTkAgg):
	#def __init__(self, master_window_var, parent_widget_var, beam_obj_var, force_obj_var):
	def __init__(self, master_window_var, parent_widget_var, tabControl):
		self.__master_window = master_window_var
		self.__parent_widget = parent_widget_var
		self.__tabControl = tabControl
		#self.__beam_obj = beam_obj_var
		#self.__force_obj = force_obj_var

		self.__master_window.update_idletasks()
		#self.__figure1 = Figure(figsize=(4*self.__master_window.winfo_width()/500, 3*self.__master_window.winfo_height()/400), dpi=100)
		self.__figure1 = Figure(figsize=(4*self.__master_window.winfo_width()/500, self.__master_window.winfo_height()/80), dpi=80)
		self.__plot1 = self.__figure1.add_subplot(3, 1, 1)
		self.__plot1.axis("off")

		self.__plot2 = self.__figure1.add_subplot(3, 1, 2)
		self.__plot2.axis("off")

		self.__plot3 = self.__figure1.add_subplot(3, 1, 3)
		self.__plot3.axis("off")

		super().__init__(self.__figure1, self.__parent_widget)


	def getPlot1(self):
		return self.__plot1

	def getPlot2(self):
		return self.__plot2

	def getPlot3(self):
		return self.__plot3


	def canv_draw(self, beam_obj_var, force_obj_var):
		#if (self.__parent_widget.getFrame_control_panel().getButton_ok_clicked() == False) and (self.__parent_widget.getFrame_control_panel().getSsb_selected() == True):
		if (self.__tabControl.getFrame_control_panel().getButton_ok_clicked() == False) and (self.__tabControl.getFrame_control_panel().getSsb_selected() == True):
			#Plots zeichnen
			x = [ 0.0, force_obj_var.getXPos(), beam_obj_var.getLength() ]
			#y = [ 0.0, beam_obj_var.calculateBendingMoment(force_obj_var.getXPos(), force_obj_var), 0.0 ]
			self.__plot1.axis("on")
			self.__plot1.grid(True)			
			
			self.__plot1.plot(x, beam_obj_var.calculateBendingMoment(x, force_obj_var), color='magenta')
			self.__plot1.axvline(x=force_obj_var.getXPos(), color='green', ls=':', label='axvline - full height')
			self.__plot1.set_xlabel("x [m]")
			self.__plot1.set_ylabel("Bending moment M(x) [Nm]")
			
			x = [ 0.0, force_obj_var.getXPos(), beam_obj_var.getLength() ]
			#y = [ beam_obj_var.calculateShearForce(0.0, force_obj_var),beam_obj_var.calculateShearForce(force_obj_var.getXPos(), force_obj_var), beam_obj_var.calculateShearForce(beam_obj_var.getLength(), force_obj_var) ]
			self.__plot2.axis("on")
			self.__plot2.grid(True)
			
			self.__plot2.step(x, beam_obj_var.calculateShearForce(x, force_obj_var), color='red')
			self.__plot2.axvline(x=force_obj_var.getXPos(), color='green', ls=':', label='axvline - full height')
			self.__plot2.set_xlabel("x [m]")
			self.__plot2.set_ylabel("Shear force Q(x) [N]")

			
			x = np.arange(0.0, beam_obj_var.getLength(), 0.1)
			x = np.append(x, beam_obj_var.getLength())
			self.__plot3.axis("on")
			self.__plot3.grid(True)

			self.__plot3.plot(x, beam_obj_var.calculateDisplacement(x, force_obj_var), color='blue')
			self.__plot3.axvline(x=force_obj_var.getXPos(), color='green', ls=':', label='axvline - full height')
			self.__plot3.set_xlabel("x [m]")
			self.__plot3.set_ylabel("Displacement w(x) [m]")

			self.draw()

		#elif (self.__parent_widget.getFrame_control_panel().getButton_ok_clicked() == False) and (self.__parent_widget.getFrame_control_panel().getCb_selected() == True):
		elif (self.__tabControl.getFrame_control_panel().getButton_ok_clicked() == False) and (self.__tabControl.getFrame_control_panel().getCb_selected() == True):
			x = [ 0.0, beam_obj_var.getLength() ]			
			self.__plot1.axis("on")
			self.__plot1.grid(True)
						
			self.__plot1.plot(x, beam_obj_var.calculateBendingMoment(x, force_obj_var), color='magenta')
			self.__plot1.axvline(x=force_obj_var.getXPos(), color='green', ls=':', label='axvline - full height')
			self.__plot1.set_xlabel("x [m]")
			self.__plot1.set_ylabel("Bending moment M(x) [Nm]")
			
			x = [ 0.0, beam_obj_var.getLength() ]			
			self.__plot2.axis("on")
			self.__plot2.grid(True)
			
			self.__plot2.plot(x, beam_obj_var.calculateShearForce(x, force_obj_var), color='red')
			self.__plot2.axvline(x=force_obj_var.getXPos(), color='green', ls=':', label='axvline - full height')
			self.__plot2.set_xlabel("x [m]")
			self.__plot2.set_ylabel("Shear force Q(x) [N]")
			
			
			x = np.arange(0.0, beam_obj_var.getLength(), 0.1)
			x = np.append(x, beam_obj_var.getLength())
			
			self.__plot3.axis("on")
			self.__plot3.grid(True)

			self.__plot3.plot(x, beam_obj_var.calculateDisplacement(x, force_obj_var), color='blue')
			self.__plot3.axvline(x=force_obj_var.getXPos(), color='green', ls=':', label='axvline - full height')
			self.__plot3.set_xlabel("x [m]")
			self.__plot3.set_ylabel("Displacement w(x) [m]")

			self.draw()
