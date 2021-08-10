import numpy as np
import math
import matplotlib.pyplot as plt
import time as tm
from src.body.body import *

# pyplot figure setup
fig = plt.figure()
ax = plt.axes(projection = '3d')

# Earth parameters, orbiting Sun
Jupiter_radius = 69911 # radius, km
Jupiter_a = None # semi-major axis
Jupiter_e = None # eccentricity
Jupiter_T = None # period, seconds
Jupiter_i = None # inclination, rads
Jupiter_apsidal_period = None # apsidal precession period, seconds
Jupiter_axial_prec_period = 1.42479521E10 # axial precession period, seconds (not sure if this is correct)
Jupiter_axial_period = 35730 # axial rotation period, seconds
Jupiter_obliquity = np.radians(3) # obliquity, rads

# initialize Jupiter body
Jupiter = body(Jupiter_radius, Jupiter_a, Jupiter_e, Jupiter_T, Jupiter_i, Jupiter_apsidal_period, Jupiter_axial_prec_period, Jupiter_axial_period, Jupiter_obliquity)

# Io parameters, orbiting Jupiter
Io_radius = 1821.6 # radius, km
Io_a = 421.8E3 # semi-major axis
Io_e = 0.004 # eccentricity
Io_T = 152853.5232 # period, seconds
Io_i = np.radians(0.04) # inclination, rads
Io_apsidal_period = -2.169654E8 # apsidal precession period, seconds (not sure if correct)
Io_axial_prec_period = None # axial precession period, seconds (couldn't find)
Io_axial_period = Io_T # axial rotation period, seconds
Io_obliquity = np.radians(1.5) # obliquity, rads

# initialize Io body
Io = body(Io_radius, Io_a, Io_e, Io_T, Io_i, Io_apsidal_period, Io_axial_prec_period, Io_axial_period, Io_obliquity, Jupiter)

# Europa parameters, orbiting Jupiter
Europa_radius = 1560.8 # radius, km
Europa_a = 671.1E3 # semi-major axis
Europa_e = 0.009 # eccentricity
Europa_T = 306882.0384 # period, seconds
Europa_i = np.radians(0.47) # inclination, rads
Europa_apsidal_period = -1.10247E9 # apsidal precession period, seconds (not sure if correct)
Europa_axial_prec_period = None # axial precession period, seconds (couldn't find)
Europa_axial_period = Europa_T # axial rotation period, seconds
Europa_obliquity = np.radians(0.1) # obliquity, rads (not measured, what?)

# initialize Europa body
Europa = body(Europa_radius, Europa_a, Europa_e, Europa_T, Europa_i, Europa_apsidal_period, Europa_axial_prec_period, Europa_axial_period, Europa_obliquity, Jupiter)

# Ganymede parameters, orbiting Jupiter
Ganymede_radius = 2631.2 # radius, km
Ganymede_a = 1070.4E3 # semi-major axis
Ganymede_e = 0.001 # eccentricity
Ganymede_T = 618153.3792 # period, seconds
Ganymede_i = np.radians(0.18) # inclination, rads
Ganymede_apsidal_period = -5.6512654E9 # apsidal precession period, seconds (not sure if correct)
Ganymede_axial_prec_period = None # axial precession period, seconds (couldn't find)
Ganymede_axial_period = Ganymede_T # axial rotation period, seconds
Ganymede_obliquity = np.radians(0.33) # obliquity, rads (between 0 - .33 deg)

# initialize Ganymede body
Ganymede = body(Ganymede_radius, Ganymede_a, Ganymede_e, Ganymede_T, Ganymede_i, Ganymede_apsidal_period, Ganymede_axial_prec_period, Ganymede_axial_period, Ganymede_obliquity, Jupiter)

# Callisto parameters, orbiting Jupiter
Callisto_radius = 2410.3 # radius, km
Callisto_a = 1882.7E3 # semi-major axis
Callisto_e = 0.007 # eccentricity
Callisto_T = 1441931.0688 # period, seconds
Callisto_i = np.radians(0.19) # inclination, rads
Callisto_apsidal_period = -4.077929E10 # apsidal precession period, seconds (not sure if correct)
Callisto_axial_prec_period = None # axial precession period, seconds (couldn't find)
Callisto_axial_period = Callisto_T # axial rotation period, seconds
Callisto_obliquity = np.radians(0) # obliquity, rads

# initialize Callisto body
Callisto = body(Callisto_radius, Callisto_a, Callisto_e, Callisto_T, Callisto_i, Callisto_apsidal_period, Callisto_axial_prec_period, Callisto_axial_period, Callisto_obliquity, Jupiter)

# plot limits
ax.set_xlim([-Callisto_a,Callisto_a])
ax.set_ylim([-Callisto_a,Callisto_a])
ax.set_zlim([-Callisto_a,Callisto_a])

# too large of a time acceleration causes major issues
time_accel = 86400

start_time = tm.time()
last_time = start_time
max_time = Callisto_T*5
elapsed_time = 0
while (tm.time() - start_time) * time_accel < max_time:
	print("elapsed time:", elapsed_time / 3.154E7, "years")
	cur_time = tm.time()
	dt = (cur_time - last_time) * time_accel
	elapsed_time += dt
	Jupiter.update(dt, ax)
	Io.update(dt, ax)
	Europa.update(dt, ax)
	Ganymede.update(dt, ax)
	Callisto.update(dt, ax)
	plt.draw()
	plt.pause(.01)
	last_time = cur_time
plt.show()