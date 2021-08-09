import numpy as np
import math
import matplotlib.pyplot as plt
import time as tm

class body:
	def __init__(self, precession_period, obliquity):
		self.precession_period = precession_period
		self.obliquity = obliquity
		self.precession_w_dot = (2*math.pi) / self.precession_period
		self.theta = 0
		self.calcRotAxis()

	def calcRotAxis(self):
		# Axis of rotation
		self.rot_axis_unit = np.array([math.sin(self.obliquity), 0, math.cos(self.obliquity)])
		self.rot_axis_unit_origin = self.rot_axis_unit
		self.precession_axis = np.array([0,0,1])

	def update(self, dt):
		# Update theta
		self.theta += self.precession_w_dot*dt

		# Keep theta from [0, 2pi]
		'''
		if self.theta > 2*math.pi:
			num = math.floor(self.theta / (2*math.pi))
			self.theta -= num*2*math.pi
		'''
		# Rodrigues' rotation formula
		prec_temp_unit = 0;
		prec_temp_unit += self.rot_axis_unit_origin*math.cos(self.theta)
		prec_temp_unit += np.cross(self.precession_axis, self.rot_axis_unit_origin)*math.sin(self.theta)
		prec_temp_unit += self.precession_axis*np.dot(self.precession_axis, self.rot_axis_unit_origin)*(1-math.cos(self.theta))
		self.rot_axis_unit = prec_temp_unit