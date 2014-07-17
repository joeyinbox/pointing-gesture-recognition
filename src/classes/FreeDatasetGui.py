#!/usr/bin/python
from PyQt5 import QtCore, QtWidgets, QtGui, QtMultimedia
from openni import *
import numpy as np
import cv2, ctypes, functools, hand, skeleton, ui

from classes.DatasetDialog import *
from classes.FreeDataset import *
from classes.SensorWidget import *
from classes.Settings import *


class FreeDatasetGui(QtWidgets.QWidget):
	def __init__(self):
		super(FreeDatasetGui, self).__init__()
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

		# Start generating
		self.context.start_generating_all()
		
		
		# Create a new dataset item
		self.data = FreeDataset()
		
		
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

		# Get the whole depth map
		self.data.depth_map = self.depth.map

		# Create the frame from the raw depth map string and convert it to RGB
		frame = np.fromstring(self.depth.get_raw_depth_map_8(), np.uint8).reshape(480, 640)
		frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
	
		# Get the RGB image of the scene
		self.data.image = np.fromstring(self.image.get_raw_image_map_bgr(), dtype=np.uint8).reshape(480, 640, 3)
		
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