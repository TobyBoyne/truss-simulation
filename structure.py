import matplotlib.pyplot as plt
import numpy as np

from parts import Joint, Member

class Structure:
	"""Structure class stores all joints/members, and handles calculation logic"""
	def __init__(self):
		self.joints = []
		self.all_members = []

	def get_nearest_joint(self, pos):
		"""Return the joint at position of click
		If no joint is there, then return None"""
		for joint in self.joints:
			if joint.isnear(pos, radius=0.02):
				return joint
		return None

