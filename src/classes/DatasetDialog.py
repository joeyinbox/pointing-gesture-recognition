#! /usr/bin/python
import functools, ui
from PyQt5 import QtCore, QtWidgets, QtGui
from copy import deepcopy

from classes.SensorWidget import *
from classes.Utils import *



# Definition of the DatasetDialog class to display a dialog window to prompt the target position
class DatasetDialog(QtWidgets.QDialog):
	
	utils = Utils()
	
	
	# Constructor of the DatasetDialog class
	# 
	# @param	parent				Parent instance to exchange informations up to the main window
	# @return	None
	def __init__(self, parent=None):
		# Initialise a dialog window
		super(DatasetDialog, self).__init__(parent)
		self.parent = parent
		self.setWindowTitle("Indicate the position of the target")
		
		self.layout = QtWidgets.QVBoxLayout(self)
		
		# Reserve some space for the depth image
		self.depthImage = SensorWidget()
		self.depthImage.setGeometry(10, 10, 640, 480)
		
		# Register action for the depth image
		action = functools.partial(self.imageClicked, self.depthImage)
		self.depthImage.clicked.connect(action)
		
		
		# Create OK|Cancel buttons
		self.buttonBox = QtWidgets.QDialogButtonBox(self)
		self.buttonBox.setFixedWidth(170)
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
		
		# Register actions for the buttons
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reject)
		self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.accept)
		
		hlayout = QtWidgets.QHBoxLayout()
		
		# Create target distance text field and the output of the clicked depth
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Target")
		groupbox_layout = QtWidgets.QVBoxLayout()
		self.targetDistance = self.add_text_field(groupbox_layout, "Distance between the target and the fingertip:", 0, self.parent.data.setDistance)
		
		self.pickedDepth = QtWidgets.QLabel("")
		self.pickedDepth.setAlignment(QtCore.Qt.AlignLeft)
		groupbox_layout.addWidget(self.pickedDepth)
		
		groupbox.setLayout(groupbox_layout)
		
		hlayout.addWidget(groupbox)
		hlayout.addWidget(self.buttonBox)
		
		
		# Insert all elements to the layout
		self.layout.addWidget(self.depthImage)
		self.layout.addLayout(hlayout)
		
		# This will assert that the image has been clicked before saving
		self.target = []
		
		# If the user hit the save button without indicating the target, display an alert
		self.messageBox = QtWidgets.QMessageBox()
		self.messageBox.setText("Please, indicate the position of the target.")
	
	
	# Add a text input and its corresponding label to the layout
	# 
	# @param	parent_layout		Layout of the parent to add the widget accordingly
	# @param	title				Label of the input text field
	# @param	value				Default value of the text field
	# @param	function			Function to trigger when the value of the input changes
	# @return	QLineEdit			Instance of the text field
	def add_text_field(self, parent_layout, title, value, function):
		hlayout = QtWidgets.QHBoxLayout()
	
		text_label = QtWidgets.QLabel(title)
		text_label.setFixedWidth(270)
		text_field = QtWidgets.QLineEdit()
		text_field.setValidator(QtGui.QIntValidator(0, 31337))
	
		hlayout.addWidget(text_label)
		hlayout.addWidget(text_field)
		parent_layout.addLayout(hlayout)
	
		# Connect changed signal to the GUI element
		text_field.textChanged.connect(function)
	
		# Set the text field value and trigger the value update
		text_field.setText(str(value))
	
		return text_field
	
	
	# Hold a naked version and update the image of the window
	# 
	# @param	frame				Image informations
	# @return	None
	def setFrame(self, frame):
		self.naked_frame = frame
		self.updateImage(frame)
	
	
	# Update the image of the window
	# 
	# @param	frame				Image informations
	# @return	None
	def updateImage(self, frame):
		self.depthImage.setPixmap(ui.convertOpenCVFrameToQPixmap(frame))
	
	
	# Slot triggered when the image receive a click event
	# 
	# @param	obj					Initiator of the event
	# @param	event				Informations about the current event
	# @return	None
	@QtCore.pyqtSlot()
	def imageClicked(self, obj, event):
		self.target = [event.x(), event.y()]
		
		# Get the depth value and show it
		depth = self.utils.getDepthFromMap(self.parent.data.depth_map, self.target)
		
		self.pickedDepth.setText("Distance between the target and the camera: %d mm."%(int(depth)))
		
		# Ignore all previous drawings by doing a deep copy of the naked frame and add the new position dot
		frame = deepcopy(self.naked_frame)
		ui.drawPoint(frame, self.target[0]-2, self.target[1]-2, 2)
		
		self.updateImage(frame)
	
	
	# Slot triggered when the OK button is used
	# 
	# @param	None
	# @return	None
	@QtCore.pyqtSlot()
	def accept(self):
		if len(self.target) == 2:
			# Get the depth value of the target and set it to the dataset
			self.target.append(self.utils.getDepthFromMap(self.parent.data.depth_map, self.target))
			self.parent.data.target = self.target
			
			# Save the dataset
			self.parent.data.save()
		
			# Close the dialog
			self.reject()
		else:
			# Display an error
			self.messageBox.exec_()
	
	
	# Slot triggered when the Cancel button is used or the dialog window closed or the echap button pressed
	# 
	# @param	None
	# @return	None
	@QtCore.pyqtSlot()
	def reject(self):
		# Reset an eventual finger tip position
		self.target = []
		self.pickedDepth.setText("")
		
		# Restart the GUI screen timer and update the dataset number label
		self.parent.timerScreen.start()
		self.parent.updateDatasetNumberLabel()
		
		# Close the dialog
		super(DatasetDialog, self).reject()