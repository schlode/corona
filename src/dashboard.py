import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
import datetime

# configure plotlib
# matplotlib.style.use('tableau-colorblind10')
matplotlib.style.use('default')
# matplotlib.style.use('seaborn-colorblind')
# matplotlib.style.use('seaborn')
# matplotlib.rcParams.update({'font.size': 30})
rc = {'axes.labelsize': 18, 'font.size': 20, 'legend.fontsize': 18.0, 'axes.titlesize': 20, 'grid.linewidth': 0.5,
      'grid.linestyle': ':', 'lines.linewidth': 2.0}
plt.rcParams.update(**rc)

confirmed = pd.read_csv(
    "../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
death = pd.read_csv("../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
recovered = pd.read_csv(
    "../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")

indizes = {'Mexico': 46, 'Germany': 11, 'Sweden': 17, 'Italy': 16, 'Austria': 32}  # , 'Hubei':154}
days_back = 50

# select plot data
countries = indizes
# countries = {'Germany': 11, 'Sweden': 17, 'Italy': 16, 'Austria': 32}
people = {'Germany': 82.79, 'Sweden': 10.12, 'Italy': 60.48, 'Austria': 8.822, 'China': 1386, 'USA': 327.2,
          'France': 66.99, 'Mexico': 129.2, 'Hubei': 57.2}
conf = {k: np.array(confirmed[confirmed['Country/Region'] == k].T[v].tolist()[-days_back:]) for k, v in
        countries.items()}
conf['USA'] = np.array(
    confirmed[confirmed['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist())
conf['China'] = np.array(
    confirmed[confirmed['Country/Region'].str.startswith('Chin')][0:53].sum(axis=0)[-days_back:].tolist())
conf['France'] = np.array(
    confirmed[confirmed['Country/Region'].str.startswith('France')][0:53].sum(axis=0)[-days_back:].tolist())

confPerMillion = {k: np.array(confirmed[confirmed['Country/Region'] == k].T[v].tolist()[-days_back:]) / people[k] for
                  k, v in countries.items()}
confPerMillion['USA'] = np.array(
    confirmed[confirmed['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist()) / people['USA']
confPerMillion['China'] = np.array(
    confirmed[confirmed['Country/Region'].str.startswith('Chin')][0:53].sum(axis=0)[-days_back:].tolist()) / people[
                              'China']
confPerMillion['France'] = np.array(
    confirmed[confirmed['Country/Region'].str.startswith('France')][0:53].sum(axis=0)[-days_back:].tolist()) / people[
                               'France']

deaths = {k: np.array(death[death['Country/Region'] == k].T[v].tolist()[-days_back:]) for k, v in countries.items()}
deaths['USA'] = np.array(death[death['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist())
deaths['China'] = np.array(
    death[death['Country/Region'].str.startswith('Chin')][0:53].sum(axis=0)[-days_back:].tolist())
deaths['France'] = np.array(
    death[death['Country/Region'].str.startswith('France')][0:53].sum(axis=0)[-days_back:].tolist())

deathsPerMillion = {k: np.array(death[death['Country/Region'] == k].T[v].tolist()[-days_back:]) / people[k] for
                    k, v in countries.items()}
deathsPerMillion['USA'] = np.array(
    confirmed[death['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist()) / people['USA']
deathsPerMillion['China'] = np.array(
    confirmed[death['Country/Region'].str.startswith('Chin')][0:53].sum(axis=0)[-days_back:].tolist()) / people[
                                'China']
deathsPerMillion['France'] = np.array(
    confirmed[death['Country/Region'].str.startswith('France')][0:53].sum(axis=0)[-days_back:].tolist()) / people[
                                 'France']

plt.close('all')


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


def plot_multi(ax, input_data, x_label, y_label, b_logarithmic=False, ):
    for country, data in input_data.items():
        if b_logarithmic:
            ax.semilogy(range(-days_back, 0), data, 'x-', label=country)
        else:
            ax.plot(range(-days_back, 0), data, 'x-', label=country)
    ax.legend()
    ax.set_xlabel(xlabel=x_label)
    ax.set_ylabel(ylabel=y_label)
    ax.grid()

def arrangeplots(datatoplot, ncols):
    # Tweak the figure size to be better suited for a row of numerous plots:
    # double the width and halve the height. NB: use relative changes because
    # some styles may have a figure size different from the default one.
    (fig_width, fig_height) = plt.rcParams['figure.figsize']
    fig_size = [fig_width * 2, fig_height / 2]
    numberofplots = datatoplot.__len__()
    nrows = numberofplots / ncols
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows.__int__(), figsize=(15, 10), squeeze=True)
    iCol = 0
    iRow = 0
    for title, data in datatoplot.items():
        plot_multi(axes[iRow,iCol], data, 'days before today', title)
        if (iCol >= ncols-1):
            iRow = iRow + 1
            iCol = 0
        else:
            iCol = iCol + 1


    # Deaths

datatoplot = {'deaths': deaths, 'deaths per million': deathsPerMillion, 'confirmed': conf,
                  'confirmed per million': confPerMillion}

# fig, ax = plt.subplots(figsize=(10, 5))

arrangeplots(datatoplot, ncols=2)

# plot_multi(deaths, 'days before today', 'deaths', True)
# plot_multi(deathsPerMillion, 'days before today', 'deaths per million', True)

# Confirmed
# plotmulti(conf, 'days before today', 'confirmed infections')

# plotmulti(confPerMillion, 'days before today','confirmed infections per million')

plt.show()
