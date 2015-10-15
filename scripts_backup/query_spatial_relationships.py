#!/usr/bin/env python
import numpy as npy
from scipy.stats import truncnorm
import matplotlib.pyplot as plt

radius_threshold = 20
discrete_size = 100

lower_bound=0
upper_bound=radius_threshold

#Defining mean and standard deviation values. 
#In the real system, both of these come from the learnt data. 
mean = 5
sigma = 3

#Converting to a non-zero mean. 
lower_bound = (lower_bound-mean)/sigma
upper_bound = (upper_bound-mean)/sigma

rad_dist = npy.linspace(0,radius_threshold,discrete_size)

prob_dist_func = truncnorm.pdf(rad_dist,lower_bound,upper_bound,mean,sigma)

plt.plot(rad_dist,prob_dist_func)
plt.show()

rad_dist_2 = npy.linspace(0,radius_threshold,discrete_size)
prob_dist_func_2 = truncnorm.pdf(rad_dist_2,lower_bound,upper_bound,mean,sigma)

#Define function that computes the value to be added to the particular point, for a particular object to find, and an alternate object.

#spatial_rel_mean is the array of radius values stored from the learn_spatial_relationships cpp file. 
#spatial_rel_cov is the array of standard deviation values stored from the learn spatial rel cpp file. 

def lookup_value_add(find_obj_index, alt_obj_index, sample_pt, alt_obj_pose, alt_obj_pose_conf):
	#We take inputs as the index of the object that we would like to find, index of the object we are comparing with, 
	#Sample point which we are checking the value of, pose of the alternate object, and confidence of detection of the alternate object. 

	#The mean radius and standard deviation are defined pairwise, so we look up this data. 
	mean_rad_obj = spatial_rel_mean[find_obj_index][alt_obj_index]
	dev_rad_obj = spatial_rel_dev[find_obj_index][alt_obj_index]

	lower_bound_calc = (lower_bound - mean_rad_obj) / dev_rad_obj
	upper_bound_calc = (upper_bound - mean_rad_obj) / dev_rad_obj

	prob_dist_func = truncnorm.pdf(rad_dist,lower_bound_calc,upper_bound_calc,mean_rad_obj,dev_rad_obj)

	##Calculate radius as norm of sample point minus the alt_obj_pose 
	#radius_val = 

	#Must calculate the radius bucket that this particular location falls into. 
	for i in range(0,discrete_size-1):
		if (radius_val>rad_dist[i]) and (radius_val<rad_dist[i+1]):
			bucket = i

	value_add = alt_obj_pose_conf * prob_dist_func(bucket)
	return value_add




