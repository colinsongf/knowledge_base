#!/usr/bin/env python
import sys
import numpy as npy

number_objects_1=41
number_objects_2=130

# object_index_mapping = npy.zeros(number_objects_1)
object_index_mapping = []

file_ob = open(str(sys.argv[1]))
for line in file_ob:
    line = line.strip()
    if len(line) > 0:
    	object_index_mapping.append(map(float, line.split(' ')))

print object_index_mapping
