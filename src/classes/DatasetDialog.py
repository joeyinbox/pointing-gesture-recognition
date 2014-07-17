#! /usr/bin/python
import functools, hand, ui
from PyQt5 import QtCore, QtWidgets
from copy import deepcopy

from classes.SensorWidget import *


# Display a dialog window to prompt the finger tip position
class DatasetDialog(QtWidgets.QDialog):
	def __init__(self, parent=None):
		super(DatasetDialog, self).__init__(parent)
		self.parent = parent
		self.setWindowTitle("Indicate the pointing finger tip position")
		
		self.layout = QtWidgets.QVBoxLayout(self)
		
		# Reserve some space for the depth image
		self.depthImage = SensorWidget()
		self.depthImage.setGeometry(10, 10, 640, 480)
		
		# Register action for the depth image
		action = functools.partial(self.imageClicked, self.depthImage)
		self.depthImage.clicked.connect(action)
		
		
		# Create OK|Cancel buttons
		self.buttonBox = QtWidgets.QDialogButtonBox(self)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
		
		# Register actions for the buttons
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept)
		
		hlayout = QtWidgets.QHBoxLayout()
		self.pickedDepth = QtWidgets.QLabel("")
		
		hlayout.addWidget(self.pickedDepth)
		hlayout.addWidget(self.buttonBox)
		
		
		# Insert all elements to the layout
		self.layout.addWidget(self.depthImage)
		self.layout.addLayout(hlayout)
		
		
		# This will assert that the image has been clicked before saving
		self.fingerTip = []
		
		
		# If the user hit the save button without pointing the finger, display an alert
		self.messageBox = QtWidgets.QMessageBox()
		self.messageBox.setText("Please, indicate the position of the pointing finger tip by clicking the depth image.")
		
	
	
	def setFrame(self, frame):
		self.naked_frame = frame
		self.updateImage(frame)
	
	def updateImage(self, frame):
		self.depthImage.setPixmap(ui.convertOpenCVFrameToQPixmap(frame))
		
	
	@QtCore.pyqtSlot()
	def imageClicked(self, obj, event):
		self.fingerTip = [event.x(), event.y()]
		
		# Get the depth value and show it
		depth = hand.getDepthFromMap(self.parent.data.depth_map, self.fingerTip)
		self.pickedDepth.setText("Finger tip at %d mm away"%(int(depth)))
		
		# Ignore all previous drawings by doing a deep copy of the naked frame and add the new position dot
		frame = deepcopy(self.naked_frame)
		ui.drawPoint(frame, event.x()-2, event.y()-2, 2)
		self.updateImage(frame)
	
	
	@QtCore.pyqtSlot()
	def accept(self):
		if len(self.fingerTip) == 2:
			# Get the depth value of the finger tip and set it to the dataset
			self.fingerTip.append(hand.getDepthFromMap(self.parent.data.depth_map, self.fingerTip))
			self.parent.data.finger = self.fingerTip
			
			# Save the dataset
			self.parent.data.save()
		
			# Close the dialog
			self.reject()
		else:
			# Display an error
			self.messageBox.exec_()
	
	
	@QtCore.pyqtSlot()
	def reject(self):
		# Reset an eventual finger tip position
		self.fingerTip = []
		self.pickedDepth.setText("")
		
		# Restart the GUI screen timer and update the dataset number label
		self.parent.timerScreen.start()
		self.parent.updateDatasetNumberLabel()
		
		# Close the dialog
		super(DatasetDialog, self).reject()