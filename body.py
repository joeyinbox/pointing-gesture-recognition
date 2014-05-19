#! /usr/bin/python
from openni import *
import numpy as np
import cv2


# Get the context and initialise it
context = Context()
context.init()

# Create the depth generator to get the depth map of the scene
depth = DepthGenerator()
depth.create(context)
depth.set_resolution_preset(RES_VGA)
depth.fps = 30

# Create the user generator to detect skeletons
user = UserGenerator()
user.create(context)

# Obtain the skeleton & pose detection capabilities
skel_cap = user.skeleton_cap


# Declare the callbacks to detect new users and start detection
def new_user(src, id):
    print "1/3 User {} detected." .format(id)
    skel_cap.request_calibration(id, True)

def calibration_start(src, id):
    print "2/3 Calibration started for user {}." .format(id)

def calibration_complete(src, id, status):
    if status == CALIBRATION_STATUS_OK:
        print "3/3 User {} successfully calibrated! Starting to track." .format(id)
        skel_cap.start_tracking(id)
    else:
        print "ERR User {} failed to calibrate. Restarting process." .format(id)
        new_user(user, id)

def lost_user(src, id):
    print "--- User {} lost." .format(id)


# Register the callbacks
user.register_user_cb(new_user, lost_user)
skel_cap.register_c_start_cb(calibration_start)
skel_cap.register_c_complete_cb(calibration_complete)




# At 1m, the hand is surrounded with a shift of 75 pixels around its center of gravity
def getHandBoundShift(depth):
    if depth == 0:
        return 75
    else:
        return int((1000/float(depth))*75)

# Return the depth value of a point from the depth map
def getDepthFromMap(depthMap, position):
    x = int(position[0])
    y = int(position[1])
    
    if x<0 or x>=depthMap.width or y<0 or y>=depthMap.height:
        return 0
    else:
        return depthMap[int(position[0]), int(position[1])]

# Draw the boundaries around the hands
def drawHandBoundaries(frame, position, shift, color):
    cv2.rectangle(frame, ((int(position[0])-shift),(int(position[1])-shift)), ((int(position[0])+shift),(int(position[1])+shift)), color, 5)








# Set the profile
skel_cap.set_profile(SKEL_PROFILE_ALL)

# Start generating
context.start_generating_all()
print "Starting to detect users.."






while True:
    # Update to next frame
    context.wait_and_update_all()
    
    # Get the whole depth map
    depthMap = depth.map
    
    # Create the frame from the raw depth map string and convert it to RGB
    frame = np.fromstring(depth.get_raw_depth_map_8(), np.uint8).reshape(480, 640)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB);

    # Extract informations of each tracked user
    for id in user.users:
        if skel_cap.is_tracking(id):
            
            # Get the informations about the two hands of this user
            # NB: Left and right are inverted on the skeleton
            leftHand = skel_cap.get_joint_position(id, SKEL_RIGHT_HAND)
            rightHand = skel_cap.get_joint_position(id, SKEL_LEFT_HAND)
            
            # Map the informations of the hands to the depth map
            leftHandPosition = depth.to_projective([leftHand.point])[0]
            rightHandPosition = depth.to_projective([rightHand.point])[0]

            # Get the pixel's depth at these coordinates
            leftPixel = getDepthFromMap(depthMap, leftHandPosition)
            rightPixel = getDepthFromMap(depthMap, rightHandPosition)
            print "Left hand depth: %d | Right hand depth: %d" % (leftPixel, rightPixel)
    
            # Get the shift of the boundaries around both hands
            leftShift = getHandBoundShift(leftPixel)
            rightShift = getHandBoundShift(rightPixel)
            
            # Display a rectangle around both hands
            drawHandBoundaries(frame, leftHandPosition, leftShift, (50, 100, 255))
            drawHandBoundaries(frame, rightHandPosition, rightShift, (200, 70, 30))
    
    # Display the depth image
    cv2.imshow("image", frame)
    cv2.waitKey(30)