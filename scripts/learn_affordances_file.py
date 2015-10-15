#!/usr/bin/env python

import rospy
import numpy as npy 
import sys

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

number_objects = 5
number_actions = 4
number_scenes = 1

number_objects_full = 130

# object_occurance = npy.zeros((130,1))
# object_list = npy.zeros((number_objects,1))
action_list = npy.zeros((number_actions,1))
search_objs = npy.zeros((number_objects,1))
search_order = npy.zeros((number_objects,1))

scene_obj_matrix = npy.zeros((number_scenes,number_objects_full))
scene_act_matrix = npy.zeros((number_scenes,number_actions))
obj_aff_matrix = npy.zeros((number_actions,number_objects_full))

scene_ind=0;
for file_id in range(1,len(sys.argv)):	
	file_ob = open(str(sys.argv[file_id]))
	line_ind=0; 
	for line in file_ob:		
		x=line
		x=x.rstrip('\n')		
		if x=='1':			
			scene_obj_matrix[scene_ind][line_ind]=1
		line_ind+=1
	scene_ind+=1
	print scene_ind

# print scene_obj_matrix

scene_act_matrix = npy.array([[0.,1.,1.,0]])		
# print scene_act_matrix.shape
	
inv_scene_obj_mat = npy.linalg.pinv(scene_obj_matrix)
print inv_scene_obj_mat.shape

print scene_act_matrix.shape

obj_aff_matrix = npy.dot(inv_scene_obj_mat,scene_act_matrix)
obj_aff_matrix = npy.transpose(obj_aff_matrix)
for j in range(0,number_actions):
	obj_aff_matrix[j]=obj_aff_matrix[j]/sum(obj_aff_matrix[j])

print("Object Affordance Matrix:")
print(obj_aff_matrix)

