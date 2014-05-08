#! /usr/bin/python
from openni import *
import numpy as np
import cv2

# Get the context and initialise it
context = Context()
context.init()

# This will use the depth generator to get the position of the hand
depth = DepthGenerator()
depth.create(context)
depth.set_resolution_preset(RES_VGA)
depth.fps = 30

# For the purpose of the tests, the subject will wave its hand to trigger tracking
gesture_generator = GestureGenerator()
gesture_generator.create(context)
gesture_generator.add_gesture('Wave')

# Create the generator thanks to the context
hands_generator = HandsGenerator()
hands_generator.create(context)

# Initialise the global variable stating if any hand is currently tracked
running = False

# Declare the callbacks
def gesture_detected(src, gesture, id, end_point):
    print "Detected gesture:", gesture
    hands_generator.start_tracking(end_point)

def gesture_progress(src, gesture, point, progress): pass

def create(src, id, pos, time):
    print 'Create ', id, pos
    
    global running
    running = True


def update(src, id, pos, time):
    handPosition = depth.to_projective([pos])[0]
    
    # Get the whole depth map
    depthMap = depth.map

    # Get the pixel's depth at these coordinates
    pixel = depthMap[int(handPosition[0]), int(handPosition[1])]
    print "map: %d | pos: %d" % (pixel, handPosition[2])
    
    # Create array from the raw depth map string
    frame = np.fromstring(depth.get_raw_depth_map_8(), np.uint8).reshape(480, 640)
    
    # At 1m, the hand is surrounded with a shift of 75 pixels around the center of gravity
    shift = int((1000/float(pixel))*75)
    cv2.rectangle(frame, ((int(handPosition[0])-shift),(int(handPosition[1])-shift)), ((int(handPosition[0])+shift),(int(handPosition[1])+shift)), (255, 0, 0), 5)
     
    # Render in OpenCV
    cv2.imshow("image", frame)
    cv2.waitKey(30)


def destroy(src, id, time):
    print 'Destroy ', id
    global running
    if running == True:
        running = False
        start()

# Register the callbacks
gesture_generator.register_gesture_cb(gesture_detected, gesture_progress)
hands_generator.register_hand_cb(create, update, destroy)

# Start generating
context.start_generating_all()

def start():
    print 'Make a Wave to start tracking...'

    while True:
        context.wait_any_update_all()

start()