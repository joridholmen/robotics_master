# -*- coding: utf-8 -*-


__author__ = 'Jorid Holmen', 'Christianie Torres'
__email__ = 'jorid.holmen@nmbu.no', 'christianie.torres@nmbu.no'

import random
import operator

from biosim.Animals import Herbivore, Carnivore


class Cell:
    """
    Class for cells
    """

    def __init__(self, population):
        random.seed()
        """
        :param population: A list with dictionaries
        :param herbivores_pop: a string
        :param carnivores_pop: a string
        :param copies: an integer
        :return: string, text concatenated copies times
        """

        self.herbivores_pop = []
        self.carnivores_pop = []
        self.N_herb = len(self.herbivores_pop)
        self.N_carn = len(self.carnivores_pop)
        for animal_info in population:
            if animal_info['species'] == 'Herbivore':
                self.herbivores_pop.append(Herbivore(animal_info))
            else:
                self.carnivores_pop.append(Carnivore(animal_info))

        self.available_fodder = self.p['f_max']

    @classmethod
    def set_given_parameters(cls, params):
        """
        Saves the parameters for the different cells for use in Cell class
        """
        for parameter in params:
            if parameter in cls.p:
                if params[parameter] < 0:
                    raise ValueError('Parameter must be positive')
                cls.p[parameter] = params[parameter]

    def sorting_animals(self):
        """
        A function for sorting the animals.
        Herbivores are sorted weakest to fittest, since the weakest are eaten first
        Carnivores are sorted fittest to weakest, since the fittest eats first
        """
        sorted_herbivores_pop = sorted(self.herbivores_pop, key=operator.attrgetter('phi'))
        sorted_carnivores_pop = sorted(self.carnivores_pop, key=operator.attrgetter('phi'))
        sorted_carnivores_pop.reverse()
        self.herbivores_pop = sorted_herbivores_pop
        self.carnivores_pop = sorted_carnivores_pop

    def make_herbivores_eat(self):
        """
        The animals eats available fodder until their appetite is filled.
        The eat_fodder-function from the Herbivore class does this.
        Herbivores eat in a random order, and therefore need to be randomised
        """
        self.available_fodder = self.p['f_max']
        random.shuffle(self.herbivores_pop)

        for animal in self.herbivores_pop:
            animal.eat_fodder(F_cell=self.available_fodder)
            self.available_fodder -= animal.F_consumption

    def feed_carnivores(self):
        """
        1. sorts herbivores and carnivores by fitness
        2. makes the carnivores eat
        3. makes the carnivores gain weight
        4. remove all eaten herbivores
        """
        self.sorting_animals()
        killed = []
        for carn in self.carnivores_pop:
            appetite = carn.p['F']
            weight_of_eaten_herbs = 0
            for herb in self.herbivores_pop:
                if weight_of_eaten_herbs < appetite:
                    if herb not in killed:
                        if carn.will_carn_kill(herb) is True:
                            carn.weight_gain_after_eating_herb(herb)
                            weight_of_eaten_herbs += herb.weight
                            killed.append(herb)

        for herb in killed:
            self.herbivores_pop.remove(herb)

    def newborn_animals(self):
        """
        An animal gives birth maximum once per year.The function birth_probability
        calculates if the animal will give birth or not and birth_weight_loss calculates the new
        weight for the mother.
        The newborn must be added to the list of either herbivores or carnivores
        """
        self.counting_animals()

        # for herbivores
        '''
        list_h = self.herbivores_pop
        list_new_h = []
        for k in range(self.N_herb):
            if list_h[k].will_the_animal_give_birth(n=self.N_herb) is True:
                newborn = Herbivore({'species': 'Herbivore',
                                     'weight': list_h[k].newborn_birth_weight, 'age': 0})
                list_h[k].birth_weight_loss(newborn_birth_weight=newborn.weight)
                list_new_h.append(newborn)

        for newborn in list_new_h:
            list_h.append(newborn)

        self.herbivores_pop = list_h
        '''

        list_new_h = []
        for herb in self.herbivores_pop:
            if herb.will_the_animal_give_birth(n=self.N_herb) is True:
                newborn = Herbivore({'species': 'Herbivore',
                                     'weight': herb.newborn_birth_weight, 'age': 0})
                herb.birth_weight_loss(newborn_birth_weight=newborn.weight)
                list_new_h.append(newborn)

        for newborn in list_new_h:
            self.herbivores_pop.append(newborn)

        # for carnivores
        list_c = self.carnivores_pop
        list_new_c = []
        for k in range(self.N_carn):
            if list_c[k].will_the_animal_give_birth(n=self.N_carn) is True:
                newborn = Carnivore({'species': 'Carnivore',
                                     'weight': list_c[k].newborn_birth_weight, 'age': 0})
                list_c[k].birth_weight_loss(newborn_birth_weight=newborn.weight)
                list_new_c.append(newborn)

        for k in list_new_c:
            list_c.append(k)

        self.carnivores_pop = list_c

    def move_animals_from_cell(self):
        """
        Checks if the animal has moved previously and also if move_single_animal() = True
        If it is it is added to herbs/carns_move and removed from the herbivores/carnivores_pop
        Later already_moved is changed to True

        :return: tot_animals, list with a list of the moving herbivores and a list of the moving
        carnivores
        :rtype: list
        """
        self.herbs_move = []
        herbs = self.herbivores_pop
        for herb in herbs:
            if herb.move_single_animal():
                herb.already_moved = True
                self.herbs_move.append(herb)

        self.carns_move = []
        carns = self.carnivores_pop
        for carn in carns:
            if carn.move_single_animal():
                carn.already_moved = True
                self.carns_move.append(carn)

        tot_animals = [self.herbs_move, self.carns_move]
        return tot_animals

    def move_animals_to_cell(self, list_of_moving_animals):
        """
        Adds the migrating animals into a new cell

        :param list_of_moving_animals: list with a list of the moving herbivores and a list of the
        moving carnivores
        :type list_of_moving_animals: list
        """

        herbs_moved = list_of_moving_animals[0]
        carns_moved = list_of_moving_animals[1]

        for herb in herbs_moved:
            self.herbivores_pop.append(herb)

        for carn in carns_moved:
            self.carnivores_pop.append(carn)

    def reset_already_moved(self):
        """
        After all the animals in all the cells have moved, they will reset so that they can move
        again next year
        """
        for animal in self.herbivores_pop:
            animal.already_moved = False
        for animal in self.carnivores_pop:
            animal.already_moved = False

    def counting_animals(self):
        """
        A function for counting how many animals there are in the cell.
        We also need to differentiate between the different animals and provide two
        variables for this
        """
        self.N_herb = len(self.herbivores_pop)
        self.N_carn = len(self.carnivores_pop)

    # yearly activities:

    def make_animals_age(self):
        """
        Each year the animals ages. Here we use the aging function from the herbivore class
        """
        '''
        for animal in self.herbivores_pop:
            animal.aging()
        for animal in self.carnivores_pop:
            animal.aging()
        '''

        # noinspection PyTypeChecker
        animals = self.herbivores_pop + self.carnivores_pop

        for animal in animals:
            animal.aging()

    def make_animals_lose_weight(self):
        """
        Each year the animal loses weight based on their own weight and eta
        """
        for animal in self.herbivores_pop:
            animal.weight_loss()
        for animal in self.carnivores_pop:
            animal.weight_loss()

    def dead_animals_natural_cause(self):
        """
        Each year some animals will die of natural causes. We check if the animal dies or not
        by using the function death_probability. After we need to remove them from the from the
        list of animals
        """
        herbs = []
        for herb in self.herbivores_pop:
            #herb.death_probability()
            if herb.will_the_animal_die() is False:
                herbs.append(herb)

        carns = []
        for carn in self.carnivores_pop:
            #carn.death_probability()
            if carn.will_the_animal_die() is False:
                carns.append(carn)

        self.herbivores_pop = herbs
        self.carnivores_pop = carns


class Lowland(Cell):
    """
    subclass for lowland cells
    """
    p = {'f_max': 800.0}

    def __init__(self, population):
        """
        Initialises lowland class

        :param population: list of dictionaries containing animals
        :type population: list
        """
        self.habitable = True
        super().__init__(population)


class Highland(Cell):
    """
    subclass for highland class
    """
    p = {'f_max': 300.0}

    def __init__(self, population):
        """
        Initialises highland class

        :param population: list of dictionaries containing animals
        :type population: list
        """
        self.habitable = True
        super().__init__(population)


class Desert(Cell):
    """
    subclass for highland class
    """
    p = {'f_max': 0}

    def __init__(self, population):
        """
        Initialises desert class

        :param population: list of dictionaries containing animals
        :type population: list
        """
        self.habitable = True
        super().__init__(population)


class Water(Cell):
    """
    subclass for highland class
    """
    p = {'f_max': 0}

    def __init__(self, population):
        """
        Initialises water class

        :param population: list of dictionaries containing animals
        :type population: list
        """
        self.habitable = False
        super().__init__(population)
