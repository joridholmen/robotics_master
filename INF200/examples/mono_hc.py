# -*- coding: utf-8 -*-

"""
Island with single jungle cell, first herbivores only, later carnivores.
"""


__author__ = 'Hans Ekkehard Plesser, NMBU'


import textwrap
from biosim.Simulation import BioSim


geogr = """\
            WWW
            WLW
            WWW"""

ini_herbs = [{'loc': (2, 2),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(1000)]}]
ini_carns = [{'loc': (2, 2),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(10)]}]

#for seed in range(100, 101):
sim = BioSim(geogr, ini_herbs+ini_carns, seed=100,
             img_dir='results', img_base=f'mono_hc_{100:05d}', img_years=300)
sim.simulate(50)
sim.add_population(ini_carns)
sim.simulate(251)
