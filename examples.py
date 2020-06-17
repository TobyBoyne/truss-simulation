import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations

from drawing import DrawingStructure

def triangle(fig, ax):
	structure = DrawingStructure(fig, ax)
	joints = np.array([
		[0.2, 0.2],
		[0.8, 0.2],
		[0.8, 0.6]
	])

	supports = (2, 3, 0)

	for pos, s in zip(joints, supports):
		joint = structure.new_joint(pos)
		structure.change_joint_type(joint, s)

	for j1, j2 in combinations(structure.joints, 2):
		structure.new_member(j1, j2)

	structure.new_point_force(structure.joints[-1], np.array([0.5, 0]))

	return structure

def square_and_triangle(fig, ax):
	structure = DrawingStructure(fig, ax)
	joints = np.array([
		[0.2, 0.2],
		[0.5, 0.2],
		[0.8, 0.2],
		[0.5, 0.6],
		[0.2, 0.6]
	])

	supports = (3, 0, 2, 0, 0)

	connections = [
		(0, 1),
		(0, 4),
		(1, 2),
		(1, 3),
		(1, 4),
		(2, 3),
		(3, 4)
	]

	for pos, s in zip(joints, supports):
		joint = structure.new_joint(pos)
		structure.change_joint_type(joint, s)

	for i1, i2 in connections:
		j1, j2 = structure.joints[i1], structure.joints[i2]
		structure.new_member(j1, j2)

	structure.new_point_force(structure.joints[3], np.array([-0.2, -0.2]))

	return structure

if __name__ == "__main__":
	fig, ax = plt.subplots()
	structure = square_and_triangle(fig, ax)
	ax.set_xlim(0, 1)
	ax.set_ylim(0, 1)
	plt.show()
