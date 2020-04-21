import matplotlib.pyplot as plt
import numpy as np

from parts import Joint, Member

class Structure:
	"""Structure class stores all joints/members; handles calculation logic
	Does NOT handle drawing logic"""
	def __init__(self):
		self.joints = []

	def get_nearest_joint(self, pos):
		"""Return the joint at position of click
		If no joint is there, then return None"""
		for joint in self.joints:
			if joint.is_near(pos, radius=0.02):
				return joint
		return None

	def add_joint(self, pos):
		new_joint = Joint(pos)
		self.joints.append(new_joint)
		return new_joint

	def delete_joint(self, joint):
		self.joints.remove(joint)
		joint.delete()