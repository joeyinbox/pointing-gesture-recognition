#!/usr/bin/python
from PyQt5 import QtCore, QtWidgets, QtGui, QtMultimedia
from openni import *
import numpy as np
import cv2, ctypes, functools, skeleton, ui

import accuracy
from classes.BPNHandler import *
from classes.DatasetDialog import *
from classes.Dataset import *
from classes.FeatureExtractor import *
from classes.SensorWidget import *
from classes.Settings import *
from classes.Utils import *



# Definition of the DatasetGui class
class DatasetGui(QtWidgets.QWidget):
	
	utils = Utils()
	featureExtractor = FeatureExtractor()
	bpn = BPNHandler(True)
	accuracy = accuracy.Accuracy()
	
	
	# Constructor of the DatasetGui class
	# 
	# @param	None
	# @return	None
	def __init__(self):
		super(DatasetGui, self).__init__()
		self.setWindowTitle("Pointing Gesture Recognition - Dataset recording")
		
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
		
		# Create a timer to eventually record data for a heat map
		self.heatmapRunning = False
		self.heatmapTimer = QtCore.QTimer()
		self.heatmapTimer.setInterval(10)
		self.heatmapTimer.setSingleShot(True)
		self.heatmapTimer.timeout.connect(self.recordHeatmap)
		
		
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
		self.createAcquisitionForm()
		
		
		# Register a dialog window to prompt the target position
		self.dialogWindow = DatasetDialog(self)
		
		
		# Allow to save the data when the right distance is reached
		self.recordIfReady = False
		
		
		# Create and launch a timer to update the images
		self.timerScreen = QtCore.QTimer()
		self.timerScreen.setInterval(30)
		self.timerScreen.setSingleShot(True)
		self.timerScreen.timeout.connect(self.updateImage)
		self.timerScreen.start()
		
	
	# Update the depth image displayed within the main window
	# 
	# @param	None
	# @return	None
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
		
		# Will be used to specify the depth of the current hand wished
		currentDepth, showCurrentDepth = 0, ""
		
		
		if len(self.user.users) > 0 and len(self.data.skeleton["head"]) > 0:
			# Highlight the head
			ui.drawPoint(frame, self.data.skeleton["head"][0], self.data.skeleton["head"][1], 5)
    		
			# Display lines from elbows to the respective hands
			ui.drawElbowLine(frame, self.data.skeleton["elbow"]["left"], self.data.skeleton["hand"]["left"])
			ui.drawElbowLine(frame, self.data.skeleton["elbow"]["right"], self.data.skeleton["hand"]["right"])
			
			# Get the pixel's depth from the coordinates of the hands
			leftPixel = self.utils.getDepthFromMap(self.data.depth_map, self.data.skeleton["hand"]["left"])
			rightPixel = self.utils.getDepthFromMap(self.data.depth_map, self.data.skeleton["hand"]["right"])
			
			if self.data.hand == self.settings.LEFT_HAND:
				currentDepth = leftPixel
			elif self.data.hand == self.settings.RIGHT_HAND:
				currentDepth = rightPixel
			
			# Get the shift of the boundaries around both hands
			leftShift = self.utils.getHandBoundShift(leftPixel)
			rightShift = self.utils.getHandBoundShift(rightPixel)
    		
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
	
	
	# Update the label indicating the number of dataset elements saved so far for the current type
	# 
	# @param	None
	# @return	None
	def updateDatasetNumberLabel(self):
		if self.data.type == Dataset.TYPE_POSITIVE:
			self.numberLabel.setText("Dataset #%d" % (self.utils.getFileNumberInFolder(self.settings.getPositiveFolder())))
		elif self.data.type == Dataset.TYPE_NEGATIVE:
			self.numberLabel.setText("Dataset #%d" % (self.utils.getFileNumberInFolder(self.settings.getNegativeFolder())))
		elif self.data.type == Dataset.TYPE_ACCURACY:
			self.numberLabel.setText("Dataset #%d" % (self.utils.getFileNumberInFolder(self.settings.getAccuracyFolder())))
		else:
			self.numberLabel.setText("Dataset #%d" % (self.utils.getFileNumberInFolder(self.settings.getDatasetFolder())))
		
	
	# Record the actual informations
	# 
	# @param	obj					Initiator of the event
	# @return	None
	def record(self, obj):
		# If the user collects data to check accuracy, prompts additional informations
		if self.data.type == Dataset.TYPE_ACCURACY:
			self.saveForTarget()
		# If the user collects data for a heat map, let's do it
		elif self.data.type == Dataset.TYPE_HEATMAP:
			# The same button will be used to stop recording
			if not self.heatmapRunning:
				self.startRecordHeatmap()
			else:
				self.stopRecordHeatmap()
		else:
			# Directly save the dataset and update the label number
			self.data.save()
			self.countdownEndedSound.play()
			self.updateDatasetNumberLabel()
	
	
	# Handle a countdown as a mean to record the informations with a delay
	# 
	# @param	None
	# @return	None
	def recordCountdown(self):
		# Decrease the countdown and check if it needs to continue
		self.countdownRemaining -= 1
		
		if self.countdownRemaining <= 0:
			# Re-initialise the timer and record the data
			self.countdownTimer.stop()
			self.countdownButton.setText("Saving..")
			self.countdownRemaining = 10
			self.record([])
		else:
			self.countdownTimer.start()
			self.countdownSound.play()
		
		# Display the actual reminaining
		self.countdownButton.setText("Save in %ds"%(self.countdownRemaining))
	
	
	# Record a heatmap representation of the informations by successive captures
	# 
	# @param	None
	# @return	None
	def recordHeatmap(self):
		if self.data.hand == self.settings.NO_HAND:
			print "Unable to record as no hand is selected"
			return False
		
		if len(self.user.users) > 0 and len(self.data.skeleton["head"]) > 0:
			# Input the data into the feature extractor
			result = self.bpn.check(self.featureExtractor.getFeatures(self.data))
			
			# Add the depth of the finger tip
			point = self.featureExtractor.fingerTip[result[1]]
			point.append(self.utils.getDepthFromMap(self.data.depth_map, point))
			
			# Verify that informations are correct
			if point[0]!=0 and point[1]!=0 and point[2]!=0:
				# Add the result of the neural network
				point.append(result[0])
				
				self.heatmap.append(point)
				self.countdownSound.play()
			
		# Loop timer
		self.heatmapTimer.start()
	
	
	# Start the recording of the heatmap
	# 
	# @param	None
	# @return	None
	def startRecordHeatmap(self):
		self.saveButton.setText("Stop recording")
		self.heatmapRunning = True
		self.heatmapTimer.start()
		
	
	# Stop the recording of the heatmap
	# 
	# @param	None
	# @return	None
	def stopRecordHeatmap(self):
		self.heatmapTimer.stop()
		self.heatmapRunning = False
		self.countdownEndedSound.play()
		
		self.saveButton.setText("Record")
		
		self.accuracy.showHeatmap(self.heatmap, "front")
		self.heatmap = []
		
		
	# Raise a flag to record the informations when the chosen distance will be met
	# 
	# @param	None
	# @return	None
	def startRecordWhenReady(self):
		self.recordIfReady = True
	
	
	# Hold the current informations to indicate the position of the target thanks to the dialog window
	# 
	# @param	None
	# @return	None
	def saveForTarget(self):
		# Freeze the data
		self.timerScreen.stop()
		self.countdownEndedSound.play()
		
		# Translate the depth values to a frame and set it in the dialog window
		frame = np.fromstring(self.depth.get_raw_depth_map_8(), np.uint8).reshape(480, 640)
		frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
		self.dialogWindow.setFrame(frame)
	
		# Prompt the position of the target
		self.dialogWindow.exec_()
	
	
	# Toggle the type of dataset chosen
	# 
	# @param	value				Identifier of the new type of dataset
	# @return	None
	def toggleType(self, value):
		self.data.toggleType(value)
		
		if value == self.data.TYPE_HEATMAP:
			self.saveButton.setText("Record")
			self.countdownButton.setText("Record in %ds"%(self.countdownRemaining))
			self.readyButton.setEnabled(False)
			
			# Create an array to hold all points
			self.heatmap = []
		else:
			self.updateDatasetNumberLabel()
			if hasattr(self, 'saveButton'):
				self.saveButton.setText("Save")
				self.countdownButton.setText("Save in %ds"%(self.countdownRemaining))
				self.readyButton.setEnabled(True)
	
	
	# Create the acquisition form of the main window
	# 
	# @param	None
	# @return	None
	def createAcquisitionForm(self):
		globalLayout = QtWidgets.QHBoxLayout()
		vlayout = QtWidgets.QVBoxLayout()
		
		# Drop down menu of the distance to record the informations when the pointing hand meet the corresponding value
		hlayout = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel("Distance")
		label.setFixedWidth(100)
		comboBox = QtWidgets.QComboBox()
		comboBox.currentIndexChanged.connect(self.data.toggleDistance)
		comboBox.setFixedWidth(200)
		comboBox.addItem("550")
		comboBox.addItem("750")
		comboBox.addItem("1000")
		comboBox.addItem("1250")
		comboBox.addItem("1500")
		comboBox.addItem("1750")
		comboBox.addItem("2000")
		comboBox.setCurrentIndex(0)
		hlayout.addWidget(label)
		hlayout.addWidget(comboBox)
		vlayout.addLayout(hlayout)
		
		# Drop down menu to select the type of hand of the dataset
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
		
		# Drop down menu of the dataset type
		hlayout = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel("Type")
		label.setFixedWidth(100)
		comboBox = QtWidgets.QComboBox()
		comboBox.currentIndexChanged.connect(self.toggleType)
		comboBox.setFixedWidth(200)
		comboBox.addItem("Positive")
		comboBox.addItem("Negative")
		comboBox.addItem("Accuracy")
		comboBox.addItem("Heat map")
		comboBox.setCurrentIndex(0)
		hlayout.addWidget(label)
		hlayout.addWidget(comboBox)
		vlayout.addLayout(hlayout)
		
		globalLayout.addLayout(vlayout)
		vlayout = QtWidgets.QVBoxLayout()
		
		self.numberLabel.setAlignment(QtCore.Qt.AlignCenter)
		vlayout.addWidget(self.numberLabel)
		
		# Action buttons to record the way that suits the most
		hLayout = QtWidgets.QHBoxLayout()
		self.readyButton = QtWidgets.QPushButton('Save when ready', clicked=self.startRecordWhenReady)
		self.saveButton = QtWidgets.QPushButton('Save', clicked=self.record)
		hLayout.addWidget(self.readyButton)
		vlayout.addLayout(hLayout)
		
		item_layout = QtWidgets.QHBoxLayout()
		self.countdownButton = QtWidgets.QPushButton("Save in %ds"%(self.countdownRemaining), clicked=self.countdownTimer.start)
		self.saveButton = QtWidgets.QPushButton('Save', clicked=self.record)
		item_layout.addWidget(self.countdownButton)
		item_layout.addWidget(self.saveButton)
		vlayout.addLayout(item_layout)
		
		globalLayout.addLayout(vlayout)
		self.layout.addLayout(globalLayout)