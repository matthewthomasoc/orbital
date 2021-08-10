import numpy as np
import math

class orbit:
	def __init__(self, a, e, orbit_period, inclination, apsidal_prec_period, parent = None):
		self.a = a
		self.e = e
		self.orbit_period = orbit_period
		self.inclination = inclination
		self.apsidal_prec_period = apsidal_prec_period
		self.theta_apsidal = 0
		self.theta_orbit = 0
		self.radius = None
		self.smoothPath = []
		self.parent = parent
		self.position = [0,0,0]
		self.calculateParameters()

	def calculateParameters(self):
		# Calculate rotational velocity
		self.w_dot = (2*math.pi) / self.orbit_period
		self.w_apsidal_dot = (2*math.pi) / self.apsidal_prec_period

		# Calculate periapsis, apoapsis radius
		p = self.a * (1 - self.e * self.e)
		self.rp = p / (1 + self.e)
		self.ra = p / (1 - self.e)

		# Calculate unit vectors
		self.orbit_axis = np.array([-math.sin(self.inclination), 0, math.cos(self.inclination)])
		self.periapsis_unit = np.array([-math.cos(self.inclination), 0, -math.sin(self.inclination)])

	# Rodrigues' rotation formula
	def rotatevec(self, axis, vector, theta):
		result = 0;
		result += vector*math.cos(theta)
		result += np.cross(axis, vector)*math.sin(theta)
		result += axis*np.dot(axis, vector)*(1-math.cos(theta))
		return result

	# Update orbit
	def update(self, dt):
		# Update orbital theta
		dtheta_orbit = self.w_dot * dt
		self.theta_orbit += dtheta_orbit

		# Update apsidal theta
		dtheta_apsidal = self.w_apsidal_dot * dt
		self.theta_apsidal += dtheta_apsidal

		# Keep apsidal theta from [0, 2pi] for readability
		if self.theta_apsidal > 2*math.pi:
			num = math.floor(self.theta_apsidal / (2*math.pi))
			self.theta_apsidal -= num*2*math.pi

		# Keep orbital theta from [0, 2pi] for readability
		if self.theta_orbit > 2*math.pi:
			num = math.floor(self.theta_orbit / (2*math.pi))
			self.theta_orbit -= num*2*math.pi

		# Update orbital radius
		self.radius = (self.a * (1 - self.e*self.e)) / (1 + self.e * math.cos(self.theta_orbit))

		# Update orbit axis
		prec_axis = np.array([0,0,1])
		self.orbit_axis = self.rotatevec(prec_axis, self.orbit_axis, dtheta_apsidal)

		# Update orbit periapsis unit vector
		self.periapsis_unit = self.rotatevec(self.orbit_axis, self.periapsis_unit, dtheta_apsidal)
		self.periapsis = self.periapsis_unit * self.rp

		# Update orbit position unit vector
		self.position_unit = self.rotatevec(self.orbit_axis, self.periapsis_unit, self.theta_orbit)
		self.position = self.position_unit * self.radius

		# Add body position to parent position, if exists
		if self.parent is not None:
			if self.parent.orbit is not None:
				self.position += self.parent.orbit.position

		# Create smooth path using linear interpolation
		self.smoothPath = []
		thetas = np.linspace(self.theta_orbit - dtheta_orbit, self.theta_orbit, 1000)
		for i in thetas:
			unitvec = self.rotatevec(self.orbit_axis, self.periapsis_unit, i)
			r = (self.a * (1 - self.e*self.e)) / (1 + self.e * math.cos(i))
			pos = unitvec * r
			# Add body position to parent position, if exists
			if self.parent is not None:
				if self.parent.orbit is not None:
					pos += self.parent.orbit.position
			self.smoothPath.append(pos)