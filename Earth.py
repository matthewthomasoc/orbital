import numpy as np
import math
import matplotlib.pyplot as plt
import time as tm
from src.body.body import *

# pyplot figure setup
fig = plt.figure()
ax = plt.axes(projection = '3d')

# Earth parameters, orbiting Sun
Earth_radius = 6378.14 # radius, km
Earth_a = None # semi-major axis
Earth_e = None # eccentricity
Earth_T = None # period, seconds
Earth_i = None # inclination, rads
Earth_apsidal_period = None # apsidal precession period, seconds
Earth_axial_prec_period = 8.1273002E11 # axial precession period, seconds
Earth_axial_period = 86164.0903 # axial rotation period, seconds
Earth_obliquity = np.radians(23.4) # obliquity, rads

# initialize Earth body
Earth = body(Earth_radius, Earth_a, Earth_e, Earth_T, Earth_i, Earth_apsidal_period, Earth_axial_prec_period, Earth_axial_period, Earth_obliquity)

# plot limits
ax.set_xlim([-Earth_radius,Earth_radius])
ax.set_ylim([-Earth_radius,Earth_radius])
ax.set_zlim([-Earth_radius,Earth_radius])

# too large of a time acceleration causes major issues
time_accel = Earth_axial_prec_period / 30

start_time = tm.time()
last_time = start_time
max_time = Earth_axial_prec_period
elapsed_time = 0
while (tm.time() - start_time) * time_accel < max_time:
	print("elapsed time:", elapsed_time / 3.154E7, "years")
	cur_time = tm.time()
	dt = (cur_time - last_time) * time_accel
	elapsed_time += dt
	Earth.update(dt, ax)
	plt.draw()
	plt.pause(.01)
	last_time = cur_time
plt.show()