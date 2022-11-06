# import numpy and matplotlib library
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.pyplot import cm

measurement = pd.read_csv("output.csv")
measurement = measurement.set_index(measurement.columns[0])


plt.axes(projection="polar",)
# plt.set_theta_zero_lsocation("N")
fig = plt.figure()
ax = fig.add_subplot(projection='polar')

color = iter(cm.rainbow(np.linspace(0, 1, len(measurement.columns))))

ax.set_theta_zero_location('N')
for idx, freq in enumerate(measurement.columns):
    current_color = next(color)
    for angle in measurement.index:
        if angle < 0:
            theta = 360 + angle
        else:
            theta = angle
        theta = math.radians(theta)
        ax.scatter(theta, measurement.at[angle,freq], color = current_color, s=0.5,  alpha = 0.4)


no_labels = len(ax.yaxis.get_ticklabels())
for n, label in enumerate(ax.yaxis.get_ticklabels()):
    if n % (no_labels//5) != 0:
        label.set_visible(False)        

ax.yaxis.get_ticklabels()[-1].set_visible(True)

# # display the Polar plot
fig.savefig("polat_plot.pdf")
