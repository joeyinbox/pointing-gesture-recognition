#!/usr/bin/python
from PyQt5 import QtCore, QtWidgets, QtGui, QtMultimedia
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
		self.setWindowTitle("Pointing Gesture Recognition - Full dataset recording")
		
		# Retrieve all settings
		self.settings = Settings()
		
		# Load sounds
		self.countdownSound = QtMultimedia.QSound(self.settings.getResourceFolder()+"countdown.wav")
		self.countdownEndedSound = QtMultimedia.QSound(self.settings.getResourceFolder()+"countdown-ended.wav")
		

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
		
		
		# Create a timer for an eventual countdown before recording the data
		self.countdownTimer = QtCore.QTimer()
		self.countdownRemaining = 10
		self.countdownTimer.setInterval(1000)
		self.countdownTimer.setSingleShot(True)
		self.countdownTimer.timeout.connect(self.recordCountdown)
		
		
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
		self.data.depth_map = np.asarray(self.depth.get_tuple_depth_map()).reshape(480, 640)

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
			#print "Left hand depth: %d | Right hand depth: %d" % (leftPixel, rightPixel)
			
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
		# Freeze the data
		self.timerScreen.stop()
		
		# Translate the depth values to a frame and set it in the dialog window
		frame = np.fromstring(self.depth.get_raw_depth_map_8(), np.uint8).reshape(480, 640)
		frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
		self.dialogWindow.setFrame(frame)
	
		# Prompt the finger tip and eye positions
		self.dialogWindow.exec_()
	
	def recordCountdown(self):
		# Decrease the countdown and check if it needs to continue
		self.countdownRemaining -= 1
		
		if self.countdownRemaining <= 0:
			# Re-initialise the timer and record the data
			self.countdownTimer.stop()
			self.countdownEndedSound.play()
			self.countdownButton.setText("Saving..")
			self.countdownRemaining = 10
			self.record([])
		else:
			self.countdownTimer.start()
			self.countdownSound.play()
		
		# Display the actual reminaining
		self.countdownButton.setText("Save in %ds"%(self.countdownRemaining))
	
	
	# Create the acquisition interface form
	def create_acquision_form(self):
		globalLayout = QtWidgets.QVBoxLayout()
		hlayout = QtWidgets.QHBoxLayout()
		
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Target")
		groupbox_layout = QtWidgets.QVBoxLayout()
		self.targetAngleField = self.add_text_field(groupbox_layout, "Angle", 0, self.data.setTargetAngle)
		self.targetDistanceField = self.add_text_field(groupbox_layout, "Distance", 0, self.data.setTargetDistance)
		self.targetHeightField = self.add_text_field(groupbox_layout, "Height", 0, self.data.setTargetHeight)
		groupbox.setLayout(groupbox_layout)
		hlayout.addWidget(groupbox)
		
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Finger tip")
		groupbox_layout = QtWidgets.QVBoxLayout()
		self.fingerTipAngleField = self.add_text_field(groupbox_layout, "Angle", 0, self.data.setFingerTipAngle)
		self.fingerTipDistanceField = self.add_text_field(groupbox_layout, "Distance", 0, self.data.setFingerTipDistance)
		self.fingerTipHeightField = self.add_text_field(groupbox_layout, "Height", 0, self.data.setFingerTipHeight)
		groupbox.setLayout(groupbox_layout)
		hlayout.addWidget(groupbox)
		
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Eye")
		groupbox_layout = QtWidgets.QVBoxLayout()
		self.eyeAngleField = self.add_text_field(groupbox_layout, "Angle", 0, self.data.setEyeAngle)
		self.eyeDistanceField = self.add_text_field(groupbox_layout, "Distance", 0, self.data.setEyeDistance)
		self.eyeHeightField = self.add_text_field(groupbox_layout, "Height", 0, self.data.setEyeHeight)
		groupbox.setLayout(groupbox_layout)
		hlayout.addWidget(groupbox)
		
		globalLayout.addLayout(hlayout)
		hlayout = QtWidgets.QHBoxLayout()
		
		
		
		
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Pointing")
		groupbox_layout = QtWidgets.QVBoxLayout()
		
		item_layout = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel("Hand")
		label.setFixedWidth(100)
		comboBox = QtWidgets.QComboBox()
		comboBox.currentIndexChanged.connect(self.data.toggleHand)
		comboBox.setFixedWidth(285)
		comboBox.addItem("Left")
		comboBox.addItem("Right")
		comboBox.setCurrentIndex(0)
		item_layout.addWidget(label)
		item_layout.addWidget(comboBox)
		groupbox_layout.addLayout(item_layout)
		
		item_layout = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel("Orientation")
		label.setFixedWidth(100)
		comboBox = QtWidgets.QComboBox()
		comboBox.currentIndexChanged.connect(self.data.toggleOrientation)
		comboBox.setFixedWidth(285)
		comboBox.addItem("Back Right")
		comboBox.addItem("Right")
		comboBox.addItem("Front Right")
		comboBox.addItem("Front")
		comboBox.addItem("Front Left")
		comboBox.addItem("Left")
		comboBox.addItem("Back Left")
		comboBox.setCurrentIndex(0)
		item_layout.addWidget(label)
		item_layout.addWidget(comboBox)
		groupbox_layout.addLayout(item_layout)
		
		item_layout = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel("Direction")
		label.setFixedWidth(100)
		comboBox = QtWidgets.QComboBox()
		comboBox.currentIndexChanged.connect(self.data.toggleDirection)
		comboBox.setFixedWidth(285)
		comboBox.addItem("Up")
		comboBox.addItem("Lateral")
		comboBox.addItem("Down")
		comboBox.setCurrentIndex(0)
		item_layout.addWidget(label)
		item_layout.addWidget(comboBox)
		groupbox_layout.addLayout(item_layout)
		
		groupbox.setLayout(groupbox_layout)
		hlayout.addWidget(groupbox)
		
		
		
	
		groupbox = QtWidgets.QGroupBox()
		groupbox.setTitle("Camera")
		groupbox_layout = QtWidgets.QVBoxLayout()
		self.cameraHeightField = self.add_text_field(groupbox_layout, "Height", 1500, self.data.setCameraHeight)
		groupbox.setLayout(groupbox_layout)
		hlayout.addWidget(groupbox)
		
		
		
		vlayout2 = QtWidgets.QVBoxLayout()
		
		self.numberLabel.setFixedWidth(420)
		self.numberLabel.setAlignment(QtCore.Qt.AlignCenter)
		vlayout2.addWidget(self.numberLabel)
		
		
		item_layout = QtWidgets.QHBoxLayout()
		self.countdownButton = QtWidgets.QPushButton("Save in %ds"%(self.countdownRemaining), clicked=self.countdownTimer.start)
		self.saveButton = QtWidgets.QPushButton('Save', clicked=self.record)
		item_layout.addWidget(self.countdownButton)
		item_layout.addWidget(self.saveButton)
		vlayout2.addLayout(item_layout)
		
		hlayout.addLayout(vlayout2)
		globalLayout.addLayout(hlayout)
		
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



