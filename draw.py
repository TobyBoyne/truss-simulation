import matplotlib.pyplot as plt
import numpy as np

def onclick(event):
	print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
		  (event.button, event.x, event.y, event.xdata, event.ydata))

	plt.plot(event.xdata, event.ydata, 'x')

	fig.canvas.draw()


if __name__ == '__main__':
	fig, ax = plt.subplots()
	ax.autoscale(False)