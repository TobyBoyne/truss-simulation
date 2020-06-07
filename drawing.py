

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

	def change_joint_type(self, joint):
		joint.change_joint_type()
		joint.draw(self.ax)

	# MEMBERS
	def new_member(self, j1, j2):
		new_member = j1.add_member(j2)
		new_member.draw(self.ax)

	# FORCES
	def new_point_force(self, force_joint, F):
		new_force = force_joint.add_force(F)
		new_force.draw(self.ax)

	# PLOTTING
	def get_picked_artist(self, artist):
		for part in self.joints + self.all_members + self.all_joint_forces:
			if artist is part.line:
				return part


	def update(self):
		self.fig.canvas.draw()
