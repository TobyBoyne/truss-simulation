import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import numpy as np

from parts import Joint

class JointHandler:
	def __init__(self, fig, ax):
		self.fig = fig
		self.ax = ax
		self.joints = []
		self.origin_joint = None

	def on_click(self, event):
		"""On click event is handled by the JointHandler class
		If an existing joint is right-clicked on, change the joint type
		If the user click-and-drags from an existing joint, draw a new member
		Otherwise, add a new joint"""
		pos = np.array([event.xdata, event.ydata])
		for joint in self.joints:
			if joint.is_near(pos):
				if event.button == MouseButton.LEFT:
					self.origin_joint = joint
				elif event.button == MouseButton.RIGHT:
					joint.change_joint_type()
					joint.draw(self.ax)
				break
		# else triggers if no break - click coord is not close to existing point
		else:
			if event.button == MouseButton.LEFT:
				new_joint = Joint(pos)
				self.joints.append(new_joint)
				new_joint.draw(self.ax)
		self.fig.canvas.draw()

	def on_release(self, event):
		"""If the mouse is being held down to draw a new member, create a member between the origin
		and the nearest joint, if one is near"""
		if self.origin_joint is not None:
			print("!")
			pos = np.array([event.xdata, event.ydata])
			for joint in self.joints:
				if joint.is_near(pos):
					joint.add_member(self.origin_joint)
					xs, ys = zip(joint.pos, self.origin_joint.pos)
					plt.plot(xs, ys)

			self.origin_joint = None
			self.fig.canvas.draw()


def get_draw_ui():
	"""Creates figure and axes for drawing
	Connects click event to onclick function"""
	fig, ax = plt.subplots()
	handler = JointHandler(fig, ax)
	fig.canvas.mpl_connect('button_press_event', handler.on_click)
	fig.canvas.mpl_connect('button_release_event', handler.on_release)
	ax.autoscale(False)
	return fig, ax, handler



if __name__ == '__main__':
	fig, ax, handler = get_draw_ui()
	plt.show()