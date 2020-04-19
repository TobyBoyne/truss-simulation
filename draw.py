import matplotlib.pyplot as plt
import numpy as np

def get_draw_ui():
	"""Creates figure and axes for drawing
	Connects click event to onclick function"""
	fig, ax = plt.subplots()
	fig.canvas.mpl_connect('button_press_event', on_click)
	ax.autoscale(False)
	return fig, ax


def on_click(event):
	print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
		  (event.button, event.x, event.y, event.xdata, event.ydata))

	plt.plot(event.xdata, event.ydata, 'x')

	fig.canvas.draw()


if __name__ == '__main__':
	fig, ax = get_draw_ui()
