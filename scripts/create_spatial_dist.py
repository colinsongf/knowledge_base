#!/usr/bin/env python
import numpy as npy
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import sys

#Copying spatial data from learnt data files. 
spatial_mean = []
spatial_dev = []

#Loading the spatial mean radius data.s
file_ob = open(str(sys.argv[1]))
for line in file_ob:
    line = line.strip()
    if len(line) > 0:
      spatial_mean.append(map(float, line.split(' ')))

#Loading spatial standard deviation data. 
file_ob = open(str(sys.argv[2]))
for line in file_ob:
	line=line.strip()
	if len(line)>0:
		spatial_dev.append(map(float,line.split(' ')))

#Defining standard parameters for gaussian. 
radius_threshold = 10
discrete_size = 100
number_objects=130

lower_bound=0
upper_bound=radius_threshold

rad_dist = npy.linspace(0,radius_threshold,discrete_size)

#NOW MUST ITERATE OVER EACH PAIR OF OBJECTS, 
#CALCULATE THE DISTRIBUTION, AND SAVE IT. 

pairwise_value_func = npy.zeros(shape=(number_objects,number_objects,discrete_size))

for i in range(0,number_objects):
	for j in range(0,number_objects):		
		if spatial_mean[i][j]>0:
			mean = spatial_mean[i][j]
			sigma = spatial_dev[i][j]
			
			#Converting to a non-zero mean. 
			lower_bound = (lower_bound-mean)/sigma
			upper_bound = (upper_bound-mean)/sigma
			
			#Creating the truncated Gaussian. 
			prob_dist_func = truncnorm.pdf(rad_dist,lower_bound,upper_bound,mean,sigma)

			# Storing the distribution in the pairwise object value function. 
			pairwise_value_func[i][j] = prob_dist_func
			
print pairwise_value_func.shape

with file('pairwise_value_function.txt','w') as outfile:
	for data_slice in pairwise_value_func:
		npy.savetxt(outfile,data_slice,fmt='%-7.2f')
		outfile.write('# New slice\n')

######In order to read the data. 
# new_data = np.loadtxt('pairwise_value_function.txt')
# # Note that this returned a 2D array!
# print new_data.shape
# new_data = new_data.reshape((number_objects,number_objects,discrete_size))
# # Just to check that they're the same...
# assert np.all(new_data == data)


# plt.plot(rad_dist,prob_dist_func)
# plt.show()

# rad_dist_2 = npy.linspace(0,radius_threshold,discrete_size)
# prob_dist_func_2 = truncnorm.pdf(rad_dist_2,lower_bound,upper_bound,mean,sigma)


#Define function that computes the value to be added to the particular point, for a particular object to find, and an alternate object.

#spatial_rel_mean is the array of radius values stored from the learn_spatial_relationships cpp file. 
#spatial_rel_cov is the array of standard deviation values stored from the learn spatial rel cpp file. 




# #################################################
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


# value_function = npy.zeros(discrete_size,discrete_size)

# for x in rad_dist:
# 	for y in rad_dist:		
# 		sample=x,y
# 		for alt_obj_ind in range(0,number_objects):			
# 			value_function[x][y]+=lookup_value_add(find_obj, alt_obj_ind, sample, alt_obj_pose, alt_obj_pose_conf)


