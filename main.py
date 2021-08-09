import numpy as np
import math
import matplotlib.pyplot as plt
import time as tm
#from src.rotation.body import *
from src.orbit.orbit import *

Moon_a = .3844E6 # semi-major axis
Moon_e = 0.0549 # eccentricity
Moon_T = 2360594.88 # period, seconds
Moon_i = np.radians(5.145) # inclination, rads
Moon_apsidal_period = 2.7909E8 # apsidal precession period, seconds
# initialize Moon body
Moon = body(Moon_a, Moon_e, Moon_T, Moon_i, Moon_apsidal_period)

time_accel = Moon_T * .5 # .5 period / sec # time acceleration

# pyplot figure setup
fig = plt.figure()
ax = plt.axes(projection = '3d')
ax.set_xlim([-1E6,1E6])
ax.set_ylim([-1E6,1E6])
ax.set_zlim([-1E6,1E6])
A = ax.quiver(0,0,0,Moon.periapsis_unit[0]*1E6,Moon.periapsis_unit[1]*1E6,Moon.periapsis_unit[2]*1E6, color="blue")
B = ax.quiver(0,0,0,Moon.orbit_axis[0]*1E6,Moon.orbit_axis[1]*1E6,Moon.orbit_axis[2]*1E6, color="red")

start_time = tm.time()
last_time = start_time
max_time = Moon_apsidal_period
elapsed_time = 0
prev_pos = None
while (tm.time() - start_time) * time_accel < max_time:
	print("elapsed time:", elapsed_time / 3.154E7, "years")
	cur_time = tm.time()
	dt = (cur_time - last_time) * time_accel
	elapsed_time += dt
	Moon.update(dt)
	B.remove()
	A.remove()
	A = ax.quiver(0,0,0,Moon.periapsis_unit[0],Moon.periapsis_unit[1],Moon.periapsis_unit[2], color="blue")
	B = ax.quiver(0,0,0,Moon.orbit_axis[0]*1E6,Moon.orbit_axis[1]*1E6,Moon.orbit_axis[2]*1E6, color="red")
	pos = Moon.position
	if prev_pos is not None:
		ax.plot3D([pos[0],prev_pos[0]], [pos[1],prev_pos[1]], [pos[2],prev_pos[2]], 'gray')
	plt.pause(0.01)
	plt.draw()
	last_time = cur_time
	prev_pos = pos
plt.show()