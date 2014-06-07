#!/usr/bin/python
from PyQt5 import QtCore, QtWidgets, QtGui
from openni import *
import numpy as np
import cv2, ctypes, hand, skeleton, ui

from classes.Dataset import *
from classes.FormItem import *


class DatasetGui(QtWidgets.QWidget):
	def __init__(self):
		super(DatasetGui, self).__init__()
		

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
		
		self.imageLabel = QtWidgets.QLabel()
		self.imageLabel.setGeometry(10, 10, 400, 100)
		
		self.imageLabel2 = QtWidgets.QLabel()
		self.imageLabel2.setGeometry(10, 10, 400, 100)
		
		layout = QtWidgets.QVBoxLayout(self)
		hlayout = QtWidgets.QHBoxLayout()
		hlayout.addWidget(self.imageLabel)
		hlayout.addWidget(self.imageLabel2)
		layout.addLayout(hlayout)
		
		ui.create_acquision_form(layout, self.data)
		
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
			ui.drawHeadPoint(frame, self.data.skeleton["head"])
    
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
    
			#dataLeft = hand.extractDepthFromArea(data.depth_map, leftHandPosition, leftShift)
			#dataRight = hand.extractDepthFromArea(data.depth_map, rightHandPosition, rightShift)
    
			# Display a rectangle around both hands
			ui.drawHandBoundaries(frame, self.data.skeleton["hand"]["left"], leftShift, (50, 100, 255))
			ui.drawHandBoundaries(frame, self.data.skeleton["hand"]["right"], rightShift, (200, 70, 30))
		
		
		
		self.imageLabel.setPixmap(ui.convertOpenCVFrameToQPixmap(frame))
		self.imageLabel2.setPixmap(ui.convertOpenCVFrameToQPixmap(self.data.image))
		
		self.timerScreen.start()