#! /usr/bin/python
import cv2, functools, numpy as np
from PyQt5 import QtGui, QtWidgets, QtCore
from classes.FormItem import *


# Highlight the head
def drawPoint(frame, x, y, width):
    cv2.circle(frame, (int(x),int(y)), width, (0,0,255), -1)

# Display lines from elbows to the respective hands
def drawElbowLine(frame, elbow, hand):
    cv2.line(frame, (int(elbow[0]),int(elbow[1])), (int(hand[0]),int(hand[1])), (0,0,0), 2)

# Draw the boundaries around the hands
def drawHandBoundaries(frame, position, shift, color):
    cv2.rectangle(frame, ((int(position[0])-shift),(int(position[1])-shift)), ((int(position[0])+shift),(int(position[1])+shift)), color, 5)

# Draw the depth values of an hand
def drawHandDepth(frame, data):
    for x in range(len(data)):
        for y in range(len(data[0])):
            cv2.rectangle(frame, (x*2,y*2), (x*2+2,y*2+2), (int(255-float(data[x,y])*255), int(float(data[x,y])*255), 0), 2)


# Convert an OpenCV frame to a QPixmap to be embedded as a QWidget
def convertOpenCVFrameToQPixmap(frame):
	# Convert the color
	img = cv2.cvtColor(frame, cv2.cv.CV_BGR2RGB)
	
	# Convert numpy mat to QPixmap image
	qimg = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
	return QtGui.QPixmap.fromImage(qimg)


# Create the acquisition interface form
def create_acquision_form(app, layout, data, obj):
	globalLayout = QtWidgets.QHBoxLayout()
	vlayout = QtWidgets.QVBoxLayout()
	
	groupbox = QtWidgets.QGroupBox()
	groupbox.setTitle("Pointing hand")
	groupbox_layout = QtWidgets.QVBoxLayout()
	buttonGroup = QtWidgets.QButtonGroup(groupbox_layout)
	obj.append(add_radio_button(buttonGroup, groupbox_layout, "Left hand", data.toggleLeftHand, True))
	obj.append(add_radio_button(buttonGroup, groupbox_layout, "Right hand", data.toggleRightHand))
	obj.append(add_radio_button(buttonGroup, groupbox_layout, "No hand", data.toggleNoHand))
	groupbox.setLayout(groupbox_layout)
	vlayout.addWidget(groupbox)
	
	groupbox = QtWidgets.QGroupBox()
	groupbox.setTitle("Hand")
	groupbox_layout = QtWidgets.QVBoxLayout()
	obj.append(add_text_field(groupbox_layout, "Height", 0, data.setHandHeight))
	obj.append(add_text_field(groupbox_layout, "Width", 0, data.setHandWidth))
	obj.append(add_text_field(groupbox_layout, "Thickness", 0, data.setHandThickness))
	groupbox.setLayout(groupbox_layout)
	vlayout.addWidget(groupbox)
	
	globalLayout.addLayout(vlayout)
	vlayout = QtWidgets.QVBoxLayout()
	
	groupbox = QtWidgets.QGroupBox()
	groupbox.setTitle("User")
	groupbox_layout = QtWidgets.QVBoxLayout()
	obj.append(add_text_field(groupbox_layout, "Distance", 0, data.setUserDistance))
	obj.append(add_text_field(groupbox_layout, "Height", 0, data.setUserHeight))
	obj.append(add_text_field(groupbox_layout, "Angle", 0, data.setUserAngle))
	groupbox.setLayout(groupbox_layout)
	vlayout.addWidget(groupbox)
	
	groupbox = QtWidgets.QGroupBox()
	groupbox.setTitle("Target")
	groupbox_layout = QtWidgets.QVBoxLayout()
	obj.append(add_text_field(groupbox_layout, "Distance", 0, data.setTargetDistance))
	obj.append(add_text_field(groupbox_layout, "Height", 0, data.setTargetHeight))
	obj.append(add_text_field(groupbox_layout, "Angle", 0, data.setTargetAngle))
	groupbox.setLayout(groupbox_layout)
	vlayout.addWidget(groupbox)
	
	globalLayout.addLayout(vlayout)
	vlayout = QtWidgets.QVBoxLayout()
	
	groupbox = QtWidgets.QGroupBox()
	groupbox.setTitle("Camera")
	groupbox_layout = QtWidgets.QVBoxLayout()
	obj.append(add_text_field(groupbox_layout, "Height", 1500, data.setCameraHeight))
	groupbox.setLayout(groupbox_layout)
	vlayout.addWidget(groupbox)
	
	groupbox = QtWidgets.QGroupBox()
	groupbox.setTitle("Arm")
	groupbox_layout = QtWidgets.QVBoxLayout()
	obj.append(add_text_field(groupbox_layout, "Length", 0, data.setUserArmLength))
	groupbox.setLayout(groupbox_layout)
	vlayout.addWidget(groupbox)
	
	add_options(app, vlayout, data, obj)
	
	globalLayout.addLayout(vlayout)
	layout.addLayout(globalLayout)


# Add a text input and its corresponding label to the layout
def add_text_field(parent_layout, title, value, function):
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


# Add the options section to the layout
def add_options(app, parent_layout, data, obj):
	vlayout = QtWidgets.QVBoxLayout()
	
	label = QtWidgets.QLabel("Dataset #42")
	label.setFixedWidth(405)
	label.setAlignment(QtCore.Qt.AlignCenter)
	vlayout.addWidget(label)
	
	buttonGroup = QtWidgets.QButtonGroup(vlayout)
	obj.append(add_radio_button(buttonGroup, vlayout, "Training", data.toggleTraining, True))
	obj.append(add_radio_button(buttonGroup, vlayout, "Positive testing", data.togglePositiveTesting))
	obj.append(add_radio_button(buttonGroup, vlayout, "Negative testing", data.toggleNegativeTesting))
	
	save = QtWidgets.QPushButton('Save', clicked=app.record)
	vlayout.addWidget(save)
	
	parent_layout.addLayout(vlayout)


# Add a radio button to the layout
def add_radio_button(group, parent_layout, title, function, selected=False):
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