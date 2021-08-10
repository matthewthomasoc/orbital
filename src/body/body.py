import numpy as np
import math
import traceback
from src.orbit.orbit import *
from src.rotation.rotation import *
import matplotlib.pyplot as plt

class body:
	def __init__(self, radius, a, e, orbit_period, inclination, apsidal_prec_period, axial_prec_period, axial_period, obliquity, parent = None):
		self.radius = radius
		try:
			self.orbit = orbit(a, e, orbit_period, inclination, apsidal_prec_period, parent)
		except:
			traceback.print_exc()
			self.orbit = None
		try:
			self.rotation = rotation(axial_prec_period, axial_period, obliquity)
		except:
			traceback.print_exc()
			self.rotation = None

		# pyplot 
		self.A = None # planet body
		self.B = None # planet axis rotation
		self.C = None # planet current orientation

		# sphere construction angles
		self.u, self.v = np.mgrid[0:2*np.pi:50j, 0:np.pi:50j]

	def update(self, dt, ax = None):
		# update orbit and rotation
		if self.orbit is not None:
			self.orbit.update(dt)
		if self.rotation is not None:
			self.rotation.update(dt)

		# plot
		if ax is not None:
			self.plotBodies(ax)

	def plotBodies(self, ax):
		# save current position of body, if orbit object created
		if self.orbit is not None:
			pos = self.orbit.position
		else:
			pos = [0,0,0]

		''' create body on plot '''
		# delete previous sphere
		if self.A is not None:
			self.A.remove()

		# create sphere for body
		try:
			x = np.cos(self.u)*np.sin(self.v)*self.radius + pos[0]
			y = np.sin(self.u)*np.sin(self.v)*self.radius + pos[1]
			z = np.cos(self.v)*self.radius + pos[2]
			# plot sphere
			self.A = body_surface = ax.plot_surface(x, y, z, color="g")
		except:
			traceback.print_exc()

		''' create direction arrows '''
		try:
			''' create axis of rotation arrow '''
			# delete previous arrow
			if self.B is not None:
				self.B.remove()
			# draw rotation axis arrow on body
			self.B = ax.quiver(pos[0],pos[1],pos[2],self.rotation.axial_rot_axis[0]*self.radius*2,self.rotation.axial_rot_axis[1]*self.radius*2,self.rotation.axial_rot_axis[2]*self.radius*2, color="red")

			''' create orientation arrow '''
			# delete previous arrow
			if self.C is not None:
				self.C.remove()
			# draw orientation arrow on body
			self.C = ax.quiver(pos[0],pos[1],pos[2],self.rotation.orientation[0]*self.radius*2,self.rotation.orientation[1]*self.radius*2,self.rotation.orientation[2]*self.radius*2, color="magenta")
		except:
			traceback.print_exc()

		''' create line showing path '''
		if self.orbit is not None:
			x, y, z = zip(*self.orbit.smoothPath)
			ax.plot3D(x,y,z, 'blue', alpha=0.25)