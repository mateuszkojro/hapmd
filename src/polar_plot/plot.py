# import numpy and matplotlib library
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import pandas as pd
import numpy as np
import sys

if __name__ == "__main__":

    data_file_path = None

    if len(sys.argv) == 2:
        data_file_path = str(sys.argv[1])
    else:
        raise ValueError(f"Provided file: '{data_file_path}' is incorrect")

    if data_file_path[-4:] != ".csv":
        raise ValueError(
            f"Provided file must have extension '.csv' not '{data_file_path[-4:]}'"
        )

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

    ax.scatter(
        0,
        0,
        alpha=0,
    )
    ax.scatter(
        0,
        -100,
        alpha=0,
    )

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


    ax.set_title("Horizontal Antenna Pattern measurement for Frequency")
    ax.legend(loc="lower right")
    # # display the Polar plot
    fig.savefig(data_file_path[:-4] + "_plot.pdf")
    