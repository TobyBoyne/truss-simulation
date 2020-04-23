"""
Stores styles for lines and markers
https://matplotlib.org/3.1.1/gallery/shapes_and_collections/marker_path.html
"""


# TODO: save only the path as a numpy array so that a patch can be generated by adding pos the vertices
# markers/mpath shouldn't be used


import matplotlib.pyplot as plt
import matplotlib.path as mpath
from matplotlib import patches
import numpy as np

rot_array = np.array([[0, -1], [1, 0]])

triangle = mpath.Path.unit_regular_polygon(3)
triangle_v = triangle.vertices - [0, 1]
rot_triangle_v = np.dot(triangle.vertices, rot_array) - [1, 0]
circle = mpath.Path.unit_circle()
circle_v = circle.vertices * 0.4

y_rollers = np.concatenate([circle_v + [0.5, -2], circle_v + [-0.5, -2]])
x_rollers = np.concatenate([circle_v + [-2, 0.5], circle_v + [-2, -0.5]])

SUPPORT_XY = mpath.Path(triangle_v, triangle.codes)
SUPPORT_Y =	mpath.Path(np.concatenate([triangle_v, y_rollers]),
						  np.concatenate([triangle.codes, circle.codes, circle.codes]))
SUPPORT_X = mpath.Path(np.concatenate([rot_triangle_v, x_rollers]),
						  np.concatenate([triangle.codes, circle.codes, circle.codes]))

if __name__ == '__main__':
	fig, ax = plt.subplots()
	for y, marker_style in enumerate((SUPPORT_XY, SUPPORT_X, SUPPORT_Y)):
		plt.plot([y, y], marker=marker_style, markersize=30)

	p = patches.PathPatch(SUPPORT_XY)
	ax.add_patch(p)
	plt.show()