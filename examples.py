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

	return structure

if __name__ == "__main__":
	fig, ax = plt.subplots()
	structure = triangle(fig, ax)
	ax.set_xlim(0, 1)
	ax.set_ylim(0, 1)
	plt.show()
