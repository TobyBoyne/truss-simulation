import matplotlib.pyplot as plt

from ui import EventHandler
import examples

if __name__ == "__main__":
	handler = EventHandler(examples.square_and_triangle)
	handler.simulate_structure()
	# saving only image of structure
	bbox = handler.drawing_structure.structure_bbox()
	handler.fig.savefig("images/square_and_triangle", bbox_inches=bbox)

	plt.show()