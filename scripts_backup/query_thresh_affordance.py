#!/usr/bin/env python
import rospy
import numpy as npy 

number_objects = 5
number_actions = 4

# object_list = npy.zeros((number_objects,1))
action_list = npy.zeros((number_actions,1))
search_objs = npy.zeros((number_objects,1))
search_order = npy.zeros((number_objects,1))

# obj_aff_matrix = numpy.zeros((number_actions,number_objects))

obj_aff_matrix = npy.array([[1.,1.,0,0,1.],[1.,1.,0,1.,0],[1.,0,1.,0,1.],[0,1.,0,1.,1.]])

print("Object Affordance Matrix:")
print(obj_aff_matrix)

obj_aff_trans = npy.transpose(obj_aff_matrix)
print("Object Affordance Matrix transpose")
print(obj_aff_trans)

for j in range(0,number_actions):
	obj_aff_matrix[j] = obj_aff_matrix[j]/sum(obj_aff_matrix[j])

print("Object Affordance Matrix:")
print(obj_aff_matrix)



object_list = npy.array([0.1,0.7,0.6,0.2,0.9])
object_list = npy.transpose(object_list)	

print("Object List:") 	
print(object_list)

action_list = npy.dot(obj_aff_matrix,object_list)
action_list_thresh = npy.dot(obj_aff_matrix,object_list)
threshold=0.3

for j in range(0,number_actions):
	action_list[j] = action_list[j]/sum(action_list)
	action_list_thresh[j] = action_list_thresh[j]/sum(action_list_thresh)
	# if action_list_thresh[j]<threshold:
		# action_list_thresh[j]=0

print("Action List:")
print(action_list)

for j in range(0,number_actions):
	if action_list_thresh[j]<threshold:
		action_list_thresh[j]=0

print("Action List Thresholded")
print(action_list_thresh)

# obj_aff_trans = npy.transpose(obj_aff_matrix)

for j in range(0,number_actions):
	obj_aff_trans[j] = obj_aff_trans[j]/sum(obj_aff_trans[j])

search_objs = npy.dot(obj_aff_trans,action_list)
search_objs_thresh = npy.dot(obj_aff_trans,action_list_thresh)

search_objs = search_objs - object_list 
search_objs_thresh = search_objs_thresh - object_list
# search_objs = object_list - search_objs    ###THIS SHOULD BE SEARCH_OBJS - OBJECT_LIST, but since argsort is ascending..... 

search_order = npy.argsort(-search_objs)

search_order_thresh = npy.argsort(-search_objs_thresh)




print("Search objects:")
print(search_objs)

print("Search order:")
print(search_order+1)

print("Search Objects Thresholded:")
print(search_objs_thresh)

print("Search Order Thresholded:")
print(search_order_thresh+1)

