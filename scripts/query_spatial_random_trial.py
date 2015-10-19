#!/usr/bin/env python
import numpy as npy
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import rospy
from std_msgs.msg import String
import roslib
from nav_msgs.msg import Odometry
import sys

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# from ar_track_alvar.msg import AlvarMarkers
import random

radius_threshold = 5
discrete_size = 100

discrete_space_x = 20
discrete_space_y = 20
max_dist = 5

#Dummy set of variables for the random object spatial querying. 
space_dist = npy.linspace(-max_dist,max_dist,discrete_space_x)

# number_objects = 130
number_objects = 41

lower_bound=0
upper_bound=radius_threshold

rad_dist = npy.linspace(0,radius_threshold,discrete_size)
print rad_dist

#READING THE spatial distribution function from file. 
pairwise_value_function = npy.loadtxt(str(sys.argv[1]))
# Note that this returned a 2D array!
print pairwise_value_function.shape
pairwise_value_function = pairwise_value_function.reshape((number_objects,number_objects,discrete_size))

value_function = npy.zeros(shape=(discrete_space_x,discrete_space_y))
# number_objects = 41
object_confidence = npy.zeros(number_objects)
object_poses = npy.zeros(shape=(number_objects,2))

# number_objects = 41
def random_obj_positions():
	number_scene_objects = 30

	for i in range(0,number_scene_objects):		
		trial_label = random.randrange(0,number_objects)
		object_confidence[trial_label] = random.random()
 		object_poses[trial_label][0] = random.randrange(-2,2)+random.randrange(0,3)
 		object_poses[trial_label][1] = random.randrange(-2,2)+random.randrange(0,3)

 	print "Object Poses:",object_poses
 	print "Object confidences:",object_confidence

random_obj_positions()

#REMEMBER, this is outside the lookup_value_add function. 

def lookup_value_add(sample_pt, obj_index):
	#########################	
	#Here, the inputs are the sample point which we are checking the value of, pose of the alternate object, and confidence of detection of the alternate object. 

	# print "Reached point 2."
	#Find radius value. 	
	rad_value = (((sample_pt[0]-object_poses[obj_index][0])**2)+((sample_pt[0]-object_poses[obj_index][1])**2))**0.5
	# rad_value = ((sample_pt.x-alt_obj_pose.x)**2+(sample_pt.y-alt_obj_pose.y)**2)**0.5
	# print "Radius value:",rad_value
	#Find radius bucket. 
	if rad_value<rad_dist[0]:
		bucket=0;
	elif rad_value>rad_dist[len(rad_dist)-1]:
		bucket=len(rad_dist)-1
	else:
		for i in range(0,len(rad_dist)):	
			if rad_value>rad_dist[i] and rad_value<rad_dist[i+1]:
				bucket=i

	print sample_pt, rad_value, bucket
	# print "Bucket:",bucket
	#Find value lookup to assign to the sample point. 

	value_lookup=0
	for i in range(0,number_objects):
		for j in range(0,number_objects):
			value_lookup += pairwise_value_function[i][j][bucket]
	# print "Value lookup.",value_lookup

	#Return value lookup. 
	return value_lookup
	###########################

def calculate_value_function(obj_index):
	# for x in discrete_space_x:
		# for y in discrete_space_y:
	# print "Reached point 1."
	for i in range(0,discrete_space_x): 
		# print "Reached point 2.",i
		for j in range(0,discrete_space_y):			
			
			sample = space_dist[i],space_dist[j]
			# print sample
			x = lookup_value_add(sample, obj_index)			
			value_function[i][j]=x

calculate_value_function(4)

print npy.any(value_function)

for i in range(0,discrete_space_x):
	print value_function[i]

fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
X,Y=npy.meshgrid(space_dist,space_dist)
ax.plot_surface(X,Y,value_function,cmap=plt.cm.jet, cstride=1, rstride=1)
plt.show()


# def callback(data):
#     # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
#     #rospy.loginfo(rospy.get_caller_id() + "Data read was %s", data.data)
#     trial_element=data.pose.pose.position    
#     print trial_element

#marker_list;



# def ar_marker_callback(msg):
# 	for i in range(0,len(msg.markers)):		
# 		label = msg.markers[i].id
# 		object_confidence[label] = msg.markers[i].confidence
# 		object_poses[label][0] = msg.markers[i].pose.pose.position.x
# 		object_poses[label][1] = msg.markers[i].pose.pose.position.y




# def listener():
#     # The anonymous=True flag means that rospy will choose a unique    
#     # name for our 'listener' node so that multiple listeners can
#     # run simultaneously.
    
#     rospy.init_node('listener', anonymous=True)
#     # rospy.Subscriber("chatter", String, callback)
#     rospy.Subscriber("/ar_pose_marker",AlvarMarkers, ar_marker_callback)

#     # spin() simply keeps python from exiting until this node is stopped
#     rospy.spin()
  
# if __name__ == '__main__':
#     listener()





