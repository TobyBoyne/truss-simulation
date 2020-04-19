import matplotlib.pyplot as plt
import numpy as np

from parts import Joint

class JointHandler:
	def __init__(self, ax):
		self.ax = ax
		


def get_draw_ui():
	"""Creates figure and axes for drawing
	Connects click event to onclick function"""
	fig, ax = plt.subplots()
	joints = JointHandler(ax)
	fig.canvas.mpl_connect('button_press_event', joints)
	ax.autoscale(False)
	return fig, ax, joints


def on_click(event):
	print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
		  (event.button, event.x, event.y, event.xdata, event.ydata))

	plt.plot(event.xdata, event.ydata, 'o')

	fig.canvas.draw()


if __name__ == '__main__':
	fig, ax, joints = get_draw_ui()
	plt.show()