# import numpy and matplotlib library
from email import message
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

measurement = pd.read_csv("output.csv")
measurement = measurement.set_index(measurement.columns[0])

max_val = measurement.max()
max_val = measurement.min()

plt.axes(projection="polar")
# plt.set_theta_zero_lsocation("N")

for angle in measurement.index:
    for freq in measurement.columns:
        print(angle, freq, measurement.at[angle,freq])
        plt.scatter(angle, freq, c = (measurement.at[angle,freq] + 1) / 2, s=0.2, cmap='hsv')

# # display the Polar plot
plt.savefig("polat_plot.pdf")
