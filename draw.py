import matplotlib.pyplot as plt
import numpy as np

from parts import Joint

class JointHandler:
	def __init__(self, ax):
		self.ax = ax
		self.joints = []

	def __call__(self, event):
		"""On click event is handled by the JointHandler class"""
		pos = np.array([event.xdata, event.ydata])
		plt.plot(*pos, 'o')
		self.joints.append(Joint(pos))
		fig.canvas.draw()


def get_draw_ui():
	"""Creates figure and axes for drawing
	Connects click event to onclick function"""
	fig, ax = plt.subplots()
	handler = JointHandler(ax)
	fig.canvas.mpl_connect('button_press_event', handler)
	ax.autoscale(False)
	return fig, ax, handler



if __name__ == '__main__':
	fig, ax, handler = get_draw_ui()
	plt.show()