import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
from reader import days_back
from reader import readData

import matplotlib.gridspec as gridspec
import datetime

# configure plotlib
matplotlib.style.use('default')
# matplotlib.style.use('tableau-colorblind10')
# matplotlib.style.use('seaborn-colorblind')
# matplotlib.style.use('seaborn')
# matplotlib.rcParams.update({'font.size': 30})
rc = {'axes.labelsize': 12, 'font.size': 12, 'legend.fontsize': 12.0, 'axes.titlesize': 12, 'grid.linewidth': 0.5,
      'grid.linestyle': ':', 'lines.linewidth': 2.0}
plt.rcParams.update(**rc)


b_legend: bool = True


def plot_figures(figures, nrows=1, ncols=1):
    """Plot a dictionary of figures.

    Parameters
    ----------
    figures : <title, figure> dictionary
    ncols : number of columns of subplots wanted in the display
    nrows : number of rows of subplots wanted in the figure
    """

    fig, axeslist = plt.subplots(ncols=ncols, nrows=nrows)
    for ind, title in enumerate(figures):
        axeslist.ravel()[ind].imshow(figures[title], cmap=plt.gray())
        axeslist.ravel()[ind].set_title(title)
        axeslist.ravel()[ind].set_axis_off()
    plt.tight_layout()  # optional

def plot_multi(ax, input_data, x_label, y_label, b_logarithmic=False):
    global b_legend
    for country, data in input_data.items():
        if b_logarithmic:
            ax.semilogy(range(-days_back, 0), data, 'x-', label=country)
        else:
            ax.plot(range(-days_back, 0), data, 'x-', label=country)
    if (b_legend):
        ax.legend()
        b_legend = False
    ax.set_xlabel(xlabel=x_label)
    ax.set_ylabel(ylabel=y_label)
    ax.grid()

import datetime

def arrangeplots(datatoplot, ncols):
    numberofplots: int = datatoplot.__len__() + 2  # 2 for additional growth factor and days to double
    nrows: int = math.ceil(numberofplots / ncols)
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows.__int__(), figsize=(15, 10), squeeze=True, sharex= True)
    fig.suptitle("Corona Dashboard "+datetime.datetime.now().strftime("%Y-%m-%d"))
    i_col: int = 0
    i_row: int = 0
    for title, data in datatoplot.items():
        plot_multi(axes[i_row, i_col], data, 'days before today', title, True)
        if i_col >= ncols - 1:
            i_row = i_row + 1
            i_col = 0
        else:
            i_col = i_col + 1

    # growth factor
    for country, data in deaths.items():
        axes[i_row, i_col].plot(range(-days_back + 1, 0), data[1:] / data[:-1], label=country)
    # axes[iRow,iCol].legend()
    axes[i_row, i_col].set_xlabel('days before today')
    axes[i_row, i_col].set_ylabel('growth factor deaths/d')
    axes[i_row, i_col].set_ylim((0.9, 2.8))
    axes[i_row, i_col].grid()

    if i_col >= ncols - 1:
        i_row = i_row + 1
        i_col = 0
    else:
        i_col = i_col + 1

    # days to double deaths
    for country, data in deaths.items():
        axes[i_row, i_col].plot(range(-days_back + 2, 0), np.log(2) / np.log(np.sqrt(data[2:] / data[:-2])),
                                label=country)
    axes[i_row, i_col].set_xlabel('days before today')
    axes[i_row, i_col].set_ylabel('d to double deaths')
    axes[i_row, i_col].set_ylim((0., 10.))
    axes[i_row, i_col].grid()

if __name__ == "__main__":
    deaths, deathsPerMillion, conf, confPerMillion, recovered, recoveredPerMillion = readData()
    datatoplot = {'deaths': deaths, 'deaths/mn': deathsPerMillion, 'confirmed': conf,
                  'confirmed/mn': confPerMillion}
    arrangeplots(datatoplot, ncols=3);

    plt.show()
