#! /usr/bin/python
import cv2


# Highlight the head
def drawHeadPoint(frame, position):
    cv2.circle(frame, (int(position[0]),int(position[1])), 5, (0,0,255), -1)

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