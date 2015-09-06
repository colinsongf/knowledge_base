#!/usr/bin/env python

import rospy
import numpy as npy 

number_objects = 5
number_actions = 4
number_scenes = 5

# object_list = npy.zeros((number_objects,1))
action_list = npy.zeros((number_actions,1))
search_objs = npy.zeros((number_objects,1))
search_order = npy.zeros((number_objects,1))

scene_obj_matrix = npy.zeros(number_scenes,number_objects)
scene_act_matrix = npy.zeros(number_scenes,number_actions)
obj_aff_matrix = npy.zeros((number_actions,number_objects))

for k in range(0,number_scenes):
	for i in range(0,number_objects)
		if (in_scene_obj(k,i))
			scene_obj_matrix[k][i] = 1
	for j in range(0,number_actions)
		if (in_scene_act(k,j))
			scene_act_matrix[k][j] = 1

for j in range(0,number_actions)
	obj_aff_matrix = npy.dot(npy.pinv(scene_obj_matrix),scene_act_matrix[:][j])
	obj_aff_matrix[j] = obj_aff_matrix[j]/sum(obj_aff_matrix[j])

print("Object Affordance Matrix:")
print(obj_aff_matrix)
