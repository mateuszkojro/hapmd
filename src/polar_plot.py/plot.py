# import numpy and matplotlib library
import numpy as np
import matplotlib.pyplot as plt


plt.axes(projection="polar")


rads = np.arange(0, (2 * np.pi), 0.01)
rs = np.arange(0, (2 * np.pi), 0.01)


# plotting the circle
for i, r in zip(rads, rs):
    plt.polar(i, r, "g.")

# display the Polar plot
plt.savefig("polat_plot.pdf")
