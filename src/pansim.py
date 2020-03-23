#!/usr/bin/env python3
'''Simulate pandemic diseases

USAGE:
    pansim.py -d <days> -p <real_pop> -i <initial_infection_rate> -c <config>
    pansim.py -h|--help

AUTHORS:
    Steffen Brinkmann <s-b@mailbox.org>

LICENSE:
    © 2020 MIT License (https://mit-license.org/)
'''

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import datetime
import argparse
import configparser
import logging

FORMAT = '%(levelname)-8s %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)


def _parse_args():
    parser = argparse.ArgumentParser(description='Simulate pandemic diseases.')
    parser.add_argument('-d', '--days', type=int, default=30,
                        help='Number of days to simulate.')
    parser.add_argument('-p', '--population', type=int, default=80000000,
                        help='Population for generating "real" numbers.')
    parser.add_argument('-i', '--initial_infection_rate', type=float, default=2e-7,
                        help='Initial infection rate of population.')
    parser.add_argument('-c', '--config', type=str, default='config.cfg',
                        help='Configuration file for simulation parameters and other stuff.')

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = _parse_args()

    config = configparser.ConfigParser()
    config.read_file(open(args.config))

    t_incubation = int(config['simulation']['t_incubation'])
    t_sick = int(config['simulation']['t_sick'])
    infection_rate_incubation = float(config['simulation']['infection_rate_incubation'])
    infection_rate_sick = float(config['simulation']['infection_rate_sick'])
    death_rate_sick = float(config['simulation']['death_rate_sick'])
    no_symptoms_rate = float(config['simulation']['no_symptoms_rate'])

    # initialize variables
    # number of deceased by day
    dead = np.zeros(args.days + 1)
    # number of newly infected by day
    infected = np.zeros(args.days + 1)
    infected[0] = args.population * args.initial_infection_rate
    # total infected history
    total_infected_history = np.copy(infected)
    # infectable population by day. i.e. never been infected
    infectable_population = np.zeros(args.days + 1)
    infectable_population[0] = args.population - infected[0]

    # main loop
    for d in range(1, args.days + 1):
        logging.debug(d)
        new_infections = 0
        # new infections due to infected but not (yet) sick people
        # logging.debug(f'inf: \t{max(0, d - t_incubation)}\t{max(0, d)}')
        new_infections += (sum(infected[max(0, d - t_incubation):d])
                           * (infection_rate_incubation - 1)
                           * infectable_population[d - 1] / args.population)

        # new infections due to sick people
        # logging.debug(f'sick:\t{max(0, d - t_incubation - t_sick)}\t{max(0, d - t_incubation)}')
        new_infections += (sum(infected[max(0, d - t_incubation - t_sick): max(0, d - t_incubation)])
                           * (infection_rate_sick - 1)
                           * infectable_population[d - 1] / args.population
                           * (1 - no_symptoms_rate))
        # new infections due to sick people who don't have (severe) symptoms,
        # i.e. the infection rate of "infected, but not sick"
        new_infections += (sum(infected[max(0, d - t_incubation - t_sick): max(0, d - t_incubation)])
                           * (infection_rate_incubation - 1)
                           * infectable_population[d - 1] / args.population
                           * no_symptoms_rate)

        logging.debug(new_infections)
        infected[d] = new_infections
        infectable_population[d] = infectable_population[d - 1] - new_infections

        # deaths
        dead[d] = (infected[max(0, d - t_incubation - t_sick): max(0, d - t_incubation)]
                   * (1 - (1. - death_rate_sick) ** (1. / t_sick))).sum()
        infectable_population[d] -= dead[d]
        infected[max(0, d - t_incubation - t_sick): max(0, d - t_incubation)] *= ((1. - death_rate_sick)
                                                                                  ** (1. / t_sick))

        # recording history
        total_infected_history[d] = infected.sum()

    logging.debug([round(x) for x in infected])
    logging.debug([round(x) for x in infected.cumsum()])
    logging.debug([round(x) for x in infectable_population])
    logging.debug([round(x) for x in dead])
    logging.debug([round(x) for x in total_infected_history])
    logging.debug([round(x, 3) for x in total_infected_history[1:] / total_infected_history[:-1]])
    logging.debug((total_infected_history[-1] / total_infected_history[0]) ** (1 / len(total_infected_history)))


    result = pd.DataFrame({'total infections': total_infected_history, 'acc. deaths': dead.cumsum()}).round()

    print(result)

    plt.semilogy(total_infected_history)
    plt.semilogy(dead.cumsum())
    plt.grid()
    plt.show()
