#! /usr/bin/python
import cv2, functools, numpy as np
from PyQt5 import QtGui


# Draw a point on the current frame
# 
# @param	frame					Reference to the current frame displayed
# @param	x						Horizontal coordinate of the head
# @param	y						Vertical coordinate of the head
# @param	width					Width of the point
# @param	color					Color of the point
# @return	None
def drawPoint(frame, x, y, width, color=(0,0,255)):
    cv2.circle(frame, (int(x),int(y)), width, color, -1)


# Display lines from elbows to the respective hands
# 
# @param	frame					Reference to the current frame displayed
# @param	elbow					Coordinates of the elbow
# @param	hand					Coordinates of the hand
# @return	None
def drawElbowLine(frame, elbow, hand):
    cv2.line(frame, (int(elbow[0]),int(elbow[1])), (int(hand[0]),int(hand[1])), (0,0,0), 2)


# Draw the boundaries around the hands
# 
# @param	frame					Reference to the current frame displayed
# @param	position				Coordinates of the hand
# @param	shift					Half of the width of the rectangle
# @param	color					Color of the rectangle
# @return	None
def drawHandBoundaries(frame, position, shift, color):
    cv2.rectangle(frame, ((int(position[0])-shift),(int(position[1])-shift)), ((int(position[0])+shift),(int(position[1])+shift)), color, 5)


# Convert an OpenCV frame to a QPixmap to be embedded as a QWidget
# 
# @param	frame					Reference to the current frame displayed
# @return	QPixmap					Newly created QPixmap
def convertOpenCVFrameToQPixmap(frame):
	# Convert the color
	img = cv2.cvtColor(frame, cv2.cv.CV_BGR2RGB)
	
	# Convert numpy mat to QPixmap image
	qimg = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
	return QtGui.QPixmap.fromImage(qimg)