import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import numpy as np

from parts import Joint

class JointHandler:
	def __init__(self, fig, ax):
		self.fig = fig
		self.ax = ax
		self.joints = []
		self.mouse_down = False

	def on_click(self, event):
		"""On click event is handled by the JointHandler class
		If an existing joint is right-clicked on, change the joint type
		If the user click-and-drags from an existing joint, draw a new member
		Otherwise, add a new joint"""
		pos = np.array([event.xdata, event.ydata])
		for joint in self.joints:
			if joint.is_near(pos):
				if event.button == MouseButton.LEFT:
					self.mouse_down = True
				elif event.button == MouseButton.RIGHT:
					joint.change_joint_type()
				break
		# else triggers if no break - click coord is not close to existing point
		else:
			if event.button == MouseButton.LEFT:
				new_joint = Joint(pos)
				self.joints.append(new_joint)
				new_joint.draw(self.ax)
				self.fig.canvas.draw()


def get_draw_ui():
	"""Creates figure and axes for drawing
	Connects click event to onclick function"""
	fig, ax = plt.subplots()
	handler = JointHandler(fig, ax)
	fig.canvas.mpl_connect('button_press_event', handler.on_click)
	ax.autoscale(False)
	return fig, ax, handler



if __name__ == '__main__':
	fig, ax, handler = get_draw_ui()
	plt.show()