# Plot per country
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
from reader import read_input_data
from reader import indizes
from reader import days_back

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

def prepareplotpercountry(country):
    confirmed, death, recovered = read_input_data()
    countries = {country: indizes[country]}
    #countries = {country: indizes[country], 'Italy': 16}
    conf = {k: np.array(confirmed[confirmed['Country/Region'] == k].T[v].tolist()[-days_back:]) for k, v in countries.items()}
    #conf['USA'] = np.array(confirmed[confirmed['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist())
    #conf
    deaths = {k: np.array(death[death['Country/Region'] == k].T[v].tolist()[-days_back:]) for k, v in countries.items()}
    #conf['USA'] = np.array(confirmed[confirmed['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist())
    #deaths
    #    reco = {k: np.array(recovered[recovered['Country/Region'] == k].T[v].tolist()[-days_back:]) for k, v in countries.items()}
    reco = {}
    #conf['USA'] = np.array(confirmed[confirmed['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist())
    #reco
    return conf, deaths, reco


def countryplot(b_logarithmic=True):
    global conf
    global deaths
    global reco
    fig, ax = plt.subplots(figsize=(15,10))
    if (b_logarithmic):
        for country, data in conf.items():
            #    ax.semilogy(range(-days_back, 0), data, 'x-', label=country)
            ax.semilogy(range(-days_back, 0), conf[country], 'x-', label="confirmed "+country)
            ax.semilogy(range(-days_back, 0), deaths[country], 'x-', label="deaths "+ country)
           # ax.semilogy(range(-days_back, 0), reco[country], 'x-', label="recovered "+ country)
        ax.legend()
        ax.set_xlabel('days before today')
        ax.set_ylabel('Cases')
        ax.grid()
    else:
        fig, ax = plt.subplots(figsize=(15,10))
        for country, data in conf.items():
            #    ax.semilogy(range(-days_back, 0), data, 'x-', label=country)
            ax.plot(range(-days_back, 0), conf[country], 'x-', label="confirmed "+country)
            ax.plot(range(-days_back, 0), deaths[country], 'x-', label="deaths "+country)
          #  ax.plot(range(-days_back, 0), reco[country], 'x-', label="recovered "+country)
        ax.legend()
        ax.set_xlabel('days before today')
        ax.set_ylabel('Cases')
        ax.grid()

    plt.show()


#deaths, deathsPerMillion, conf, confPerMillion, recovered, recoveredPerMillion = readData()
country='Germany'
conf, deaths, reco = prepareplotpercountry(country)
countryplot(b_logarithmic=False)
#countryplot(b_logarithmic=True)
