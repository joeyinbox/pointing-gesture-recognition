#!/usr/bin/python
from PyQt5 import QtCore, QtWidgets, QtGui, QtMultimedia
from openni import *
import numpy as np
from copy import deepcopy
import cv2, ctypes, functools, skeleton, ui

from classes.BPNHandler import *
from classes.FeatureExtractor import *
from classes.LiveDataset import *
from classes.SensorWidget import *
from classes.Settings import *
from classes.Utils import *


class LiveGui(QtWidgets.QWidget):
	
	utils = Utils()
	featureExtractor = FeatureExtractor()
	bpn = BPNHandler(True)
	
	def __init__(self):
		super(LiveGui, self).__init__()
		self.setWindowTitle("Pointing Gesture Recognition - Live")
		
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

		# Create the user generator to detect skeletons
		self.user = UserGenerator()
		self.user.create(self.context)

		# Initialise the skeleton tracking
		skeleton.init(self.user)

		# Start generating
		self.context.start_generating_all()
		print "Starting to detect users.."
		
		
		# Create a new dataset item
		self.data = LiveDataset()
		
		
		# Create the global layout
		self.layout = QtWidgets.QVBoxLayout(self)
		
		# Create custom widgets to hold sensor's images
		self.depthImage = SensorWidget()
		self.depthImage.setGeometry(10, 10, 640, 480)
		
		# Add these custom widgets to the global layout
		self.layout.addWidget(self.depthImage)
		
		# Set the default result text
		self.resultLabel = QtWidgets.QLabel()
		self.resultLabel.setText("No")
		
		# Create the acquisition form elements
		self.create_acquision_form()
		
		
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
		frame = cv2.cvtColor(frame.astype(np.uint8), cv2.COLOR_GRAY2RGB)
		
		# Will be used to specify the depth of the current hand wished
		currentDepth, showCurrentDepth = 0, ""
		
		
		if len(self.user.users) > 0 and len(self.data.skeleton["head"]) > 0:
			# Highlight the head
			#ui.drawPoint(frame, self.data.skeleton["head"][0], self.data.skeleton["head"][1], 5)
    		
			# Display lines from elbows to the respective hands
			#ui.drawElbowLine(frame, self.data.skeleton["elbow"]["left"], self.data.skeleton["hand"]["left"])
			#ui.drawElbowLine(frame, self.data.skeleton["elbow"]["right"], self.data.skeleton["hand"]["right"])
			
			# Get the pixel's depth from the coordinates of the hands
			leftPixel = self.utils.getDepthFromMap(self.data.depth_map, self.data.skeleton["hand"]["left"])
			rightPixel = self.utils.getDepthFromMap(self.data.depth_map, self.data.skeleton["hand"]["right"])
			#print "Left hand depth: %d | Right hand depth: %d" % (leftPixel, rightPixel)
			
			
			# Get the shift of the boundaries around both hands
			leftShift = self.utils.getHandBoundShift(leftPixel)
			rightShift = self.utils.getHandBoundShift(rightPixel)
			
			if self.data.hand == self.settings.LEFT_HAND:
				currentDepth = leftPixel
				# Display a rectangle around the current hand
				#ui.drawHandBoundaries(frame, self.data.skeleton["hand"]["left"], leftShift, (200, 70, 30))
			elif self.data.hand == self.settings.RIGHT_HAND:
				currentDepth = rightPixel
				# Display a rectangle around the current hand
				#ui.drawHandBoundaries(frame, self.data.skeleton["hand"]["right"], rightShift, (200, 70, 30))
			#else:
				# Display a rectangle around both hands
				#ui.drawHandBoundaries(frame, self.data.skeleton["hand"]["left"], leftShift, (200, 70, 30))
				#ui.drawHandBoundaries(frame, self.data.skeleton["hand"]["right"], rightShift, (200, 70, 30))
			
			
			# Test the data against the neural network if possible
			if self.data.hand != self.settings.NO_HAND:
				result = self.bpn.check(self.featureExtractor.getFeatures(self.data))
				self.resultLabel.setText(str(result[0]))
				
				# Highlight the finger tip
				if result[0] != False:
					ui.drawPoint(frame, self.featureExtractor.fingerTip[result[1]][0], self.featureExtractor.fingerTip[result[1]][1], 5)
				
					# Highlight the eye
					ui.drawPoint(frame, self.featureExtractor.eyePosition[result[1]][0], self.featureExtractor.eyePosition[result[1]][1], 5)
				
					# Line of sight
					ui.drawElbowLine(frame, self.featureExtractor.eyePosition[result[1]], self.featureExtractor.fingerTip[result[1]])
			
					# Indicate orientation
					cv2.putText(frame, self.featureExtractor.orientation[result[1]], (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 2, (50, 100, 255), 5)
		
		# Update the frame
		self.depthImage.setPixmap(ui.convertOpenCVFrameToQPixmap(frame))
		
		self.timerScreen.start()
		
	
	# Create the acquisition interface form
	def create_acquision_form(self):
		globalLayout = QtWidgets.QHBoxLayout()
		
		hlayout = QtWidgets.QHBoxLayout()
		label = QtWidgets.QLabel("Pointing hand")
		label.setFixedWidth(100)
		comboBox = QtWidgets.QComboBox()
		comboBox.currentIndexChanged.connect(self.data.toggleHand)
		comboBox.setFixedWidth(200)
		comboBox.addItem("Left")
		comboBox.addItem("Right")
		comboBox.addItem("None")
		comboBox.addItem("Both")
		comboBox.setCurrentIndex(3)
		hlayout.addWidget(label)
		hlayout.addWidget(comboBox)
		globalLayout.addLayout(hlayout)
		
		self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)
		globalLayout.addWidget(self.resultLabel)
		
		self.layout.addLayout(globalLayout)