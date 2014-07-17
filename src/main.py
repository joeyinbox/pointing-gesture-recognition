#!/usr/bin/python
from PyQt5 import QtWidgets
from classes.DatasetGui import *
from classes.LightDatasetGui import *
import sys



try:
	print str(sys.argv[1])
	
	# Create a new Dataset GUI window and display it
	app = QtWidgets.QApplication([])
	gui = LightDatasetGui()
	gui.show()

	app.exec_()
	
	
except IndexError:
	# Create a new Dataset GUI window and display it
	app = QtWidgets.QApplication([])
	gui = DatasetGui()
	gui.show()

	app.exec_()