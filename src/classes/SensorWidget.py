#!/usr/bin/python
from PyQt5 import QtCore, QtWidgets



# Definition of the SensorWidget class to retrieve click events
class SensorWidget(QtWidgets.QLabel):
	
	# Register the signal
	clicked = QtCore.pyqtSignal(object)
	
	
	# Constructor of the SensorWidget class
	# 
	# @param	parent				Reference to the parent class to pass informations up
	# @return	None
	def __init(self, parent):
		QtWidgets.QLabel.__init__(self, parent)
	
	
	# Emits a mouseReleaseEvent event
	# 
	# @param	event				Event triggered after releasing a click within the widget
	# @return	None
	def mouseReleaseEvent(self, event):
		self.clicked.emit(event)