# -*- encoding: utf-8 -*-

"""
"""

__author__ = 'Christianie Torres'
__email__ = 'christianie.torres@nmbu.no'

# -*- coding: utf-8 -*-

"""
Island with single jungle cell, first herbivores only, later carnivores.
"""


__author__ = 'Hans Ekkehard Plesser, NMBU'


import textwrap
from biosim.Simulation import BioSim


geogr = """\
            WWWWWWW
            WDDDDDW
            WDDDDDW
            WDDDDDW
            WDDDDDW
            WDDDDDW
            WWWWWWW"""

ini_herbs = [{'loc': (4, 4),
              'pop': [{'species': 'Herbivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(1000)]}]
ini_carns = [{'loc': (4, 4),
              'pop': [{'species': 'Carnivore',
                       'age': 5,
                       'weight': 20}
                      for _ in range(2000)]}]

for seed in range(100, 103):
    sim = BioSim(geogr, ini_herbs, seed=seed,
                 img_dir='results', img_base=f'mono_hc_{seed:05d}', img_years=300)


    sim.set_animal_parameters('Herbivore', {'mu': 1, 'omega': 0, 'gamma': 0, 'F': 0,
                                            'a_half': 1000})
    sim.set_animal_parameters('Carnivore', {'mu': 1, 'omega': 0, 'gamma': 0, 'F': 0,
                                            'a_half': 1000})

    sim.simulate(50)
    sim.add_population(ini_carns)
    sim.simulate(251)