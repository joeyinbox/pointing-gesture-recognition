#!/usr/bin/python
from PyQt5 import QtCore, QtWidgets


# Subclass QLabel to retrieve click events
class SensorWidget(QtWidgets.QLabel):
	# Register the signal
	clicked = QtCore.pyqtSignal(object)
	
	def __init(self, parent):
		QtWidgets.QLabel.__init__(self, parent)
		
	def mouseReleaseEvent(self, event):
		self.clicked.emit(event)