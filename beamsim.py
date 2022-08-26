from tkinter import * 
from tkinter import ttk
from tkinter.ttk import *

#from functools import partial  
#import numbers

#import math
#import numpy as np

#from BeamType import Beam, Force, BeamException, ForceException
from BeamDisplayFrame import BeamFrameControl, BeamFrameVisual
from BeamDisplayCanvas import CanvasBeam, CanvasPlot




if __name__ == "__main__":

	main_window = Tk(className = "Beam Bending Simulation")
	main_window.geometry("950x750")


	#Test-Beam
	beam = None

	#Test-Force
	force = None


	frame1 = BeamFrameControl.Frame_Control_Panel(main_window)
	frame1.grid(row=0, column=0)


	#-------------------------Test---------------------------
	frame2 = BeamFrameVisual.Frame_Visualization(main_window, frame1)
	frame2.grid(row=0, column=1, sticky=E+W+N+S)
	main_window.rowconfigure(0, weight=1)
	main_window.columnconfigure(1, weight=1)
	frame2.rowconfigure(1, weight=0)
	frame2.columnconfigure(0, weight=1)

	tab_beam = ttk.Frame(frame2) 
	tab_plot = ttk.Frame(frame2) 

	frame2.add(tab_beam, text ="Visualization") 
	frame2.add(tab_plot, text ="Data") 

	tab_beam.columnconfigure( 0, weight=1)
	tab_beam.rowconfigure(1, weight=1)
	tab_plot.columnconfigure( 0, weight=1)
	tab_plot.rowconfigure(1, weight=1)

	canv = CanvasBeam.Canvas_Beam(main_window, tab_beam, frame2)
	canv.grid(row=0, column=0, sticky=N+E+W)

	canvas1 = CanvasPlot.Canvas_Plot(main_window, tab_plot, frame2)
	canvas1.get_tk_widget().grid(row=0, column=0, sticky=N+S+E+W, padx=2)
	#-------------------------Test---------------------------

	frame1.getButton_ok().config(command = lambda: frame1.button_ok_pressed(canv, canvas1))

	frame1.getButton_cancel().config(command = lambda: frame1.button_cancel_pressed(canv, canvas1))

	main_window.mainloop()


