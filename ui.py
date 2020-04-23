import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton, MouseEvent, KeyEvent
from matplotlib.widgets import RadioButtons
import numpy as np
from itertools import chain

from parts import Joint, Member
from structure import Structure

class EventHandler:
	"""Handles all events from user input
	Contains calls for drawing"""
	def __init__(self, fig: plt.Figure, ax: plt.Axes):
		self.fig = fig
		self.ax = ax
		self.structure = Structure()

		self.origin_joint = None
		self.new_line, = self.ax.plot([], [], lw=3, visible=False, ls='--')

		self.mode_buttons = RadioButtons(ax, ('Draw', 'Force', 'Delete'))
		self.mode_buttons.on_clicked(self.choose_mode)
		self.mode = 'Draw'


	def choose_mode(self, label):
		self.mode = label

	def on_click(self, event: MouseEvent):
		"""On click event is handled by the JointHandler class
		If an existing joint is right-clicked on, change the joint type
		If it is double-clicked, remove the joint
		If the user click-and-drags from an existing joint, draw a new member
		Otherwise, add a new joint"""
		pos = np.array([event.xdata, event.ydata])
		joint = self.structure.get_nearest_joint(pos)
		if joint is not None:
			if event.button == MouseButton.LEFT:
				if event.dblclick:
					# delete the joint
					self.structure.delete_joint(joint)
				else:
					# set the new member to be visible
					self.origin_joint = joint
					self.new_line.set_data(*zip(joint.pos, pos))
					self.new_line.set_visible(True)

			elif event.button == MouseButton.RIGHT:
				# change the type of support
				joint.change_joint_type()
				joint.draw(self.ax)

		# else triggers if click coord is not close to existing point
		else:
			if event.button == MouseButton.LEFT:
				# create new joint
				new_joint = self.structure.add_joint(pos)
				new_joint.draw(self.ax)
		self.fig.canvas.draw()

	def on_release(self, event: MouseEvent):
		"""If the mouse is being held down to draw a new member, create a member between the origin
		and the nearest joint, if one is near"""
		if self.origin_joint is not None:
			pos = np.array([event.xdata, event.ydata])
			joint = self.structure.get_nearest_joint(pos)
			if joint is not None and joint is not self.origin_joint:
				new_member = joint.add_member(self.origin_joint)
				new_member.draw(self.ax)

			self.new_line.set_visible(False)
			self.origin_joint = None
			self.fig.canvas.draw()

	def on_move(self, event: MouseEvent):
		"""If a line is being drawn, update the member to end at the current mouse position"""
		if self.origin_joint is not None:
			pos = np.array([event.xdata, event.ydata])
			self.new_line.set_data(*zip(self.origin_joint.pos, pos))
			self.fig.canvas.draw()


	def on_key_down(self, event: KeyEvent):
		"""If the space key is pressed, start simulating structure"""
		if event.key == ' ':
			if not self.structure.is_determinate:
				raise NotImplementedError('The simulation only works for statically determinate structures.')
			self.structure.simulate()



def get_draw_ui():
	"""Creates figure and axes for drawing
	Connects click event to onclick function"""
	fig, ax = plt.subplots()
	handler = EventHandler(fig, ax)

	fig.canvas.mpl_connect('button_press_event', handler.on_click)
	fig.canvas.mpl_connect('button_release_event', handler.on_release)
	fig.canvas.mpl_connect('motion_notify_event', handler.on_move)
	fig.canvas.mpl_connect('key_press_event', handler.on_key_down)

	ax.autoscale(False)
	return fig, ax, handler



if __name__ == '__main__':
	fig, ax, handler = get_draw_ui()
	plt.show()