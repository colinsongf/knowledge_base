#!/usr/bin/env python
import numpy as npy
from scipy.stats import truncnorm
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

radius_threshold = 10

lower_bound=0
upper_bound=radius_threshold

#Defining mean and covariance values. 
#In the real system, both of these come from the learnt data. 
mean = 3
sigma = 2

#Converting to a non-zero mean. 
lower_bound = (lower_bound-mean)/sigma
upper_bound = (upper_bound-mean)/sigma

rad_dist = npy.linspace(0,radius_threshold,100)

prob_dist_func = truncnorm.pdf(rad_dist,lower_bound,upper_bound,mean,sigma)

# plt.plot(rad_dist,prob_dist_func)
# plt.show()

rad_dist_2 = npy.linspace(0,radius_threshold,100)
prob_dist_func_2 = truncnorm.pdf(rad_dist_2,lower_bound,upper_bound,mean,sigma)

# random = npy.dot(npy.transpose(prob_dist_func),prob_dist_func)


# print random

X, Y = npy.meshgrid(rad_dist,rad_dist)
R = npy.sqrt(X**2+Y**2)
Z= truncnorm.pdf(R,lower_bound,upper_bound,mean,sigma)
#x = np.arange(0,np.pi, 0.1)
#y = x.copy()
#z = np.sin(x).repeat(32).reshape(32,32)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X,Y,Z, cmap=plt.cm.jet, cstride=1, rstride=1)

plt.show()