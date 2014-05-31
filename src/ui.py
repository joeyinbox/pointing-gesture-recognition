#! /usr/bin/python
import cv2, sdl2, numpy as np


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

# Embed an array in the frame
def embedFrame(frame, data, x, y):
	# Add an alpha channel and rotate values to fit into the initial shape
	frame = np.insert(frame,3,255,axis=2)
	frame = np.rot90(frame)
	
	data[x:x+frame.shape[0], y:y+frame.shape[1]] = frame
	
	return data

# Create the SDL window
def createWindow(width, height):
	sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
	
	data = {
		"screen": sdl2.SDL_CreateWindow(b"Pointing Gesture Recognition", sdl2.SDL_WINDOWPOS_CENTERED, sdl2.SDL_WINDOWPOS_CENTERED, width, height, sdl2.SDL_WINDOW_SHOWN),
		"surface":0,
		"array":0
	}
	data["surface"] = sdl2.SDL_GetWindowSurface(data["screen"])
	data["array"] = sdl2.ext.pixels3d(data["surface"].contents)
	
	return data

# Refresh the SDL window
def refresh(window):
	sdl2.SDL_UpdateWindowSurface(window)

# Initialise the SDL window