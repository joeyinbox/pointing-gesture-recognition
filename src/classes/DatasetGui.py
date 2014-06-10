#!/usr/bin/python
from PyQt5 import QtCore, QtWidgets, QtGui
from openni import *
import numpy as np
import cv2, ctypes, functools, hand, skeleton, ui

from classes.Dataset import *
from classes.DatasetDialog import *
from classes.FormItem import *
from classes.SensorWidget import *
from classes.Settings import *


class DatasetGui(QtWidgets.QWidget):
	def __init__(self):
		super(DatasetGui, self).__init__()
		self.setWindowTitle("Pointing Gesture Recognition - Dataset recording")
		
		# Retrieve all settings
		self.settings = Settings()
		

		# Get the context and initialise it
		self.context = Context()
		self.context.init()

		# Create the depth generator to get the depth map of the scene
		self.depth = DepthGenerator()
		self.depth.create(self.context)
		self.depth.set_resolution_preset(RES_VGA)
		self.depth.fps = 30

		# Create the image generator to get an RGB image of the scene
		self.image = ImageGenerator()
		self.image.create(self.context)
		self.image.set_resolution_preset(RES_VGA)
		self.image.fps = 30

		# Create the user generator to detect skeletons
		self.user = UserGenerator()
		self.user.create(self.context)

		# Initialise the skeleton tracking
		skeleton.init(self.user)

		# Start generating
		self.context.start_generating_all()
		print "Starting to detect users.."
		
		
		# Create a new dataset item
		self.data = Dataset()
		
		
		# Create the global layout
		self.layout = QtWidgets.QVBoxLayout(self)
		hlayout = QtWidgets.QHBoxLayout()
		
		# Create custom widgets to hold sensor's images
		self.depthImage = SensorWidget()
		self.depthImage.setGeometry(10, 10, 640, 480)
		self.rgbImage = SensorWidget()
		self.rgbImage.setGeometry(10, 10, 640, 480)
		
		# Add these custom widgets to the global layout
		hlayout.addWidget(self.depthImage)
		hlayout.addWidget(self.rgbImage)
		self.layout.addLayout(hlayout)
		
		# Hold the label indicating the number of dataset taken
		self.numberLabel = QtWidgets.QLabel()
		self.updateDatasetNumberLabel()
		
		# Create the acquisition form elements
		self.create_acquision_form()
		
		
		# Register a dialog window to prompt the finger tip position
		self.dialogWindow = DatasetDialog(self)
		
		
		# Create and launch a timer to update the images
		self.timerScreen = QtCore.QTimer()
		self.timerScreen.setInterval(30)
		self.timerScreen.setSingleShot(True)
		self.timerScreen.timeout.connect(self.updateImage)
		self.timerScreen.start()
	
		
	def updateImage(self):
		
		# Update to next frame
		self.context.wait_and_update_all()
		
		# Extract informations of each tracked user
		self.data = skeleton.track(self.user, self.depth, self.data)

		# Get the whole depth map
		self.data.depth_map = self.depth.map

		# Create the frame from the raw depth map string and convert it to RGB
		frame = np.fromstring(self.depth.get_raw_depth_map_8(), np.uint8).reshape(480, 640)
		frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
	
		# Get the RGB image of the scene
		self.data.image = np.fromstring(self.image.get_raw_image_map_bgr(), dtype=np.uint8).reshape(480, 640, 3)
		
		
		if len(self.user.users) > 0 and len(self.data.skeleton["head"]) > 0:
			# Highlight the head
			ui.drawPoint(frame, self.data.skeleton["head"][0], self.data.skeleton["head"][1], 5)
    		
			# Display lines from elbows to the respective hands
			ui.drawElbowLine(frame, self.data.skeleton["elbow"]["left"], self.data.skeleton["hand"]["left"])
			ui.drawElbowLine(frame, self.data.skeleton["elbow"]["right"], self.data.skeleton["hand"]["right"])
		
			# Get the pixel's depth from the coordinates of the hands
			leftPixel = hand.getDepthFromMap(self.data.depth_map, self.data.skeleton["hand"]["left"])
			rightPixel = hand.getDepthFromMap(self.data.depth_map, self.data.skeleton["hand"]["right"])
			print "Left hand depth: %d | Right hand depth: %d" % (leftPixel, rightPixel)
			
			# Get the shift of the boundaries around both hands
			leftShift = hand.getHandBoundShift(leftPixel)
			rightShift = hand.getHandBoundShift(rightPixel)
    		
			# Display a rectangle around both hands
			ui.drawHandBoundaries(frame, self.data.skeleton["hand"]["left"], leftShift, (50, 100, 255))
			ui.drawHandBoundaries(frame, self.data.skeleton["hand"]["right"], rightShift, (200, 70, 30))
		
		
		self.depthImage.setPixmap(ui.convertOpenCVFrameToQPixmap(frame))
		self.rgbImage.setPixmap(ui.convertOpenCVFrameToQPixmap(self.data.image))
		
		self.timerScreen.start()
	
	
	def updateDatasetNumberLabel(self):
		self.numberLabel.setText("Dataset #%d" % (utils.getFileNumberInFolder(self.settings.getDatasetFolder())))
	
	
	def record(self, obj):
		# Prompt the finger tip position only if needed
		if self.data.hand["type"] == Dataset.NO_HAND:
			# Directly save the dataset and update the label number
			self.data.save()
			self.updateDatasetNumberLabel()
		else:
			# Freeze the data
			self.timerScreen.stop()
			
			# Translate the depth values to a frame and set it in the dialog window
			frame = np.fromstring(self.depth.get_raw_depth_map_8(), np.uint8).reshape(480, 640)
			frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
			self.dialogWindow.setFrame(frame)
		
			# Display the dialog window
			self.dialogWindow.exec_()
	
	
	
	# Create the acquisition interface form
	def create_acquision_form(self):
		globalLayout = QtWidgets.QHBoxLayout()
		vlayout = QtWidgets.QVBoxLayout()
	
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Pointing hand")
		groupbox_layout = QtWidgets.QVBoxLayout()
		buttonGroup = QtWidgets.QButtonGroup(groupbox_layout)
		self.leftHandRadio = self.add_radio_button(buttonGroup, groupbox_layout, "Left hand", self.data.toggleLeftHand, True)
		self.rightHandRadio = self.add_radio_button(buttonGroup, groupbox_layout, "Right hand", self.data.toggleRightHand)
		self.noHandRadio = self.add_radio_button(buttonGroup, groupbox_layout, "No hand", self.data.toggleNoHand)
		groupbox.setLayout(groupbox_layout)
		vlayout.addWidget(groupbox)
	
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Hand")
		groupbox_layout = QtWidgets.QVBoxLayout()
		self.handHeightField = self.add_text_field(groupbox_layout, "Height", 0, self.data.setHandHeight)
		self.handWidthField = self.add_text_field(groupbox_layout, "Width", 0, self.data.setHandWidth)
		self.handThicknessField = self.add_text_field(groupbox_layout, "Thickness", 0, self.data.setHandThickness)
		groupbox.setLayout(groupbox_layout)
		vlayout.addWidget(groupbox)
	
		globalLayout.addLayout(vlayout)
		vlayout = QtWidgets.QVBoxLayout()
	
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("User")
		groupbox_layout = QtWidgets.QVBoxLayout()
		self.userDistanceField = self.add_text_field(groupbox_layout, "Distance", 0, self.data.setUserDistance)
		self.userHeightField = self.add_text_field(groupbox_layout, "Height", 0, self.data.setUserHeight)
		self.userAngleField = self.add_text_field(groupbox_layout, "Angle", 0, self.data.setUserAngle)
		groupbox.setLayout(groupbox_layout)
		vlayout.addWidget(groupbox)
	
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Target")
		groupbox_layout = QtWidgets.QVBoxLayout()
		self.targetDistanceField = self.add_text_field(groupbox_layout, "Distance", 0, self.data.setTargetDistance)
		self.targetHeightField = self.add_text_field(groupbox_layout, "Height", 0, self.data.setTargetHeight)
		self.targetAngleField = self.add_text_field(groupbox_layout, "Angle", 0, self.data.setTargetAngle)
		groupbox.setLayout(groupbox_layout)
		vlayout.addWidget(groupbox)
	
		globalLayout.addLayout(vlayout)
		vlayout = QtWidgets.QVBoxLayout()
	
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Camera")
		groupbox_layout = QtWidgets.QVBoxLayout()
		self.cameraHeightField = self.add_text_field(groupbox_layout, "Height", 1500, self.data.setCameraHeight)
		groupbox.setLayout(groupbox_layout)
		vlayout.addWidget(groupbox)
	
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Arm")
		groupbox_layout = QtWidgets.QVBoxLayout()
		self.userArmLengthField = self.add_text_field(groupbox_layout, "Length", 0, self.data.setUserArmLength)
		groupbox.setLayout(groupbox_layout)
		vlayout.addWidget(groupbox)
		
		vlayout2 = QtWidgets.QVBoxLayout()
		
		self.numberLabel.setFixedWidth(405)
		self.numberLabel.setAlignment(QtCore.Qt.AlignCenter)
		vlayout2.addWidget(self.numberLabel)
		
		buttonGroup = QtWidgets.QButtonGroup(vlayout2)
		self.trainingRadio = self.add_radio_button(buttonGroup, vlayout2, "Training", self.data.toggleTraining, True)
		self.positiveTestingRadio = self.add_radio_button(buttonGroup, vlayout2, "Positive testing", self.data.togglePositiveTesting)
		self.negativeTestingRadio = self.add_radio_button(buttonGroup, vlayout2, "Negative testing", self.data.toggleNegativeTesting)
	
		save = QtWidgets.QPushButton('Save', clicked=self.record)
		vlayout2.addWidget(save)
	
		vlayout.addLayout(vlayout2)
		globalLayout.addLayout(vlayout)
		self.layout.addLayout(globalLayout)


	# Add a text input and its corresponding label to the layout
	def add_text_field(self, parent_layout, title, value, function):
		hlayout = QtWidgets.QHBoxLayout()
	
		text_label = QtWidgets.QLabel(title)
		text_label.setFixedWidth(70)
		text_field = QtWidgets.QLineEdit()
		text_field.setValidator(QtGui.QIntValidator(0, 31337))
	
		hlayout.addWidget(text_label)
		hlayout.addWidget(text_field)
		parent_layout.addLayout(hlayout)
	
		# Create a form item and connect changed signal to the GUI element
		obj = FormItem(value)
		action = functools.partial(function, obj)
		obj.value.changed.connect(action)
		obj.value.changed.connect(text_field.setText)
		text_field.textChanged.connect(obj.value.set_value)
	
		# Set the text field value and trigger the value update
		text_field.setText(str(value))
	
		return obj




	# Add a radio button to the layout
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