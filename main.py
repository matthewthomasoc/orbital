import numpy as np
import math
import matplotlib.pyplot as plt
import time as tm
from src.rotation.body import *

time_accel = 3.154E7*10
fig = plt.figure()
ax = plt.axes(projection = '3d')
ax.set_xlim([-1,1])
ax.set_ylim([-1,1])
ax.set_zlim([-1,1])
start = [0,0,0]

earth_prec_period = 8.1273002E11
earth_obliquity = 0.408407
Earth = body(earth_prec_period, earth_obliquity)
A = ax.quiver(0,0,0,Earth.precession_axis[0],Earth.precession_axis[1],Earth.precession_axis[2], color="blue")
B = ax.quiver(0,0,0,Earth.rot_axis_unit_origin[0],Earth.rot_axis_unit_origin[1],Earth.rot_axis_unit_origin[2], color="red")

plt.pause(2)
start_time = tm.time()
last_time = start_time
max_time = 8.1273002E11
elapsed_time = 0
while (tm.time() - start_time) * time_accel < max_time:
	print("elapsed time:", elapsed_time / 3.154E7, "years")
	cur_time = tm.time()
	dt = (cur_time - last_time) * time_accel
	elapsed_time += dt
	Earth.update(dt)
	B.remove()
	B = ax.quiver(0,0,0,Earth.rot_axis_unit[0],Earth.rot_axis_unit[1],Earth.rot_axis_unit[2], color="red")
	plt.pause(0.01)
	plt.draw()
	last_time = cur_time
plt.show()