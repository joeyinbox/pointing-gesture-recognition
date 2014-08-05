#!/usr/bin/python
from PyQt5 import QtWidgets
from classes.DatasetGui import *
from classes.LightDatasetGui import *
from classes.LiveGui import *
import sys



try:
	if str(sys.argv[1])=="light":
		# Create a new Light Dataset GUI window and display it
		app = QtWidgets.QApplication([])
		gui = LightDatasetGui()
		gui.show()

		app.exec_()
		
		
	else:
		# Create a new Dataset GUI window and display it
		app = QtWidgets.QApplication([])
		gui = DatasetGui()
		gui.show()

		app.exec_()
	
	
except IndexError:
	# Create a live GUI window and display it
	app = QtWidgets.QApplication([])
	gui = LiveGui()
	gui.show()

	app.exec_()