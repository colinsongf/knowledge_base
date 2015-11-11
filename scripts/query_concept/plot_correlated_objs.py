#!/usr/bin/env python
import rospy
import numpy as npy 
import sys
import random
from scipy.stats import rankdata
from scipy.stats import truncnorm
# import matplotlib.pyplot as plt
from std_msgs.msg import String
import roslib
from nav_msgs.msg import Odometry
import sys

from mpl_toolkits.mplot3d import Axes3D
# from ar_track_alvar.msg import AlvarMarkers
# from matplotlib import *
from matplotlib.pyplot import *

number_objects = 41
number_actions = 15

object_list = npy.zeros(number_objects)
action_list = npy.zeros((number_actions,1))
search_objs = npy.zeros((number_objects,1))
search_order = npy.zeros((number_objects,1))

obj_aff_matrix = npy.loadtxt(sys.argv[1])
print (obj_aff_matrix.shape)

for j in range(0,number_actions):
	obj_aff_matrix[j] = obj_aff_matrix[j]/sum(obj_aff_matrix[j])

print("Object Affordance Matrix:")
# print(obj_aff_matrix)

correlated_objs = npy.dot(npy.transpose(obj_aff_matrix),obj_aff_matrix)


print correlated_objs.shape
for line in correlated_objs:
	print line
imshow(obj_aff_matrix, interpolation='nearest', origin='lower', extent=[0,10,0,10], aspect='auto')
show(block=False)
colorbar()
# draw()
show()




