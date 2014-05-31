#! /usr/bin/python
from openni import *
import numpy as np
import sys, ctypes
import cv2
import sdl2, sdl2.ext
import hand, ui, Dataset, eventHandler, skeleton


# Get the context and initialise it
context = Context()
context.init()

# Create the depth generator to get the depth map of the scene
depth = DepthGenerator()
depth.create(context)
depth.set_resolution_preset(RES_VGA)
depth.fps = 30

# Create the image generator to get an RGB image of the scene
image = ImageGenerator()
image.create(context)
image.set_resolution_preset(RES_VGA)
image.fps = 30

# Create the user generator to detect skeletons
user = UserGenerator()
user.create(context)

# Initialise the skeleton tracking
skeleton.init(user)

# Start generating
context.start_generating_all()
print "Starting to detect users.."


def run():
	# Create a new window
	window = ui.createWindow(1280,480)
    
	# Create a new dataset item
	data = Dataset.Dataset()

	running = True
	event = sdl2.SDL_Event()
	
	while running:
		
		# Update to next frame
		context.wait_and_update_all()
		
		# Extract informations of each tracked user
		data = skeleton.track(user, depth, data)

		# Get the whole depth map
		data.depth_map = depth.map

		# Create the frame from the raw depth map string and convert it to RGB
		frame = np.fromstring(depth.get_raw_depth_map_8(), np.uint8).reshape(480, 640)
		frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
	
		# Get the RGB image of the scene
		data.image = np.fromstring(image.get_raw_image_map_bgr(), dtype=np.uint8).reshape(480, 640, 3)

		
		
		# 
		if len(user.users) > 0 and len(data.skeleton["head"]) > 0:
			# Highlight the head
			ui.drawHeadPoint(frame, data.skeleton["head"])
    
			# Display lines from elbows to the respective hands
			ui.drawElbowLine(frame, data.skeleton["elbow"]["left"], data.skeleton["hand"]["left"])
			ui.drawElbowLine(frame, data.skeleton["elbow"]["right"], data.skeleton["hand"]["right"])
		
			# Get the pixel's depth from the coordinates of the hands
			leftPixel = hand.getDepthFromMap(data.depth_map, data.skeleton["hand"]["left"])
			rightPixel = hand.getDepthFromMap(data.depth_map, data.skeleton["hand"]["right"])
			#print "Left hand depth: %d | Right hand depth: %d" % (leftPixel, rightPixel)

			# Get the shift of the boundaries around both hands
			leftShift = hand.getHandBoundShift(leftPixel)
			rightShift = hand.getHandBoundShift(rightPixel)
    
			#dataLeft = hand.extractDepthFromArea(data.depth_map, leftHandPosition, leftShift)
			#dataRight = hand.extractDepthFromArea(data.depth_map, rightHandPosition, rightShift)
    
			# Display a rectangle around both hands
			ui.drawHandBoundaries(frame, data.skeleton["hand"]["left"], leftShift, (50, 100, 255))
			ui.drawHandBoundaries(frame, data.skeleton["hand"]["right"], rightShift, (200, 70, 30))
			
		
		# Blit new frames' informations to the window
		window["array"] = ui.embedFrame(data.image, window["array"], 0, 0)
		window["array"] = ui.embedFrame(frame, window["array"], 640, 0)
		
		# Refresh the window
		ui.refresh(window["screen"])
		
		# Handle eventual events and wait 10ms
		running = eventHandler.handleEvent(event, data)
		sdl2.SDL_Delay(10)
	
	
	# The application now needs to exit
	freeResources()
	sdl2.SDL_DestroyWindow(window["screen"])
	sdl2.SDL_Quit()
	return 0

# Free used ressources
def freeResources():
	global context
	global depth
	global image
	global user
	
	del context
	del depth
	del image
	del user


if __name__ == "__main__":
	sys.exit(run())