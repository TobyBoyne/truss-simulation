import matplotlib.pyplot as plt
import numpy as np

# support types show the (X, Y, rot) restrictions
SUPPORT_TYPES = {
	0: (False, False, False),	# pin-joint
	1: (True, False, False),	# X-restricted roller support
	2: (False, True, False),	# Y-restricted roller support
	3: (True, True, False),		# stationary pin-joint support
	4: (True, True, True)		# cantilever support
}

class Joint:
	"""Class to contain a joint or support
	Handles all members as connections between joints"""
	def __init__(self, pos: np.ndarray, support=0):
		self.pos = pos
		self.connections = []
		self.support_type = support

	def add_member(self, other: 'Joint'):
		self.connections.append(other)

	def draw(self, ax: plt.Axes):
		ax.plot(*self.pos,'o', color="red")

	def is_near(self, other_pos, radius=10):
		return np.linalg.norm(self.pos - other_pos) < radius

	def change_joint_type(self):
		self.support_type = (self.support_type + 1) % len(SUPPORT_TYPES)