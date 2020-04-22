import matplotlib.pyplot as plt
import numpy as np
from typing import List, Union

from parts import Joint, Member

class Structure:
	"""Structure class stores all joints/members; handles calculation logic
	Does NOT handle drawing logic"""
	def __init__(self):
		self.joints: List[Joint] = []

	def get_nearest_joint(self, pos) -> Union[Joint, None]:
		"""Return the joint at position of click
		If no joint is there, then return None"""
		for joint in self.joints:
			if joint.is_near(pos, radius=0.02):
				return joint
		return None

	def add_joint(self, pos) -> Joint:
		new_joint = Joint(pos)
		self.joints.append(new_joint)
		return new_joint

	def delete_joint(self, joint):
		self.joints.remove(joint)
		joint.delete()

	@property
	def is_determinate(self):
		"""Returns True if the structure is statically determinate
		This is not always accurate - a structure that consists of a mechanism and a statically indeterminate
		sub-structure may cause errors later in the code"""
		j = len(self.joints)
		m = sum(len(j.members) for j in self.joints) // 2
		r = sum(sum(j.support.restrictions) for j in self.joints)
		return 2 * j == m + r