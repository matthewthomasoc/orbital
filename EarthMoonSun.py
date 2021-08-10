import numpy as np
import math
import matplotlib.pyplot as plt
import time as tm
from src.body.body import *

# pyplot figure setup
fig = plt.figure()
ax = plt.axes(projection = '3d')

# Sun parameters, centered at 0,0,0 w/ no orbit
Sun_radius = 696340 # radius, km
Sun_a = None # semi-major axis
Sun_e = None # eccentricity
Sun_T = None # period, seconds
Sun_i = None # inclination, rads
Sun_apsidal_period = None # apsidal precession period, seconds
Sun_axial_prec_period = None # axial precession period, seconds
Sun_axial_period = 2.333E6 # axial rotation period, seconds
Sun_obliquity = 0 # obliquity, rads

# initialize Sun body
Sun = body(Sun_radius, Sun_a, Sun_e, Sun_T, Sun_i, Sun_apsidal_period, Sun_axial_prec_period, Sun_axial_period, Sun_obliquity)

# Earth parameters, orbiting Sun
Earth_radius = 6378.14 # radius, km
Earth_a = 149.596E6 # semi-major axis
Earth_e = 0.0167 # eccentricity
Earth_T = 31558118.4 # period, seconds
Earth_i = 0 # inclination, rads
Earth_apsidal_period = 3.532032E12 # apsidal precession period, seconds
Earth_axial_prec_period = 8.1273002E11 # axial precession period, seconds
Earth_axial_period = 86164.0903 # axial rotation period, seconds
Earth_obliquity = np.radians(23.4) # obliquity, rads

# initialize Earth body
Earth = body(Earth_radius, Earth_a, Earth_e, Earth_T, Earth_i, Earth_apsidal_period, Earth_axial_prec_period, Earth_axial_period, Earth_obliquity, Sun)

# Moon parameters, orbiting Earth
Moon_radius = 1737.4 # radius, km
Moon_a = .3844E6 # semi-major axis
#Moon_e = .8 # eccentricity
Moon_e = 0.0549 # eccentricity
Moon_T = 2360594.88 # period, seconds
Moon_i = np.radians(5.145) # inclination, rads
Moon_apsidal_period = 2.7909E8 # apsidal precession period, seconds
Moon_axial_prec_period = 5.8657E8 # axial precession period, seconds
Moon_axial_period = Moon_T # axial rotation period, seconds
Moon_obliquity = np.radians(1.5) # obliquity, rads

# initialize Moon body
Moon = body(Moon_radius, Moon_a, Moon_e, Moon_T, Moon_i, Moon_apsidal_period, Moon_axial_prec_period, Moon_axial_period, Moon_obliquity, Earth)

# plot limits
ax.set_xlim([-Earth_a,Earth_a])
ax.set_ylim([-Earth_a,Earth_a])
ax.set_zlim([-Earth_a,Earth_a])

time_accel = 86400

start_time = tm.time()
last_time = start_time
max_time = Earth_axial_prec_period*25
elapsed_time = 0
while (tm.time() - start_time) * time_accel < max_time:
	print("elapsed time:", elapsed_time / 3.154E7, "years")
	cur_time = tm.time()
	dt = (cur_time - last_time) * time_accel
	elapsed_time += dt
	Sun.update(dt, ax)
	Earth.update(dt, ax)
	Moon.update(dt, ax)
	plt.draw()
	plt.pause(.01)
	last_time = cur_time
plt.show()