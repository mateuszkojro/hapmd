import numpy as np
import matplotlib.pyplot as plt


r = np.arange(0, 2, 0.01)
array_x = [x % 100 for x in range (360)] 
array_y = [x for x in range (360)]

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
ax.plot(array_x, array_y)
ax.set_rmax(2)
ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line
ax.grid(True)

ax.set_title("A line plot on a polar axis", va='bottom')
plt.savefig(ax.get_title() + '.pdf')