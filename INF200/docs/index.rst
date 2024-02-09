.. biosim documentation master file, created by
   sphinx-quickstart on Fri Jun  4 01:29:24 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to biosim's documentation!
==================================
This is a simulation of an island including
 * Herbivores
 * Carnivores
 * Several landscapes
 * An island

The animals module creates herbivores and carnivores.

The cell module creates cells, consisting of lowland,
highland, desert and water. In the cell module we also
include what happens in the cell, eg. feeding and
procreation.

In the MapIsland module we create the island and put
together all the cells. In addition it simulates everything
that happens on the island during a year.

In the simulation module we simulate the whole island,
including the visualisation.

Comments on code
 * We are aware of the carnivores dying out during every
   simulation, but we did not find a solution to that
   problem before the deadline. We suspect it has something
   to do with the carnivores eating the herbivores.
 * When simulating with just herbivores in a single cell,
   the herbivore population does not reach 200, as it should.
   We are yet to find the source of that problem.



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   Simulation
   MapIsland
   Cell
   Animals

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

