import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

#indizes = {'Mexico': 160, 'Germany': 122, 'Spain':203, 'Sweden': 207, 'Italy': 139, 'Austria': 18}  # , 'Hubei':154}
indizes = {'Mexico': 158, 'Germany': 120, 'Spain':201, 'Sweden': 205, 'Italy': 137, 'Austria': 16}  # , 'Hubei':154}
#indizes = {'Mexico': 46, 'Germany': 11, 'Spain':18, 'Sweden': 17, 'Italy': 16, 'Austria': 32}  # , 'Hubei':154}
days_back = 40

def read_input_data():
    #confirmed = pd.read_csv(
      #  "../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
    confirmed = pd.read_csv("../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
    #death = pd.read_csv("../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
    death = pd.read_csv("../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")
    #recovered = pd.read_csv(
        #"../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")
    recovered = pd.read_csv(
    "../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
    return confirmed, death, recovered

def readData():
    confirmed, death, recovered = read_input_data()

    # select plot data
    countries = indizes
    # countries = {'Germany': 11, 'Sweden': 17, 'Italy': 16, 'Austria': 32}
    people = {'Germany': 82.79, 'Spain': 46.66, 'Sweden': 10.12, 'Italy': 60.48, 'Austria': 8.822, 'China': 1386, 'USA': 327.2,
              'France': 66.99, 'Mexico': 129.2, 'Hubei': 57.2}
    conf = {k: np.array(confirmed[confirmed['Country/Region'] == k].T[v].tolist()[-days_back:]) for k, v in
            countries.items()}
    conf['USA'] = np.array(
        confirmed[confirmed['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist())
    conf['China'] = np.array(
        confirmed[confirmed['Country/Region'].str.startswith('Chin')][0:53].sum(axis=0)[-days_back:].tolist())
    conf['France'] = np.array(
        confirmed[confirmed['Country/Region'].str.startswith('France')][0:53].sum(axis=0)[-days_back:].tolist())

    deaths = {k: np.array(death[death['Country/Region'] == k].T[v].tolist()[-days_back:]) for k, v in countries.items()}
    deaths['USA'] = np.array(death[death['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist())
    deaths['China'] = np.array(
        death[death['Country/Region'].str.startswith('Chin')][0:53].sum(axis=0)[-days_back:].tolist())
    deaths['France'] = np.array(
        death[death['Country/Region'].str.startswith('France')][0:53].sum(axis=0)[-days_back:].tolist())

    # reco = {k: np.array(recovered[recovered['Country/Region'] == k].T[v].tolist()[-days_back:]) for k, v in countries.items()}
    # reco['USA'] = np.array(recovered[recovered['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist())
    # reco['China'] = np.array(
    #     recovered[recovered['Country/Region'].str.startswith('Chin')][0:53].sum(axis=0)[-days_back:].tolist())
    # reco['France'] = np.array(
    #     recovered[recovered['Country/Region'].str.startswith('France')][0:53].sum(axis=0)[-days_back:].tolist())
    reco = {}
    return deaths, conf, reco, people, countries