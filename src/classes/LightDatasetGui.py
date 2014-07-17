#!/usr/bin/python
from PyQt5 import QtCore, QtWidgets, QtGui, QtMultimedia
from openni import *
import numpy as np
import cv2, ctypes, functools, hand, skeleton, ui

from classes.DatasetDialog import *
from classes.LightDataset import *
from classes.SensorWidget import *
from classes.Settings import *


class LightDatasetGui(QtWidgets.QWidget):
	def __init__(self):
		super(LightDatasetGui, self).__init__()
		self.setWindowTitle("Pointing Gesture Recognition - Light dataset recording")
		
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
		self.data = LightDataset()
		
		
		# Create a timer for an eventual countdown before recording the data
		self.countdownTimer = QtCore.QTimer()
		self.countdownRemaining = 10
		self.countdownTimer.setInterval(1000)
		self.countdownTimer.setSingleShot(True)
		self.countdownTimer.timeout.connect(self.recordCountdown)
		
		
		# Create the global layout
		self.layout = QtWidgets.QVBoxLayout(self)
		
		# Create custom widgets to hold sensor's images
		self.depthImage = SensorWidget()
		self.depthImage.setGeometry(10, 10, 640, 480)
		
		# Add these custom widgets to the global layout
		self.layout.addWidget(self.depthImage)
		
		# Hold the label indicating the number of dataset taken
		self.numberLabel = QtWidgets.QLabel()
		self.updateDatasetNumberLabel()
		
		# Create the acquisition form elements
		self.create_acquision_form()
		
		
		# Allow to save the data when the right distance is reached
		self.recordIfReady = False
		
		
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
		
		# Will be used to specify the depth of the current hand wished
		currentDepth, showCurrentDepth = 0, ""
		
		
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
			
			if self.data.hand == LightDataset.LEFT_HAND:
				currentDepth = leftPixel
			elif self.data.hand == LightDataset.RIGHT_HAND:
				currentDepth = rightPixel
			
			# Get the shift of the boundaries around both hands
			leftShift = hand.getHandBoundShift(leftPixel)
			rightShift = hand.getHandBoundShift(rightPixel)
    		
			# Display a rectangle around both hands
			ui.drawHandBoundaries(frame, self.data.skeleton["hand"]["left"], leftShift, (50, 100, 255))
			ui.drawHandBoundaries(frame, self.data.skeleton["hand"]["right"], rightShift, (200, 70, 30))
		
		# Record the current data if the user is ready
		if self.recordIfReady:
			cv2.putText(frame, str(self.data.getWishedDistance()), (470, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (252, 63, 253), 5)
			
			if self.data.getWishedDistance()>=int(currentDepth)-10 and self.data.getWishedDistance()<=int(currentDepth)+10:
				self.record([])
				self.recordIfReady = False
			else:
				if int(currentDepth)<self.data.getWishedDistance():
					showCurrentDepth = str(currentDepth)+" +"
				else:
					showCurrentDepth = str(currentDepth)+" -"
		else:
			showCurrentDepth = str(currentDepth)
			
		cv2.putText(frame, showCurrentDepth, (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 100, 255), 5)
		
		# Update the frame
		self.depthImage.setPixmap(ui.convertOpenCVFrameToQPixmap(frame))
		
		self.timerScreen.start()
	
	
	def updateDatasetNumberLabel(self):
		self.numberLabel.setText("Dataset #%d" % (utils.getFileNumberInFolder(self.settings.getLightDatasetFolder())))
	
	
	def record(self, obj):
		# Directly save the dataset and update the label number
		self.data.save()
		self.updateDatasetNumberLabel()
	
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
	
	
	def startRecordWhenReady(self):
		self.recordIfReady = True
	def clearUsers(self):
		print "Clearing active users"
		skeleton.clear(self.user.users)
	# Create the acquisition interface form
	def create_acquision_form(self):
		globalLayout = QtWidgets.QHBoxLayout()
		vlayout = QtWidgets.QVBoxLayout()
		
		hlayout = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel("Distance")
		label.setFixedWidth(100)
		comboBox = QtWidgets.QComboBox()
		comboBox.currentIndexChanged.connect(self.data.toggleDistance)
		comboBox.setFixedWidth(200)
		comboBox.addItem("550")
		comboBox.addItem("1000")
		comboBox.addItem("1500")
		comboBox.addItem("2000")
		comboBox.setCurrentIndex(0)
		hlayout.addWidget(label)
		hlayout.addWidget(comboBox)
		vlayout.addLayout(hlayout)
		
		
		hlayout = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel("Pointing hand")
		label.setFixedWidth(100)
		comboBox = QtWidgets.QComboBox()
		comboBox.currentIndexChanged.connect(self.data.toggleHand)
		comboBox.setFixedWidth(200)
		comboBox.addItem("Left")
		comboBox.addItem("Right")
		comboBox.addItem("None")
		comboBox.setCurrentIndex(0)
		hlayout.addWidget(label)
		hlayout.addWidget(comboBox)
		vlayout.addLayout(hlayout)
		
		hlayout = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel("Type")
		label.setFixedWidth(100)
		comboBox = QtWidgets.QComboBox()
		comboBox.currentIndexChanged.connect(self.data.toggleType)
		comboBox.setFixedWidth(200)
		comboBox.addItem("Positive")
		comboBox.addItem("Negative")
		comboBox.setCurrentIndex(0)
		hlayout.addWidget(label)
		hlayout.addWidget(comboBox)
		vlayout.addLayout(hlayout)
		
		globalLayout.addLayout(vlayout)
		vlayout = QtWidgets.QVBoxLayout()
		
		self.numberLabel.setAlignment(QtCore.Qt.AlignCenter)
		vlayout.addWidget(self.numberLabel)
		
		hLayout = QtWidgets.QHBoxLayout()
		self.readyButton = QtWidgets.QPushButton('Save when ready', clicked=self.startRecordWhenReady)
		#self.countdownButton = QtWidgets.QPushButton("Save in %ds"%(self.countdownRemaining), clicked=self.countdownTimer.start)
		self.saveButton = QtWidgets.QPushButton('Save', clicked=self.record)
		self.clearButton = QtWidgets.QPushButton('Clear users', clicked=self.clearUsers)
		#hLayout.addWidget(self.countdownButton)
		hLayout.addWidget(self.readyButton)
		hLayout.addWidget(self.clearButton)
		vlayout.addLayout(hLayout)
		vlayout.addWidget(self.saveButton)
		
		globalLayout.addLayout(vlayout)
		self.layout.addLayout(globalLayout)