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

for j in range(0,number_actions):
	obj_aff_matrix[j] = obj_aff_matrix[j]/sum(obj_aff_matrix[j])

print("Object Affordance Matrix:")
print(obj_aff_matrix)

object_list = npy.array([0.1,0.7,0.6,0.2,0.9])
object_list = npy.transpose(object_list)	

print("Object List:") 	
print(object_list)

action_list = npy.dot(obj_aff_matrix,object_list)
for j in range(0,number_actions):
	action_list[j] = action_list[j]/sum(action_list)

obj_aff_trans = npy.transpose(obj_aff_matrix)
for j in range(0,number_actions):
	obj_aff_trans[j] = obj_aff_trans[j]/sum(obj_aff_trans[j])

search_objs = npy.dot(obj_aff_trans,action_list)
#search_objs = search_objs - object_list 

search_objs = object_list - search_objs    ###THIS SHOULD BE SEARCH_OBJS - OBJECT_LIST, but since argsort is ascending..... 
search_order = npy.argsort(search_objs)

print("Search objects:")
print(-search_objs)

print("Search order:")
print(search_order+1)

