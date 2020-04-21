import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import numpy as np

from parts import Joint

class JointHandler:
	def __init__(self, fig: plt.Figure, ax: plt.Axes):
		self.fig = fig
		self.ax = ax
		self.joints = []

		self.origin_joint = None
		self.new_line, = self.ax.plot([], [], lw=3, visible=False, ls='--')

	def on_click(self, event):
		"""On click event is handled by the JointHandler class
		If an existing joint is right-clicked on, change the joint type
		If it is double-clicked, remove the joint
		If the user click-and-drags from an existing joint, draw a new member
		Otherwise, add a new joint"""
		pos = np.array([event.xdata, event.ydata])
		for joint in self.joints:
			if joint.is_near(pos):
				if event.button == MouseButton.LEFT:
					if event.dblclick:
						# delete the joint
						joint.delete()
						self.joints.remove(joint)
					else:
						# set the new member to be visible
						self.origin_joint = joint
						self.new_line.set_data(*zip(joint.pos, pos))
						self.new_line.set_visible(True)

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
			pos = np.array([event.xdata, event.ydata])
			for joint in self.joints:
				if joint.is_near(pos):
					joint.add_member(self.origin_joint)
					xs, ys = zip(joint.pos, self.origin_joint.pos)
					plt.plot(xs, ys)

			self.new_line.set_visible(False)
			self.origin_joint = None
			self.fig.canvas.draw()

	def on_move(self, event):
		"""If a line is being drawn, update the member to end at the current mouse position"""
		if self.origin_joint is not None:
			pos = np.array([event.xdata, event.ydata])
			self.new_line.set_data(*zip(self.origin_joint.pos, pos))
			self.fig.canvas.draw()



def get_draw_ui():
	"""Creates figure and axes for drawing
	Connects click event to onclick function"""
	fig, ax = plt.subplots()
	handler = JointHandler(fig, ax)
	fig.canvas.mpl_connect('button_press_event', handler.on_click)
	fig.canvas.mpl_connect('button_release_event', handler.on_release)
	fig.canvas.mpl_connect('motion_notify_event', handler.on_move)
	ax.autoscale(False)
	return fig, ax, handler



if __name__ == '__main__':
	fig, ax, handler = get_draw_ui()
	plt.show()