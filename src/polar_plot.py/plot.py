# import numpy and matplotlib library
import math
import matplotlib.pyplot as plt
import pandas as pd

measurement = pd.read_csv("output.csv")
measurement = measurement.set_index(measurement.columns[0])


plt.axes(projection="polar",)
# plt.set_theta_zero_lsocation("N")
fig = plt.figure()
ax = fig.add_subplot(projection='polar')

ax.set_theta_zero_location('N')
for angle in measurement.index:
    for freq in measurement.columns:
        if angle < 0:
            theta = 360 + angle
        else:
            theta = angle
        theta = math.radians(theta)
        ax.scatter(theta, freq, c = ((measurement.at[angle,freq] + 1) / 2), s=0.5, cmap='plasma', alpha = 0.2)


no_labels = len(ax.yaxis.get_ticklabels())
for n, label in enumerate(ax.yaxis.get_ticklabels()):
    if n % (no_labels//5) != 0:
        label.set_visible(False)
        

ax.yaxis.get_ticklabels()[-1].set_visible(True)

# # display the Polar plot
fig.savefig("polat_plot.pdf")
