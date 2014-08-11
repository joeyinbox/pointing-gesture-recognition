#! /usr/bin/python
import cv2, functools, numpy as np
from PyQt5 import QtGui


# Highlight the head
def drawPoint(frame, x, y, width, color=(0,0,255)):
    cv2.circle(frame, (int(x),int(y)), width, color, -1)

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