import numpy as np
import math

class rotation:
	def __init__(self, axial_prec_period, axial_period, obliquity):
		self.axial_prec_period = axial_prec_period
		self.axial_period = axial_period
		self.obliquity = obliquity
		if self.axial_prec_period is not None:
			self.precession_w_dot = (2*math.pi) / self.axial_prec_period
			self.theta_prec = 0
		self.axial_w_dot = (2*math.pi) / self.axial_period
		self.theta_axial = 0
		self.calcRotAxis()

	def calcRotAxis(self):
		# Axis of rotation
		self.axial_rot_axis= np.array([math.sin(self.obliquity), 0, math.cos(self.obliquity)])
		self.precession_axis = np.array([0,0,1])
		self.orientation = np.array([math.sin(self.obliquity + math.pi/2), 0, math.cos(self.obliquity + math.pi/2)])

	# Rodrigues' rotation formula
	def rotatevec(self, axis, vector, theta):
		result = 0;
		result += vector*math.cos(theta)
		result += np.cross(axis, vector)*math.sin(theta)
		result += axis*np.dot(axis, vector)*(1-math.cos(theta))
		return result

	def update(self, dt):
		# Update theta
		if self.axial_prec_period is not None:
			dtheta_prec = self.precession_w_dot*dt
			self.theta_prec += dtheta_prec

			# Keep precession theta from [0, 2pi]
			if self.theta_prec > 2*math.pi:
				num = math.floor(self.theta_prec / (2*math.pi))
				self.theta_prec -= num*2*math.pi

			# Update rotation axis
			self.axial_rot_axis = self.rotatevec(self.precession_axis, self.axial_rot_axis, dtheta_prec)

		dtheta_axial = self.axial_w_dot*dt
		self.theta_axial += dtheta_axial

		# Keep axial theta from [0, 2pi]
		if self.theta_axial > 2*math.pi:
			num = math.floor(self.theta_axial / (2*math.pi))
			self.theta_axial -= num*2*math.pi

		# Update orientation
		self.orientation = self.rotatevec(self.axial_rot_axis, self.orientation, dtheta_axial)
		print(np.dot(self.orientation, self.axial_rot_axis))