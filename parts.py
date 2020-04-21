import matplotlib.pyplot as plt
import numpy as np
from collections import namedtuple

# support types show the (X, Y, rot) restrictions
Support = namedtuple('Support', ('restrictions', 'color'))
SUPPORT_TYPES = (
	Support((False, False, False), 'red'),	# pin-joint
	Support((True, False, False), 'blue'),	# X-restricted roller support
	Support((False, True, False), 'green'),	# Y-restricted roller support
	Support((True, True, False), 'orange'),	# stationary pin-joint support
	Support((True, True, True), 'black')	# cantilever support
)

class Joint:
	"""Class to contain a joint or support"""
	def __init__(self, pos: np.ndarray, support=0):
		self.pos = pos
		self.members = []
		self.support_type = support
		self.line = None

	def add_member(self, other: 'Joint'):
		new_member = Member(self, other)
		self.members.append(new_member)
		other.members.append(new_member)
		return new_member

	def draw(self, ax: plt.Axes):
		"""Plots a marker on the axes. If there is already a marker for this joint, update it"""
		color = SUPPORT_TYPES[self.support_type].color
		if self.line is None:
			self.line, = ax.plot(*self.pos,'o', color=color, picker=True)
		else:
			self.line.set_color(color)

	def is_near(self, other_pos, radius=0.02):
		return np.linalg.norm(self.pos - other_pos) < radius

	def change_joint_type(self):
		self.support_type = (self.support_type + 1) % len(SUPPORT_TYPES)

	def delete(self):
		"""Removes the marker and all connected members"""
		self.line.remove()
		for m in self.members:
			m.delete(from_joint=self)


class Member:
	"""Stores information about a single member between two joints"""
	def __init__(self, joint1: Joint, joint2: Joint):
		self.j1 = joint1
		self.j2 = joint2
		self.line = None

	def draw(self, ax: plt.Axes):
		self.line, = ax.plot(*zip(self.j1.pos, self.j2.pos), color='blue')

	def delete(self, from_joint=None):
		"""Remove line from axes, then delete all references to self
		If from_joint is passed, that joint is to be deleted anyway and so references between
		the two no longer need to be deleted"""
		if self.line is not None:
			self.line.remove()
		for joint in (self.j1, self.j2):
			if joint is not from_joint:
				joint.members.remove(self)
