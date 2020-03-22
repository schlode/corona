import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math

indizes = {'Mexico': 46, 'Germany': 11, 'Sweden': 17, 'Italy': 16, 'Austria': 32}  # , 'Hubei':154}
days_back = 10

def read_input_data():
    confirmed = pd.read_csv(
        "../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv")
    death = pd.read_csv("../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv")
    recovered = pd.read_csv(
        "../../COVID-19/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv")
    return confirmed, death, recovered

def readData():
    confirmed, death, recovered = read_input_data()

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

    # confPerMillion = {conf[k] / people[k] for k, v in countries.items()}
    confPerMillion = {}
    for k in countries.keys():
        confPerMillion[k] = conf[k] / people[k]
    confPerMillion['USA'] = conf['USA'] / people['USA']
    confPerMillion['China'] = conf['China'] / people['China']
    confPerMillion['France'] = conf['France'] / people['France']

    deaths = {k: np.array(death[death['Country/Region'] == k].T[v].tolist()[-days_back:]) for k, v in countries.items()}
    deaths['USA'] = np.array(death[death['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist())
    deaths['China'] = np.array(
        death[death['Country/Region'].str.startswith('Chin')][0:53].sum(axis=0)[-days_back:].tolist())
    deaths['France'] = np.array(
        death[death['Country/Region'].str.startswith('France')][0:53].sum(axis=0)[-days_back:].tolist())

    reco = {k: np.array(recovered[recovered['Country/Region'] == k].T[v].tolist()[-days_back:]) for k, v in countries.items()}
    reco['USA'] = np.array(recovered[recovered['Country/Region'].str.startswith('US')][0:53].sum(axis=0)[-days_back:].tolist())
    reco['China'] = np.array(
        recovered[recovered['Country/Region'].str.startswith('Chin')][0:53].sum(axis=0)[-days_back:].tolist())
    reco['France'] = np.array(
        recovered[recovered['Country/Region'].str.startswith('France')][0:53].sum(axis=0)[-days_back:].tolist())


    # deathsPerMillion = {deaths[k] / people[k] for k, v in countries.items()}
    deathsPerMillion = {}
    for k in countries.keys():
        deathsPerMillion[k] = deaths[k] / people[k]
    deathsPerMillion['USA'] = deaths['USA'] / people['USA']
    deathsPerMillion['China'] = deaths['China'] / people['China']
    deathsPerMillion['France'] = deaths['France'] / people['France']
    print('deaths ')
    print(deaths['Italy'])
    print('deaths per million')
    print(deathsPerMillion['Italy'])

    recoveredPerMillion = {}
    for k in countries.keys():
        recoveredPerMillion[k] = reco[k] / people[k]
    recoveredPerMillion['USA'] = reco['USA'] / people['USA']
    recoveredPerMillion['China'] = reco['China'] / people['China']
    recoveredPerMillion['France'] = reco['France'] / people['France']

    return deaths, deathsPerMillion, conf, confPerMillion, reco, recoveredPerMillion