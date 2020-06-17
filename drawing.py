

from structure import Structure

class DrawingStructure(Structure):
	def __init__(self, fig, ax):
		super().__init__()
		self.fig = fig
		self.ax = ax

	# JOINTS
	def new_joint(self, pos):
		new_joint = self.add_joint(pos)
		new_joint.draw(self.ax)
		return new_joint

	def change_joint_type(self, joint, n=1):
		joint.change_joint_type(n)
		joint.draw(self.ax)

	# MEMBERS
	def new_member(self, j1, j2):
		new_member = j1.add_member(j2)
		new_member.draw(self.ax)
		return new_member

	# FORCES
	def new_point_force(self, force_joint, F):
		new_force = force_joint.add_force(F)
		new_force.draw(self.ax)
		return new_force

	# PLOTTING
	def get_picked_artist(self, artist):
		for part in self.joints + self.all_members + self.all_joint_forces:
			if artist is part.line:
				return part

	def structure_bbox(self):
		"""Return the bounding box for the Axis object that the structure is plotted on"""
		bbox = self.ax.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
		return bbox

	def update(self):
		self.fig.canvas.draw()
