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
	def all_joint_forces(self) -> List[Force]:
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
		n_j = len(self.joints)
		m = len(self.all_members)
		r = sum(sum(j.support.restrictions) for j in self.joints)
		return 2 * n_j == m + r


	def simulate(self):
		members = self.all_members
		tensions = self.internal_forces()
		lengths = np.array([m.length() for m in members])
		extensions = tensions * lengths

		x_F = np.array([1., 0.])
		y_F = np.array([0., 1.])

		for joint in self.joints:
			x_restr, y_restr = joint.support.restrictions[:2]
			if not x_restr:
				force_virtual = Force(x_F, joint.pos)
				tensions_virtual = self.internal_forces()

	def reaction_forces(self, forces):
		"""Create simultaneous equations for the reactions of the structure to be solved in internal_forces"""
		# TODO: make function more general
		#  	include moment applied at support in case of cantilever
		#   exit early if no force is applied
		supports = self.supports

		# calculate total forces and moments
		force_arr = np.array([force.F for force in forces])
		resultant = np.sum(force_arr, axis=0)
		pivot = np.array([0, 0])
		total_moment = sum([force.moment(pivot) for force in forces])
		resultant = np.concatenate((resultant, [total_moment]))

		rolling_support, static_support = sorted(supports, key=lambda s: sum(s.support.restrictions))
		# x-restricted -> horizontal reaction -> horizontal distance
		i = 0 if rolling_support.support.restrictions[0] else 1

		dists = [rolling_support.pos[i], static_support.pos[0], static_support.pos[1]]

		A = np.array([[0, 0, 1],
					  [1, 1, 0],
					  dists])

		return A, resultant, rolling_support, static_support


	def internal_forces(self, force_set=None):
		"""Use method of joints to find tensions in all members"""
		members = self.all_members

		# if no force set is provided, use real forces
		if force_set is None:
			force_set = self.all_joint_forces

		reaction_eq, resultant, rolling, static = self.reaction_forces(force_set)

		# 2N equations - two (x, y) for each joint
		# 2N unknowns - 3 reaction forces, 2N-3 member forces
		N = len(self.joints) * 2
		equations = np.zeros((N, N))
		equations[:3, :3] = reaction_eq

		forces = np.zeros(N)

		for i, j in enumerate(self.joints):
			eq = np.zeros((2, N))
			for m in j.members:
				idx = members.index(m) + 3
				# direction vector from current join -> tension
				dir_vec = m.direction(j)
				eq[:, idx] = (dir_vec / np.linalg.norm(dir_vec))

			# add reaction force to eq
			# TODO: more general for different supports
			if j is rolling:
				# reaction vec accounts for horizontal or vertical
				reaction_vec = np.array(j.support.restrictions).astype(float)[:2]
				eq[:, 0] = reaction_vec
			elif j is static:
				reaction_vec = np.array([[0, 1], [1, 0]])
				eq[:, 1:3] = reaction_vec

			equations[i*2:i*2+2, :] = eq
			force = np.zeros(2)
			force += np.sum(np.array([force.F for force in j.forces]), axis=0)
			forces[i*2:i*2+2] = force

		solution = np.linalg.solve(equations, -forces)
		print(solution)
		tensions = solution[3:]
		return tensions

	def virtual_work(self, tensions):
		"""Calculate the displacement of a joint using the principle of virtual work
		F*d = T*e"""
		members = self.all_members
		lengths = np.array([m.length() for m in members])

		work = tensions * lengths
		return work




if __name__ == "__main__":
	a = np.array([[1, 2], [3, 4]])
	b = np.array([[5, 6]])
	print(np.sum(b, axis=0))