# -*- encoding: utf-8 -*-

"""
This is a module that creates animals by using the class function
"""

__author__ = 'Christianie Torres', 'Jorid Holmen'
__email__ = 'christianie.torres@nmbu.no', 'jorid.holmen@nmbu.no'

import random
import math


class Animal:
    """
    This is a class for animals on the island. Parent class for Herbivore and Carnivore
    """

    def __init__(self, properties):
        """
        Initializing animal class for given values

        :param properties: dictionary containing species, age and weight for an animal
        :type properties: dict
        """
        random.seed()

        if properties["age"] < 0:
            raise ValueError('Age must be positive')
        else:
            self.age = properties["age"]

        if properties["weight"] < 0:
            raise ValueError('Weight must be positive')
        else:
            self.weight = properties["weight"]

        self.fitness()
        self.already_moved = False

    @classmethod
    def set_given_parameters(cls, params):
        """
        Saves new parameters for the different animals for use in Animals class

        :raises ValueError: if invalid landscape type is given in geography string
        """
        for parameter in params:
            if parameter in cls.p:
                if params[parameter] < 0:
                    raise ValueError('Parameter must be positive')
                cls.p[parameter] = params[parameter]

    def aging(self):
        """
        A function for aging the animal
        """
        self.age += 1
        self.fitness()

    def birth_weight_function(self):
        """
        Sets value of birth weight from a gaussian distribution
        """
        self.birth_weight = random.gauss(self.p['w_birth'], self.p['sigma_birth'])
        return self.birth_weight

    def weight_loss(self):
        """
        The animal loses weight each year
        """
        self.weight -= self.p['eta'] * self.weight
        self.fitness()

    def weight_gain(self, consumption):
        """
        The animal gains weight everytime they eat. In this function, appetite is described as
        what is eaten, but in some cases that is not possible.

        :param consumption: amount of fodder the animal consumes
        :type consumption: float
        """
        self.weight += self.p['beta'] * consumption
        self.fitness()

    def fitness(self):
        """
        The animal has a certain fitness. This function calculates the fitness for one animal,
        but does not update continuously
        """
        q_plus = 1 / (1 + math.exp(self.p['phi_age'] * (self.age - self.p['a_half'])))
        q_minus = 1 / (1 + math.exp(-self.p['phi_weight'] * (self.weight - self.p['w_half'])))

        if self.weight <= 0:
            self.phi = 0
        else:
            self.phi = q_plus * q_minus

        if 0 > self.phi or self.phi >= 1:
            return False
        else:
            return self.phi

    def birth_probability(self, n):
        """
        Animals can mate if there are two or more animals of the same species in the same cell.
        The animals can give birth with a probability, which depends on fitness and weight.
        If the newborn weighs more than the mother, the probability of birth is zero.

        :param n: number of animals in the cell
        :type n: float
        :return: the probability of birth
        :rtype: float
        """
        variable = self.p['gamma'] * self.phi * (n - 1)
        self.newborn_birth_weight = self.birth_weight_function()

        if self.weight < self.p['zeta'] * (self.p['w_birth'] + self.p['sigma_birth']):
            return 0
        elif self.weight <= self.newborn_birth_weight * self.p['zeta']:
            return 0
        else:
            return min(1, variable)

    def will_the_animal_give_birth(self, n):
        """
        If the random number generated is less than the probability for birth, the birth will not
        take place

        :param n: number of animals in the cell
        :type n: float
        :return: True if the birth takes place, False if not
        :rtype: bool
        """
        p = self.birth_probability(n)
        r = random.random()

        if r <= p:
            return True
        else:
            return False

    def birth_weight_loss(self, newborn_birth_weight):
        """
        If the mother gives birth, she looses weight

        :params newborn_birth_weight: the weight of the newborn
        :type newborn_birth_weight: float
        """
        self.weight -= self.p['zeta'] * newborn_birth_weight
        self.fitness()

    def death_probability(self):
        """
        The animal dies if it weighs nothing, but also with a probability

        :return: the probability of dying
        :rtype: float
        """
        if self.phi == 0:
            return 1
        else:
            return self.p['omega'] * (1 - self.phi)

    def will_the_animal_die(self):
        """
        If the random number generated is less than the probability the animal will die

        :return: True if animal dies, False if it survives
        :rtype: bool
        """
        p = self.death_probability()
        d = random.random()

        if d < p:
            return True
        else:
            return False

    def move_single_animal(self):
        """
        If the random number generated is less than prob_move, the animal will try to move

        :return: True if the animal will try to move, False if not
        :rtype: bool
        """
        prob_move = self.p['mu'] * self.phi
        m = random.random()
        if self.already_moved is False:
            if m < prob_move:
                return True
            else:
                return False
        else:
            return False


class Herbivore(Animal):
    """
    this is a class for herbivores on the island
    """

    p = {
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.6,
        "w_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0,
    }

    def __init__(self, properties):
        """
        Initialisation of weight and age for a new herbivore

        :param properties: dictionary containing species, weight and age
        :type properties: dict
        """
        super().__init__(properties)

    def eat_fodder(self, F_cell):
        """
        Herbivores tries to eat a certain amount in a year. However, how much the animal
        actually consumes depends on how much fodder is available in the cell.

        F_cell: how much food in the cell
        F: how much the herbivore wants to eat in a year (appetite)
        F_consumption: how much the herbivore actually eats

        After the consumption the herbivore gains weight

        :param F_cell: the amount of fodder available in the cell
        :type F_cell: float
        :Raises ValueError: if there is a nonnegative amount of fodder
        """
        if F_cell >= self.p['F']:
            self.F_consumption = self.p['F']
            self.weight_gain(consumption=self.F_consumption)
            if self.F_consumption < 0:
                raise ValueError('There has to be a nonnegative amount of fodder')
        else:
            self.F_consumption = F_cell
            self.weight_gain(consumption=self.F_consumption)
            if self.F_consumption < 0:
                raise ValueError('There has to be a nonnegative amount of fodder')


class Carnivore(Animal):
    """
    this is a class for carnivores  on the island
    """

    p = {
        "w_birth": 6.0,
        "sigma_birth": 1.0,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 40.0,
        "phi_age": 0.3,
        "w_half": 4.0,
        "phi_weight": 0.4,
        "mu": 0.4,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.8,
        "F": 50.0,
        "DeltaPhiMax": 10.0
    }

    def __init__(self, properties):
        """
        initialisation of weight and age for a new herbivore

        :param properties: dictionary containing species, weight and age
        :type properties: dict
        """
        super().__init__(properties)

    def probability_kill_herbivore(self, herb):
        """
        The carnivore kills a herbivore with probability prob_kill

        :param herb: the herbivore the carnivore will try to kill
        :type herb: class Herbivore
        :return: probability of killing
        :rtype: float
        """
        if self.phi <= herb.phi:
            return 0
        elif 0 < self.phi - herb.phi < self.p['DeltaPhiMax']:
            return (self.phi - herb.phi) / self.p['DeltaPhiMax']
        else:
            return 1

    def will_carn_kill(self, herb):
        """
        If the generated number is less than the probability for killing, the carnivore will eat
        the herbivore

        :param herb: the herbivore the carnivore will try to kill
        :type herb: class Herbivore
        :return: True if it will eat, False if not
        :rtype: bool
        """
        p = self.probability_kill_herbivore(herb)
        r = random.random()

        if r < p:
            return True
        else:
            return False

    def weight_gain_after_eating_herb(self, herb):
        """
        After eating the carnivore gains weight relative to the eaten herbivore

        :param herb: the herbivore the carnivore eats
        :type herb: class herbivore
        """
        self.weight_gain(consumption=herb.weight)
