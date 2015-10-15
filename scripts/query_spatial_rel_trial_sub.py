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

lower_bound=0
upper_bound=radius_threshold

rad_dist = npy.linspace(0,radius_threshold,discrete_size)

# prob_dist_func = truncnorm.pdf(rad_dist,lower_bound,upper_bound,mean,sigma)

# plt.plot(rad_dist,prob_dist_func)
# plt.show()

# rad_dist_2 = npy.linspace(0,radius_threshold,discrete_size)
# prob_dist_func_2 = truncnorm.pdf(rad_dist_2,lower_bound,upper_bound,mean,sigma)

#Define function that computes the value to be added to the particular point, for a particular object to find, and an alternate object.

#spatial_rel_mean is the array of radius values stored from the learn_spatial_relationships cpp file. 
#spatial_rel_cov is the array of standard deviation values stored from the learn spatial rel cpp file. 


#READING THE spatial distribution function from file. 
pairwise_value_function = npy.loadtxt(str(sys.argv[1]))
# Note that this returned a 2D array!
print pairwise_value_function.shape
pairwise_value_function = pairwise_value_function.reshape((number_objects,number_objects,discrete_size))

# def lookup_value_add(find_obj_index, alt_obj_index, sample_pt, alt_obj_pose, alt_obj_pose_conf):
# 	#We take inputs as the index of the object that we would like to find, index of the object we are comparing with, 
# 	#Sample point which we are checking the value of, pose of the alternate object, and confidence of detection of the alternate object. 

# 	#The mean radius and standard deviation are defined pairwise, so we look up this data. 
# 	mean_rad_obj = spatial_rel_mean[find_obj_index][alt_obj_index]
# 	dev_rad_obj = spatial_rel_dev[find_obj_index][alt_obj_index]

# 	lower_bound_calc = (lower_bound - mean_rad_obj) / dev_rad_obj
# 	upper_bound_calc = (upper_bound - mean_rad_obj) / dev_rad_obj

# 	prob_dist_func = truncnorm.pdf(rad_dist,lower_bound_calc,upper_bound_calc,mean_rad_obj,dev_rad_obj)

# 	##Calculate radius as norm of sample point minus the alt_obj_pose 
# 	#radius_val = 

# 	#Must calculate the radius bucket that this particular location falls into. 
# 	for i in range(0,discrete_size-1):
# 		if (radius_val>rad_dist[i]) and (radius_val<rad_dist[i+1]):
# 			bucket = i

# 	value_add = alt_obj_pose_conf * prob_dist_func(bucket)
# 	return value_add

def lookup_value_add(sample_pt, alt_obj_pose, alt_obj_pose_conf):
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

#REMEMBER, this is outside the lookup_value_add function. 
value_function = numpy.zeros(shape=(discrete_size,discrete_size))
for x in discrete_space_x:
	for y in discrete_space_y:
		sample = x,y
		value_function[x][y] = lookup_value_add(sample, alt_obj_pose, alt_obj_pose_conf)

def callback(data):
    # rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    #rospy.loginfo(rospy.get_caller_id() + "Data read was %s", data.data)
    trial_element=data.pose.pose.position    
    print trial_element
    
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique    
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    
    rospy.init_node('listener', anonymous=True)
    # rospy.Subscriber("chatter", String, callback)
    rospy.Subscriber("/az3/base_controller/odom", Odometry, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()





