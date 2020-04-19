import matplotlib.pyplot as plt
import numpy as np

class Joint:
	def __init__(self, pos: np.ndarray, support=False):
		self.pos = pos

	def draw(self, ax: plt.Axes):
		ax.plot(*self.pos, 'o')