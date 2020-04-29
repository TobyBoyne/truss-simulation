import matplotlib.pyplot as plt
import numpy as np
from typing import List, Union

from parts import Joint, Member, Force, SUPPORT_TYPES

class Structure:
	"""Structure class stores all joints/members; handles calculation logic
	Does NOT handle drawing logic"""
	def __init__(self):
		self.joints: List[Joint] = []

	@property
	def all_members(self) -> List[Member]:
		"""Returns a list of all members in the structure"""
		members = []
		for joint in self.joints:
			for member in joint.members:
				if member not in members:
					members.append(member)
		return members

	@property
	def all_forces(self) -> List[Force]:
		"""Returns a list of all forces acting on the structure"""
		forces = []
		for joint in self.joints:
			for force in joint.forces:
				forces.append(force)
		return forces

	@property
	def supports(self) -> List[Joint]:
		"""Returns all the joints that are supports in the structure"""
		return [j for j in self.joints if j.support_type != 0]


	def get_nearest_joint(self, pos) -> Union[Joint, None]:
		"""Return the joint at position of click
		If no joint is there, then return None"""
		for joint in self.joints:
			if joint.is_near(pos, radius=0.04):
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


	def simulate(self):
		reaction = self.reaction_forces()

	def reaction_forces(self):
		"""Calculate the reaction forces at the supports by considering horizontal, vertical
		and moment equilibria"""
		# TODO: make function more general
		#  	include moment applied at support in case of cantilever
		supports = self.supports

		# calculate total forces
		force_arr = np.array([force.F for force in self.all_forces])
		print(force_arr)

		rolling_support, static_support = sorted(supports, key=lambda s: sum(s.support.restrictions))


	def internal_forces(self):
		pass
