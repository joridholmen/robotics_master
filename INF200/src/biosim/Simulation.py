# -*- coding: utf-8 -*-
"""
Template for BioSim class.
"""

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU

__author__ = 'Jorid Holmen', 'Christianie Torres'
__email__ = 'jorid.holmen@nmbu.no', 'Christianie.torres@nmbu.no'

from biosim.Animals import Herbivore, Carnivore
from biosim.Cell import Lowland, Highland, Desert, Water
from biosim.MapIsland import Map_Island

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import subprocess
import os


class BioSim:
    """ A class for BioSIm that simulates the dynamics of the island and creates graphics"""

    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None, log_file=None):

        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param img_years: years between visualizations saved to files (default: vis_years)
        :param log_file: If given, write animal counts to this file

        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.

        If img_dir is None, no figures are written to file. Filenames are formed as

            f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'

        where img_number are consecutive image numbers starting from 0.

        img_dir and img_base must either be both None or both strings.
        """
        random.seed(seed)

        self.island_map_graph = Map_Island(island_map, ini_pop)
        self.island_map_graph.create_map_dict()

        self.num_years_simulated = 0

        img_name = 'figures'

        if img_base is None:
            if img_dir is not None:
                self.img_base = os.path.join(img_dir, img_name)
            else:
                self.img_base = None
        else:
            self.img_base = img_base

        self.img_fmt = img_fmt

        self.img_ctr = 0

        self.vis_years = vis_years

        if cmax_animals is None:
            self.cmax_carn = 50
            self.cmax_herb = 200
        else:
            self.cmax_carn = cmax_animals['Carnivore']
            self.cmax_herb = cmax_animals['Herbivore']

        if hist_specs is None:
            self.hist_specs = {'fitness': {'max': 1, 'delta': 0.05}, 'age': {'max': 60, 'delta': 2},
                               'weight': {'max': 60, 'delta': 2}}
        else:
            self.hist_specs = hist_specs

    def set_animal_parameters(self, species, p):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param p: Dict with valid parameter specification for species
        """

        class_names = {'Herbivore': Herbivore, 'Carnivore': Carnivore}
        for param_name in p.keys():
            if param_name in class_names[species].p:
                class_names[species].p[param_name] = p[param_name]

    def set_landscape_parameters(self, landscape, p):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param p: Dict with valid parameter specification for landscape
        """
        class_names = {'L': Lowland, 'H': Highland, 'D': Desert, 'W': Water}
        for param_name in p.keys():
            if param_name in class_names[landscape].p.keys():
                class_names[landscape].p[param_name] = p[param_name]

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """
        self.phi_array_herb = []
        self.age_array_herb = []
        self.weight_array_herb = []
        self.N_herb = []
        self.N_carn = []

        self.phi_array_carn = []
        self.age_array_carn = []
        self.weight_array_carn = []
        self.N_total = []
        self.V_year = []
        self.num_years = num_years
        self.setup_graphics()

        for year in range(num_years):

            self.island_map_graph.year_cycle()
            self.data_heat_map_herb = []
            self.data_heat_map_carn = []

            for loc, cell in self.island_map_graph.map.items():

                nr_herbs_cell = len(cell.herbivores_pop)
                nr_carns_cell = len(cell.carnivores_pop)
                self.data_heat_map_herb.append(nr_herbs_cell)
                self.data_heat_map_carn.append(nr_carns_cell)
                for herb in cell.herbivores_pop:
                    self.phi_array_herb.append(herb.phi)
                    self.age_array_herb.append(herb.age)
                    self.weight_array_herb.append(herb.weight)
                for carn in cell.carnivores_pop:
                    self.phi_array_herb.append(carn.phi)
                    self.age_array_herb.append(carn.age)
                    self.weight_array_herb.append(carn.weight)

            self.N_herb.append(self.num_animals_per_species['Herbivore'])
            self.N_carn.append(self.num_animals_per_species['Carnivore'])
            self.N_total.append(self.num_animals)
            self.V_year.append(self.num_years_simulated)

            self.update_graphics()

            self.num_years_simulated += 1

        # values needed after stopping:
        number_of_simulated_years = self.num_years_simulated
        total_number_of_animals = self.num_animals

        print('Number of animals:', total_number_of_animals)
        print(self.num_animals_per_species)
        print('Number of simulated years:', number_of_simulated_years)

    def setup_graphics(self):
        """
        Sets up the graphics of the island
        """
        self.fig = plt.figure()
        self.gs = gridspec.GridSpec(ncols=3, nrows=3, figure=self.fig)
        self.create_map()

        # years
        self.axt = self.fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
        self.axt.axis('off')
        self.template = 'Years: %s' % self.num_years_simulated
        self.txt = self.axt.text(0.5, 0.5, self.template.format(0),
                                 horizontalalignment='center',
                                 verticalalignment='center',
                                 transform=self.axt.transAxes)

        self.ax2 = self.fig.add_subplot(self.gs[0, 2])
        self.ax2.set_title('Animal count')

        self.ax3 = self.fig.add_subplot(self.gs[1, 0])
        self.ax3.set_title("Herbivore distribution")
        self.axes_bar = self.fig.add_axes([0.32, 0.4, 0.01, 0.2])

        self.ax4 = self.fig.add_subplot(self.gs[1, 2])
        self.ax4.set_title("Carnivore distribution")
        self.axes_bar2 = self.fig.add_axes([0.95, 0.4, 0.01, 0.2])

        self.ax5 = self.fig.add_subplot(self.gs[2, 0])
        self.ax5.set_title('fitness')

        self.ax6 = self.fig.add_subplot(self.gs[2, 1])
        self.ax6.set_title('age')

        self.ax7 = self.fig.add_subplot(self.gs[2, 2])
        self.ax7.set_title('weight')
        self.fig = self.fig.tight_layout()

    def update_graphics(self):
        """
        Updates the graphics of the island
        """
        if self.vis_years > 0:
            if self.num_years_simulated % self.vis_years == 0:
                self.template = 'Years: %s' % self.num_years_simulated
                self.txt.set_text(self.template.format(0))

                self.ax2.clear()
                self.ax2.plot(self.V_year, self.N_herb, 'b', label='herb')
                self.ax2.plot(self.V_year, self.N_carn, 'r', label='carn')
                handles, labels = self.ax2.get_legend_handles_labels()
                self.ax2.legend(handles=handles, labels=labels)

                self.x = self.island_map_graph.x_coord
                self.y = self.island_map_graph.y_coord

                # HEAT MAP HERB

                self.heatmap_herb = self.ax3.imshow(
                    np.array(self.data_heat_map_herb).reshape(self.x, self.y),
                    extent=[1, self.x, self.y, 1], vmin=0,
                    vmax=self.cmax_herb, cmap='viridis', interpolation="nearest")

                plt.colorbar(self.heatmap_herb, cax=self.axes_bar)

                # HEAT MAP CARN
                self.heatmap_carn = self.ax4.imshow(
                    np.array(self.data_heat_map_carn).reshape(self.x, self.y),
                    extent=[1, self.x, self.y, 1], vmin=0,
                    vmax=self.cmax_carn, cmap='viridis', interpolation="nearest")

                plt.colorbar(self.heatmap_carn, cax=self.axes_bar2)

                # FITNESS
                self.ax5.clear()
                self.bins_fit_f = int(
                    self.hist_specs['fitness']['max'] / self.hist_specs['fitness']['delta'])
                self.range_f = (0, self.hist_specs['fitness']['max'])
                self.ax5.hist(self.phi_array_herb, bins=self.bins_fit_f, range=self.range_f,
                              label='phi herbs', histtype='step',
                              edgecolor='b')
                self.ax5.hist(self.phi_array_carn, bins=self.bins_fit_f, range=self.range_f,
                              label='phi carns', histtype='step',
                              edgecolor='r')
                handles, labels = self.ax5.get_legend_handles_labels()
                self.ax5.legend(labels=labels)

                # AGE
                self.ax6.clear()
                self.bins_fit_a = int(
                    self.hist_specs['age']['max'] / self.hist_specs['age']['delta'])
                self.range_a = (0, self.hist_specs['age']['max'])
                self.ax6.hist(self.age_array_herb, bins=self.bins_fit_a, range=self.range_a,
                              label='age herbs', histtype='step',
                              edgecolor='b')
                self.ax6.hist(self.age_array_carn, bins=self.bins_fit_a, range=self.range_a,
                              label='age carns', histtype='step',
                              edgecolor='r')
                handles, labels = self.ax6.get_legend_handles_labels()
                self.ax6.legend(handles=handles, labels=labels)

                # WEIGHT
                self.ax7.clear()
                self.bins_fit_w = int(
                    self.hist_specs['weight']['max'] / self.hist_specs['weight']['delta'])
                self.range_w = (0, self.hist_specs['weight']['max'])
                self.ax7.hist(self.weight_array_herb, bins=self.bins_fit_w, range=self.range_w,
                              label='weight herbs', histtype='step',
                              edgecolor='b')
                self.ax7.hist(self.weight_array_carn, bins=self.bins_fit_w, range=self.range_w,
                              label='weight carns', histtype='step',
                              edgecolor='r')
                handles, labels = self.ax7.get_legend_handles_labels()
                self.ax7.legend(labels=labels)

                plt.pause(0.01)
                if self.num_years_simulated % self.vis_years == 0:
                    self._save_graphics()

    def create_map(self):
        """
        Creates a graphic map of the island
        """
        # Each letter has a colour value
        #                  R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in self.island_map_graph.geo.splitlines()]

        # Adding axes to a empty figure that will be the island
        self.ax_im = self.fig.add_subplot(self.gs[0, 0])  # llx, lly, w, h

        # shows the island with  water
        self.ax_im.imshow(map_rgb)
        if (len(map_rgb[0])) < 21:
            self.ax_im.set_xticks(range(len(map_rgb[0])))
            self.ax_im.set_xticklabels(range(1, 1 + len(map_rgb[0])))
            self.ax_im.set_yticks(range(len(map_rgb)))
            self.ax_im.set_yticklabels(range(1, 1 + len(map_rgb)))

        # Creates a new coordinate system for the figure
        self.ax_lg = self.fig.add_axes([0.32, 0.71, 0.1, 0.26])  # llx, lly, w, h
        self.ax_lg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland', 'Highland', 'Desert')):
            self.ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1, edgecolor='none',
                                               facecolor=rgb_value[name[0]]))
            self.ax_lg.text(0.35, ix * 0.2, name, transform=self.ax_lg.transAxes)

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island_map_graph.add_population(population)

    @property
    def year(self):
        """
        Last year simulated.
        :return: the last year simulated
        :rtype: float
        """
        return self.num_years_simulated

    @property
    def num_animals(self):
        """
        Total number of animals on island.
        :return: total number of animals
        :rtype: float
        """
        num_carnivores = 0
        num_herbivores = 0
        for cell in self.island_map_graph.map.values():
            num_carnivores += len(cell.carnivores_pop)
            num_herbivores += len(cell.herbivores_pop)
        number_of_animals = num_carnivores + num_herbivores
        return number_of_animals

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.
        :return: number of animals per species
        :rtype: dict
        """
        num_animals_per_species = {"Herbivore": 0, "Carnivore": 0}
        for cell in self.island_map_graph.map.values():
            num_animals_per_species["Herbivore"] += len(cell.herbivores_pop)
            num_animals_per_species["Carnivore"] += len(cell.carnivores_pop)
        return num_animals_per_species

    def _save_graphics(self):
        """
        Saves graphics to file if file name given.
        :return: nothing if img_base is None
        """

        if self.img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self.img_ctr,
                                                     type=self.img_fmt))
        self.img_ctr += 1

    def make_movie(self, movie_fmt=None):
        """
        Creates MPEG4 movie from visualization images saved.

        .. :note:
            Requires ffmpeg for MP4 and magick for GIF

        The movie is stored as img_base + movie_fmt
        """

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt is None:
            movie_fmt = 'mp4'

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call(['ffmpeg',
                                       '-i', '{}_%05d.png'.format(self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call(['magick',
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self.img_base),
                                       '{}.{}'.format(self.img_base, movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)
