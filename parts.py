import matplotlib.pyplot as plt
import numpy as np

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
		ax.plot(*self.pos, 'o')

	def is_near(self, other_pos, radius=10):
		return np.linalg.norm(self.pos - other_pos) < radius

	def change_joint_type(self):
		self.support_type += 1