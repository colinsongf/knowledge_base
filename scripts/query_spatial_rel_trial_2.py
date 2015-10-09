#!/usr/bin/env python
import numpy as npy
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import rospy
from std_msgs.msg import String
import roslib
from nav_msgs.msg import Odometry
from ar_track_alvar.msg import AlvarMarkers

radius_threshold = 2
discrete_size = 100
number_objects =130

lower_bound=0
upper_bound=radius_threshold

rad_dist = npy.linspace(0,radius_threshold,discrete_size)

#READING THE spatial distribution function from file. 
pairwise_value_function = npy.loadtxt(str(sys.argv[1]))
# Note that this returned a 2D array!
print pairwise_value_function.shape
pairwise_value_function = pairwise_value_function.reshape((number_objects,number_objects,discrete_size))

value_function = numpy.zeros(shape=(discrete_size,discrete_size))

object_confidence = numpy.zeros(number_objects)


def lookup_value_add(sample_pt, alt_obj_pose, alt_obj_pose_conf):
	#########################	
	#Here, the inputs are the sample point which we are checking the value of, pose of the alternate object, and confidence of detection of the alternate object. 
	#Find radius value. 
	rad_value = ((sample_pt[0]-alt_obj_pose[0])**2+(sample_pt[0]-alt_obj_pose[1])**2)**0.5
	# rad_value = ((sample_pt.x-alt_obj_pose.x)**2+(sample_pt.y-alt_obj_pose.y)**2)**0.5

	#Find radius bucket. 
	if rad_value<rad_dist[0]:
		bucket=0;
	else if rad_value>rad_dist[len(rad_dist)-1]:
		bucket=len(rad_dist)-1
	else:
		for i in range(0,len(rad_dist)):	
			if rad_value>rad_dist[i] and rad_value<rad_dist[i+1]:
				bucket=i

	#Find value lookup to assign to the sample point. 
	value_lookup=0
	for i in range(0,number_objects):
		for j in range(0,number_objects):
			value_lookup += pairwise_value_function[i][j][bucket]

	#Return value lookup. 
	return value_lookup
	############################


#REMEMBER, this is outside the lookup_value_add function. 

def calculate_value_function(alt_obj_pose, alt_obj_pose_conf):
	for x in discrete_space_x:
		for y in discrete_space_y:
			sample = x,y
			value_function[x][y] = lookup_value_add(sample, alt_obj_pose, alt_obj_pose_conf)

# def callback(data):
#     # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
#     #rospy.loginfo(rospy.get_caller_id() + "Data read was %s", data.data)
#     trial_element=data.pose.pose.position    
#     print trial_element

#marker_list;

def ar_marker_callback(msg):
	for i in range(0,len(msg.markers)):		
		label = msg.markers[i].id
		object_confidence[label] = msg.markers[i].confidence


def listener():
    # The anonymous=True flag means that rospy will choose a unique    
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    
    rospy.init_node('listener', anonymous=True)
    # rospy.Subscriber("chatter", String, callback)
    rospy.Subscriber("/ar_pose_marker",AlvarMarkers, ar_marker_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()





