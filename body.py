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
        return depthMap[x, y]

# Draw the boundaries around the hands
def drawHandBoundaries(frame, position, shift, color):
    cv2.rectangle(frame, ((int(position[0])-shift),(int(position[1])-shift)), ((int(position[0])+shift),(int(position[1])+shift)), color, 5)

# Draw the depth values of an hand
def drawHandDepth(frame, data):
    for x in range(len(data)):
        for y in range(len(data[0])):
            cv2.rectangle(frame, (x*2,y*2), (x*2+2,y*2+2), (int(255-float(data[x,y])*255), int(float(data[x,y])*255), 0), 2)




# Extract depth data from a specifed area
def extractDepthFromArea(depthMap, position, shift):
    result = np.zeros(shape=(2*shift+1, 2*shift+1))
    
    i = 0
    for x in range(int(position[0])-shift, int(position[0])+shift):
        j = 0
        for y in range(int(position[1])-shift, int(position[1])+shift):
            if x>=0 and x<depthMap.width and y>=0 and y<depthMap.height:
                result[i, j] = convertDepthToRange(depthMap[x, y])
            j += 1
        i += 1
    
    return result

# Convert depth data to a value within the range 1-0 (with 1 for smallest values from 500 to 4000 mm)
def convertDepthToRange(depth):
    maxDepth = 4000
    minDepth = 500
    
    if depth>=minDepth and depth<=maxDepth:
        return round((maxDepth-float(depth))/(maxDepth-minDepth), 3)
    return 0

# Write array values to a file
def writeToFile(data):
    f = open('result.txt','w')
    for x in xrange(len(data)):
        f.write("[")
        for y in xrange(len(data[0])):
            f.write(("%.3f,"%(data[x,y])))
        f.write("]\n")




# Set the profile
skel_cap.set_profile(SKEL_PROFILE_ALL)

# Start generating
context.start_generating_all()
print "Starting to detect users.."

inc = 0

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
            
            # Get the skeleton joints informations needed
            # NB: Left and right are inverted on the skeleton
            leftHand = skel_cap.get_joint_position(id, SKEL_RIGHT_HAND)
            rightHand = skel_cap.get_joint_position(id, SKEL_LEFT_HAND)
            head = skel_cap.get_joint_position(id, SKEL_HEAD)
            leftElbow = skel_cap.get_joint_position(id, SKEL_RIGHT_ELBOW)
            rightElbow = skel_cap.get_joint_position(id, SKEL_LEFT_ELBOW)
            
            # Map the informations to the depth map
            leftHandPosition = depth.to_projective([leftHand.point])[0]
            rightHandPosition = depth.to_projective([rightHand.point])[0]
            headPosition = depth.to_projective([head.point])[0]
            leftElbowPosition = depth.to_projective([leftElbow.point])[0]
            rightElbowPosition = depth.to_projective([rightElbow.point])[0]
            
            # Highlight the head
            cv2.circle(frame, (int(headPosition[0]),int(headPosition[1])) , 5, (0,0,255), -1)
            
            # Display lines from elbows to the respective hands
            cv2.line(frame, (int(leftElbowPosition[0]),int(leftElbowPosition[1])), (int(leftHandPosition[0]),int(leftHandPosition[1])), (0,0,0), 2)
            cv2.line(frame, (int(rightElbowPosition[0]),int(rightElbowPosition[1])), (int(rightHandPosition[0]),int(rightHandPosition[1])), (0,0,0), 2)
            

            # Get the pixel's depth from the coordinates of the hands
            leftPixel = getDepthFromMap(depthMap, leftHandPosition)
            rightPixel = getDepthFromMap(depthMap, rightHandPosition)
            print "Left hand depth: %d | Right hand depth: %d" % (leftPixel, rightPixel)
    
            # Get the shift of the boundaries around both hands
            leftShift = getHandBoundShift(leftPixel)
            rightShift = getHandBoundShift(rightPixel)
            
            # Display a rectangle around both hands
            drawHandBoundaries(frame, leftHandPosition, leftShift, (50, 100, 255))
            drawHandBoundaries(frame, rightHandPosition, rightShift, (200, 70, 30))
            
            #dataLeft = extractDepthFromArea(depthMap, leftHandPosition, leftShift)
            #dataRight = extractDepthFromArea(depthMap, rightHandPosition, rightShift)
    
    # Display the depth image
    cv2.imshow("image", frame)
    cv2.waitKey(10)