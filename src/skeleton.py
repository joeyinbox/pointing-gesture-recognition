#! /usr/bin/python
from openni import *


# Initialise a global variable used within this module
skel_cap = 0

# Initialise the skeleton tracking
def init(user):
	global skel_cap
	
	# Get the skeleton capabilities
	skel_cap = user.skeleton_cap

	# Register the callbacks
	user.register_user_cb(new_user, lost_user)
	skel_cap.register_c_start_cb(calibration_start)
	skel_cap.register_c_complete_cb(calibration_complete)

	# Set the profile
	skel_cap.set_profile(SKEL_PROFILE_ALL)
	

# Callback used when a new user is detected
def new_user(src, id):
    print "1/3 User {} detected." .format(id)
    skel_cap.request_calibration(id, True)


# Callback used to calibrate a new user skeleton
def calibration_start(src, id):
    print "2/3 Calibration started for user {}." .format(id)


# Callback used to start tracking a user
def calibration_complete(src, id, status):
    if status == CALIBRATION_STATUS_OK:
        print "3/3 User {} successfully calibrated! Starting to track." .format(id)
        skel_cap.start_tracking(id)
    else:
        print "ERR User {} failed to calibrate. Restarting process." .format(id)
        new_user(user, id)


# Callback called when a user is lost
def lost_user(src, id):
    print "User {} lost.." .format(id)


# Track detected users' skeletons
def track(user, depth, data):
	for id in user.users:
		if skel_cap.is_tracking(id):
			# Get the skeleton joints informations needed
			# NB: Left and right are inverted on the skeleton
			leftHand = skel_cap.get_joint_position(id, SKEL_RIGHT_HAND)
			rightHand = skel_cap.get_joint_position(id, SKEL_LEFT_HAND)
			head = skel_cap.get_joint_position(id, SKEL_HEAD)
			leftElbow = skel_cap.get_joint_position(id, SKEL_RIGHT_ELBOW)
			rightElbow = skel_cap.get_joint_position(id, SKEL_LEFT_ELBOW)
			leftShoulder = skel_cap.get_joint_position(id, SKEL_RIGHT_SHOULDER)
			rightShoulder = skel_cap.get_joint_position(id, SKEL_LEFT_SHOULDER)
			centerShoulder = skel_cap.get_joint_position(id, SKEL_NECK)
        
			# Map the informations to the depth map within the data object
			data.skeleton["head"] = depth.to_projective([head.point])[0]
			data.skeleton["shoulder"]["left"] = depth.to_projective([leftShoulder.point])[0]
			data.skeleton["shoulder"]["right"] = depth.to_projective([rightShoulder.point])[0]
			data.skeleton["shoulder"]["center"] = depth.to_projective([centerShoulder.point])[0]
			data.skeleton["elbow"]["left"] = depth.to_projective([leftElbow.point])[0]
			data.skeleton["elbow"]["right"] = depth.to_projective([rightElbow.point])[0]
			data.skeleton["hand"]["left"] = depth.to_projective([leftHand.point])[0]
			data.skeleton["hand"]["right"] = depth.to_projective([rightHand.point])[0]
	
	return data