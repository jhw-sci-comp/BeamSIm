from tkinter import * 
from tkinter import ttk
from tkinter.ttk import *
from BeamType import Beam, Force, BeamException, ForceException
from tkinter import messagebox



class Frame_Control_Panel(Frame):
	def __init__(self, master_window_var):
		self.__master_window = master_window_var
		#self.__canvas_image = canvas_image_var
		#self.__canvas_plot = canvas_plot_var

		self.__button_ok_clicked = False  # vielleicht public oder protected machen?????
		self.__ssb_selected = False
		self.__cb_selected = False

		super().__init__(self.__master_window, borderwidth = 20)

		#beam
		self.__label_beam_selection = Label(self, text="Beam type:")
		self.__label_beam_selection.grid(row=0, column=0)

		beam_list = ["Simply supported beam", "Cantilever beam"]
		self.__beam_selection = ttk.Combobox(self, values = beam_list, state = "readonly")
		self.__beam_selection.grid(row=0, column=1, pady=10)
		self.__beam_selection.bind("<<ComboboxSelected>>", self.selectBeam)

		self.__label_length = Label(self, text = "Beam length (m):", state = "disabled")
		self.__label_length.grid(row=1, column=0)

		self.__entry_length = Entry(self, state = "disabled")
		self.__entry_length.grid(row=1, column=1, pady=10)

		self.__label_height = Label(self, text = "Beam height (m):", state = "disabled")
		self.__label_height.grid(row=2, column=0)

		self.__entry_height = Entry(self, state = "disabled")
		self.__entry_height.grid(row=2, column=1, pady=10)

		self.__label_width = Label(self, text = "Beam width (m):", state = "disabled")
		self.__label_width.grid(row=3, column=0)

		self.__entry_width = Entry(self, state = "disabled")
		self.__entry_width.grid(row=3, column=1, pady=10)

		
		#force
		self.__label_force_val = Label(self, text = "Force value (N):", state = "disabled")
		self.__label_force_val.grid(row=4, column=0)

		self.__entry_force_val = Entry(self, state = "disabled")
		self.__entry_force_val.grid(row=4, column=1, pady=10)

		self.__label_force_pos = Label(self, text = "Force position (m):", state = "disabled")
		self.__label_force_pos.grid(row=5, column=0)

		self.__entry_force_pos = Entry(self, state = "disabled")
		self.__entry_force_pos.grid(row=5, column=1, pady=10)

		
		#Material
		self.__label_young_modulus = Label(self, text = "Young's modulus (GPa):", state = "disabled")
		self.__label_young_modulus.grid(row=6, column=0, pady=10)

		self.__entry_young_modulus = Entry(self, state = "disabled")
		self.__entry_young_modulus.grid(row=6, column=1, pady=10)

		
		#control
		self.__button_ok = Button(self, text="Ok", state="disabled")
		self.__button_ok.grid(row=7, column=0, pady=10)
				
		self.__button_cancel = Button(self, text="Cancel", state="disabled")
		self.__button_cancel.grid(row=7, column=1, pady=10)
		

	
	def getButton_ok(self):
		return self.__button_ok


	def getButton_cancel(self):
		return self.__button_cancel


	def getBeam_selection(self):
		return self.__beam_selection

	
	def getButton_ok_clicked(self):
		return self.__button_ok_clicked

	def setButton_ok_clicked(self, val):
		self.__button_ok_clicked = val

	def getSsb_selected(self):
		return self.__ssb_selected

	def setSsb_selected(self, val):
		self.__ssb_selected = val

	def getCb_selected(self):
		return self.__cb_selected

	def setCb_selected(self, val):
		self.__cb_selected = val


	def selectBeam(self, event):
		global beam
		global force

		force = Force.Force(0,0)
		
		if self.__beam_selection.get() == "Simply supported beam":
			beam = Beam.SimplySupportedBeam(1, 0.2, 0.1)
			
			self.__button_ok.config(state="active")
			self.__label_length.config(state="active")
			self.__entry_length.config(state="active")
			self.__label_height.config(state="active")
			self.__entry_height.config(state="active")
			self.__label_width.config(state="active")
			self.__entry_width.config(state="active")
			self.__label_force_val.config(state="active")
			self.__entry_force_val.config(state="active")
			self.__label_force_pos.config(state="active")
			self.__entry_force_pos.config(state="active")
			self.__label_young_modulus.config(state="active")
			self.__entry_young_modulus.config(state="active")

			self.__ssb_selected = True
			self.__cb_selected = False

		elif self.__beam_selection.get() == "Cantilever beam":
			beam = Beam.CantileverBeam(1, 0.2, 0.1)
			
			self.__button_ok.config(state="active")
			self.__label_length.config(state="active")
			self.__entry_length.config(state="active")
			self.__label_height.config(state="active")
			self.__entry_height.config(state="active")
			self.__label_width.config(state="active")
			self.__entry_width.config(state="active")
			self.__label_force_val.config(state="active")
			self.__entry_force_val.config(state="active")
			self.__label_force_pos.config(state="disabled")
			self.__entry_force_pos.config(state="disabled")
			self.__label_young_modulus.config(state="active")
			self.__entry_young_modulus.config(state="active")

			self.__cb_selected = True
			self.__ssb_selected = False


	
	def button_ok_pressed(self, canvas_image, canvas_plot):
		global beam
		global force

		try:
			length = self.__entry_length.get()
			height = self.__entry_height.get()
			width  = self.__entry_width.get()
			young_modulus = self.__entry_young_modulus.get()
			force_val = self.__entry_force_val.get()
			force_pos = self.__entry_force_pos.get()

			
			if ((length.replace('.','',1).isdigit() == False) or (len(length) == 0) or (float(length) <= 0.0)):
				raise BeamException.InputExceptionBeamMeasurements("length")

			if ((height.replace('.','',1).isdigit() == False) or len(height) == 0) or (float(height) <= 0.0):
				raise BeamException.InputExceptionBeamMeasurements("height")

			if ((width.replace('.','',1).isdigit() == False) or len(width) == 0) or (float(width) <= 0.0):
				raise BeamException.InputExceptionBeamMeasurements("width")

			if ((young_modulus.replace('.','',1).isdigit() == False) or len(young_modulus) == 0) or (float(young_modulus) <= 0.0):
				raise BeamException.InputExceptionBeamYoungModul("Young's modulus")

			if ((force_val.replace('.','',1).isdigit() == False) or len(force_val) == 0) or (float(force_val) < 0.0):
				raise ForceException.InputExceptionForceVal("Force value")

			beam.setLength(float(length))
			beam.setHeight(float(height))
			beam.setWidth(float(width))
			beam.setYoungModulus(float(young_modulus))
			force.setValue(float(force_val))
		
			
			if isinstance(beam, Beam.CantileverBeam):
				force.setXPos(float(length))
			else:
				if ((force_pos.replace('.','',1).isdigit() == False) or len(force_pos) == 0) or (float(force_pos) < 0.0) or (float(force_pos) > float(length)):
					raise ForceException.InputExceptionForcePos("Force position")
				force.setXPos(float(force_pos))
			
			  
			canvas_image.canv_draw(beam, force)
			canvas_plot.canv_draw(beam, force)

			self.__button_ok_clicked = True

			self.__beam_selection.config(state="disabled")
			self.__button_ok.config(state="disabled")
			self.__entry_length.config(state="disabled")
			self.__label_length.config(state="disabled")
			self.__label_beam_selection.config(state="disabled")
			self.__label_height.config(state="disabled")
			self.__entry_height.config(state="disabled")
			self.__label_width.config(state="disabled")
			self.__entry_width.config(state="disabled")
			self.__label_force_val.config(state="disabled")
			self.__entry_force_val.config(state="disabled")
			self.__label_force_pos.config(state="disabled")
			self.__entry_force_pos.config(state="disabled")
			self.__label_young_modulus.config(state="disabled")
			self.__entry_young_modulus.config(state="disabled")
			self.__button_cancel.config(state="active")
			
			
			canvas_image.bind("<Configure>", lambda event: canvas_image.canv_redraw(event, beam, force))

		except BeamException.InputExceptionBeamMeasurements as e:
			messagebox.showinfo("Input Exception", "Beam " + e.str + " expects a numeric value greater than 0.")
		except BeamException.InputExceptionBeamYoungModul as e:
			messagebox.showinfo("Input Exception", e.str + " expects a numeric value greater than 0.")
		except ForceException.InputExceptionForceVal as e:
			messagebox.showinfo("Input Exception", e.str + " expects a numeric value greater than or equal to 0.")
		except ForceException.InputExceptionForcePos as e:
			messagebox.showinfo("Input Exception", e.str + " expects a numeric value greater than 0 and smaller than or equal to beam length.")


	def button_cancel_pressed(self, canvas_image, canvas_plot):
		#global ssb_selected
		#global cb_selected
		#global button_ok_clicked
		
		canvas_image.delete("all")
		canvas_plot.getPlot1().cla()
		canvas_plot.getPlot1().axis("off")
		canvas_plot.getPlot2().cla()
		canvas_plot.getPlot2().axis("off")
		canvas_plot.getPlot3().cla()
		canvas_plot.getPlot3().axis("off")
		canvas_plot.draw()
		
		self.__label_beam_selection.config(state="active")
		self.__beam_selection.config(state="active")
		self.__button_ok.config(state="disabled")
		self.__button_cancel.config(state="disabled")
		#self.__entry_length.config(state="disabled")
		#self.__label_length.config(state="disabled")

		self.__ssb_selected = False
		self.__button_ok_clicked = False		
		self.__cb_selected = False
		
