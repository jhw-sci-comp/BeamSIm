from tkinter import ttk
from tkinter.ttk import *

class Frame_Visualization(Notebook):
	def __init__(self, master_window, frame_control_panel_var):
		self.__frame_control_panel = frame_control_panel_var
		super().__init__(master_window)


	def getFrame_control_panel(self):
		return self.__frame_control_panel	