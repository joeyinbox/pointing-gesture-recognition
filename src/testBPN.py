#! /usr/bin/python
from classes.BPNTraining import *
import numpy as np
import sys




#training = np.arange(7, 39)
#positive = [41, 47]
#negative = [6, 40]


positive = [0, 1, 2, 3, 4, 7, 8, 10, 11, 12, 13, 15, 16, 17, 18, 21, 22, 26, 30, 31, 32, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 47, 49, 50, 52, 53, 54, 55, 58, 59, 60, 61, 64, 67, 78, 80, 81, 82, 86, 87, 88, 89, 96, 97, 98, 99, 101, 102, 103, 106, 116, 118, 119, 122, 123, 124, 126, 127, 128, 129, 131, 132, 133, 136, 137, 138, 140, 145, 151, 152, 153, 156, 157, 158, 160, 161, 162, 163, 165, 166, 167, 168, 169, 171, 174, 175]





#positive = np.arange(30, 181)
negative = np.arange(0, 10)



bpn = BPNTraining([], positive, negative)
bpn.run()

sys.exit(1)