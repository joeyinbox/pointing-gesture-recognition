#! /usr/bin/python
import functools, hand, ui
from PyQt5 import QtCore, QtWidgets
from copy import deepcopy

from classes.SensorWidget import *
from classes.FormItem import *


# Display a dialog window to prompt the finger tip position
class DatasetDialog(QtWidgets.QDialog):
	FINGER_TIP_TOOL = 0
	EYE_TOOL = 1
	
	tool = 0
	
	
	def __init__(self, parent=None):
		super(DatasetDialog, self).__init__(parent)
		self.parent = parent
		self.setWindowTitle("Indicate the positions of the pointing finger tip and the eye")
		
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
		group_layout = QtWidgets.QVBoxLayout()
		buttonGroup = QtWidgets.QButtonGroup(group_layout)
		self.trainingRadio = self.add_radio_button(buttonGroup, group_layout, "Set finger tip position", self.toggleFingerTipTool, True)
		self.positiveTestingRadio = self.add_radio_button(buttonGroup, group_layout, "Set eye position", self.toggleEyeTool)
		hlayout.addLayout(group_layout)
		
		self.pickedDepth = QtWidgets.QLabel("")
		self.pickedDepth.setAlignment(QtCore.Qt.AlignRight)
		
		vlayout = QtWidgets.QVBoxLayout()
		vlayout.addWidget(self.pickedDepth)
		vlayout.addWidget(self.buttonBox)
		
		hlayout.addLayout(vlayout)
		
		
		# Insert all elements to the layout
		self.layout.addWidget(self.depthImage)
		self.layout.addLayout(hlayout)
		
		
		# This will assert that the image has been clicked before saving
		self.fingerTip = []
		self.eye = []
		
		
		# If the user hit the save button without pointing the finger, display an alert
		self.messageBox = QtWidgets.QMessageBox()
		self.messageBox.setText("Please, indicate the positions of the pointing finger tip and the eye by clicking the depth image.")
	
	
	def toggleFingerTipTool(self, obj, value):
		if value == "True":
			self.tool = DatasetDialog.FINGER_TIP_TOOL
			print "Finger tip tool selected"
	
	def toggleEyeTool(self, obj, value):
		if value == "True":
			self.tool = DatasetDialog.EYE_TOOL
			print "eye tool selected"
	
	
	
	
	def add_radio_button(self, group, parent_layout, title, function, selected=False):
		radioButton = QtWidgets.QRadioButton(title)
		parent_layout.addWidget(radioButton)
		group.addButton(radioButton)
	
		obj = FormItem(selected)
		action = functools.partial(function, obj)
		# connect signals to gui elements
		obj.value.changed.connect(action)
		radioButton.toggled.connect(obj.value.set_value)
	
		if selected == True:
			radioButton.toggle()
	
		return obj
	
	
	def setFrame(self, frame):
		self.naked_frame = frame
		self.updateImage(frame)
	
	def updateImage(self, frame):
		self.depthImage.setPixmap(ui.convertOpenCVFrameToQPixmap(frame))
		
	
	@QtCore.pyqtSlot()
	def imageClicked(self, obj, event):
		self.click = [event.x(), event.y()]
		
		# Get the depth value and show it
		depth = hand.getDepthFromMap(self.parent.data.depth_map, [self.click[1], self.click[0]])
		
		if self.tool == DatasetDialog.FINGER_TIP_TOOL:
			self.fingerTip = self.click
			self.pickedDepth.setText("Finger tip at %d mm away"%(int(depth)))
		elif self.tool == DatasetDialog.EYE_TOOL:
			self.eye = self.click
			self.pickedDepth.setText("Eye at %d mm away"%(int(depth)))
		
		# Ignore all previous drawings by doing a deep copy of the naked frame and add the new position dot
		frame = deepcopy(self.naked_frame)
		
		if len(self.fingerTip) == 2:
			ui.drawPoint(frame, self.fingerTip[0]-2, self.fingerTip[1]-2, 2)
		
		if len(self.eye) == 2:
			ui.drawPoint(frame, self.eye[0]-2, self.eye[1]-2, 2, (255, 0, 255))
		
		self.updateImage(frame)
	
	
	@QtCore.pyqtSlot()
	def accept(self):
		if len(self.fingerTip) == 2 and len(self.eye) == 2:
			# Get the depth value of the finger tip and set it to the dataset
			self.fingerTip.append(hand.getDepthFromMap(self.parent.data.depth_map, self.fingerTip))
			self.parent.data.fingerTip["position"] = self.fingerTip
			
			# Repeat for the eye
			self.eye.append(hand.getDepthFromMap(self.parent.data.depth_map, self.eye))
			self.parent.data.eye["position"] = self.eye
			
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
		self.eye = []
		self.pickedDepth.setText("")
		
		# Restart the GUI screen timer and update the dataset number label
		self.parent.timerScreen.start()
		self.parent.updateDatasetNumberLabel()
		
		# Close the dialog
		super(DatasetDialog, self).reject()