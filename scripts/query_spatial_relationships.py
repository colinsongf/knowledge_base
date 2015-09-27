#!/usr/bin/env python
import numpy as npy
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
radius_threshold = 20

lower_bound=0
upper_bound=radius_threshold

#Defining mean and covariance values. 
#In the real system, both of these come from the learnt data. 
mean = 5
sigma = 3

#Converting to a non-zero mean. 
lower_bound = (lower_bound-mean)/sigma
upper_bound = (upper_bound-mean)/sigma

rad_dist = npy.linspace(0,radius_threshold,100)

prob_dist_func = truncnorm.pdf(rad_dist,lower_bound,upper_bound,mean,sigma)

plt.plot(rad_dist,prob_dist_func)
plt.show()

rad_dist_2 = npy.linspace(0,radius_threshold,100)
prob_dist_func_2 = truncnorm.pdf(rad_dist_2,lower_bound,upper_bound,mean,sigma)

