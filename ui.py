import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton, MouseEvent, KeyEvent, PickEvent
from matplotlib.widgets import RadioButtons
import numpy as np
from typing import Tuple
from enum import Enum

from parts import Joint, Member
from drawing import DrawingStructure

class Modes(Enum):
	DRAW = 0
	FORCE = 1
	DELETE = 2


class EventHandler:
	"""Handles all events from user input
	Contains calls for drawing"""
	def __init__(self):
		self.fig, self.ax, rax = get_draw_ui(self)

		# self.structure = Structure()
		self.drawing_structure = DrawingStructure(self.fig, self.ax)

		self.origin_joint = None
		self.force_joint = None
		self.new_line, = self.ax.plot([], [], lw=3, visible=False, ls='--', color='blue')
		self.new_force, = self.ax.plot([], [], lw=3, visible=False, ls='--', color='black')

		self.mode_buttons = RadioButtons(rax, [name for name in Modes.__members__])


	@property
	def mode(self):
		mode = Modes[self.mode_buttons.value_selected]
		return mode

	def on_click(self, event: MouseEvent):
		"""On click event is handled by the JointHandler class
		If an existing joint is right-clicked on, change the joint type
		If it is double-clicked, remove the joint
		If the user click-and-drags from an existing joint, draw a new member
		Otherwise, add a new joint"""
		# if the click is not in the drawing axes, ignore the event
		if event.inaxes is not self.ax:
			return
		pos = np.array([event.xdata, event.ydata])
		joint = self.drawing_structure.get_nearest_joint(pos)

		# DRAW
		if self.mode == Modes.DRAW:
			if joint is not None:
				if event.button == MouseButton.LEFT:
					# set the new member to be visible
					self.origin_joint = joint
					self.new_line.set_data(*zip(joint.pos, pos))
					self.new_line.set_visible(True)

				elif event.button == MouseButton.RIGHT:
					# change the type of support
					self.drawing_structure.change_joint_type(joint)

			# else triggers if click coord is not close to existing point
			else:
				if event.button == MouseButton.LEFT:
					# create new joint
					self.drawing_structure.new_joint(pos)

		# FORCE
		elif self.mode == Modes.FORCE:
			if joint is not None:
				if event.button == MouseButton.LEFT:
					# start drawing the force
					self.force_joint = joint
					self.new_force.set_data(*zip(joint.pos, pos))
					self.new_force.set_visible(True)


		self.drawing_structure.update()

	def on_pick(self, event: PickEvent):
		"""Triggers when an artist is clicked on
		Used to delete members/joints"""
		if self.mode == Modes.DELETE:
			artist = event.artist
			part = self.drawing_structure.get_picked_artist(artist)
			part.delete()

	def on_release(self, event: MouseEvent):
		"""If the mouse is being held down to draw a new member, create a member between the origin
		and the nearest joint, if one is near"""
		pos = np.array([event.xdata, event.ydata])
		# draw new member
		if self.origin_joint is not None:
			joint = self.drawing_structure.get_nearest_joint(pos)
			if joint is not None and joint is not self.origin_joint:
				self.drawing_structure.new_member(joint, self.origin_joint)

			self.new_line.set_visible(False)
			self.origin_joint = None

		# draw new force
		if self.force_joint is not None:
			F = self.force_joint.pos - pos
			# minimum force length
			if np.linalg.norm(F) > 0.05:
				self.drawing_structure.new_point_force(self.force_joint, F)

			self.new_force.set_visible(False)
			self.force_joint = None


		self.drawing_structure.update()

	def on_move(self, event: MouseEvent):
		"""If a line is being drawn, update the member to end at the current mouse position"""
		if (self.origin_joint is not None and self.mode == Modes.DRAW) or \
			(self.force_joint is not None and self.mode == Modes.FORCE):
			pos = np.array([event.xdata, event.ydata])
			if self.mode == Modes.DRAW:
				self.new_line.set_data(*zip(self.origin_joint.pos, pos))
			elif self.mode == Modes.FORCE:
				self.new_force.set_data(*zip(self.force_joint.pos, pos))

			self.drawing_structure.update()


	def on_key_down(self, event: KeyEvent):
		"""If the space key is pressed, start simulating structure"""
		if event.key == ' ':
			if not self.drawing_structure.is_determinate:
				raise NotImplementedError('The simulation only works for statically determinate structures.')
			self.drawing_structure.simulate()



def get_draw_ui(handler: EventHandler) -> Tuple[plt.Figure, plt.Axes, plt.Axes]:
	"""Creates figure and axes for drawing
	Also creates rax for radio buttons
	Connects click event to onclick function"""
	fig, (ax, rax) = plt.subplots(2, 1)

	fig.canvas.mpl_connect('button_press_event', handler.on_click)
	fig.canvas.mpl_connect('pick_event', handler.on_pick)
	fig.canvas.mpl_connect('button_release_event', handler.on_release)
	fig.canvas.mpl_connect('motion_notify_event', handler.on_move)
	fig.canvas.mpl_connect('key_press_event', handler.on_key_down)

	ax.autoscale(False)
	return fig, ax, rax



if __name__ == '__main__':
	handler = EventHandler()
	plt.show()