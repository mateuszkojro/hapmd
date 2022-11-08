# import numpy and matplotlib library
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import pandas as pd
import numpy as np
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Azimuth plot at elevation 0°"
    )
    parser.add_argument(
        "path",
        help="path to .csv file, containing the data for plot in correct format",
        type=str,
    )
    parser.add_argument(
        "--scale_plot",
        "-s",
        dest="scale",
        help="if true, radius axis will be stretched between lowest and highest measured value",
        type=bool,
        default=False,
    )

    args = parser.parse_args()
    data_file_path = args.path

    # load separator symbol
    with open(data_file_path) as f:
        separator = f.read(1)

    measurement: pd.DataFrame = pd.read_csv(data_file_path, sep=separator)
    measurement = measurement.set_index(measurement.columns[0])

    plt.axes(
        projection="polar",
    )

    fig = plt.figure()
    ax = fig.add_subplot(projection="polar")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)

    color = iter(cm.rainbow(np.linspace(0, 1, len(measurement.columns))))

    if len(measurement.columns) == 1:
        alpha = 1
    else:
        alpha = 0.6

    if not args.scale:
        ax.scatter(0, 0, alpha=0)
        ax.scatter(0, -100, alpha=0)

    measurement_index_as_radians = [math.radians(freq) for freq in measurement.index]

    for idx, freq in enumerate(measurement.columns):
        current_color = next(color)
        ax.scatter(
            measurement_index_as_radians,
            measurement.iloc[:, idx].values,
            color=current_color,
            s=0.5,
            alpha=alpha,
            label=f"{'{:.3e}'.format(float(freq))}Hz",
        )

    no_labels = len(ax.yaxis.get_ticklabels())
    for n, label in enumerate(ax.yaxis.get_ticklabels()):
        if n % (no_labels // 5) != 0:
            label.set_visible(False)

    ax.yaxis.get_ticklabels()[-1].set_visible(True)

    (lines, labels) = plt.thetagrids(
        range(0, 360, 45), ("0°", "45°", "90°", "135°", "180°", "-135°", "-90°", "-45°")
    )

    for label, angle in zip(labels, range(0, 360, 45)):
        label.set_rotation(90 - angle)

    # label_position=ax.get_rlabel_position()
    # ax.text(np.radians(label_position+10),ax.get_rmax()/2.,'Antenna signal Strength [dB]',
    #     rotation=label_position,ha='center',va='center')

    ax.set_title("Directivity (dB) at 0° elevation for different Frequencies")
    ax.legend(loc="lower right")
    # # display the Polar plot
    fig.savefig(data_file_path[:-4] + "_plot.pdf")
