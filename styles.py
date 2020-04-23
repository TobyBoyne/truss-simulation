"""
Stores styles for lines and markers
"""

import matplotlib.pyplot as plt
import matplotlib.path as mpath
import numpy as np

triangle = mpath.Path.unit_regular_polygon(3)
circle = mpath.Path.unit_circle()

SUPPORT_XY = mpath.Path(triangle.vertices - [0, 1], triangle.codes)


if __name__ == '__main__':

	plt.plot([0, 1], [0, 1], marker=SUPPORT_XY, markersize=15)
	plt.show()