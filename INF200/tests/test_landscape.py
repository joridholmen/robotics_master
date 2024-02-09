"""'
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
"""

from biosim.Cell import Lowland, Highland, Desert, Water
from biosim.Animals import Herbivore, Carnivore
import pytest


@pytest.fixture(autouse=True)
def reset_parameters():
    Herbivore.p['F'] = 10
    Carnivore.p['F'] = 50
    #Lowland.af = 800
    Lowland.p['f_max'] = 800


@pytest.fixture
def list_herbivores_and_carnivores():
    return [{'species': 'Herbivore', 'weight': 35, 'age': 5},
            {'species': 'Herbivore', 'weight': 41, 'age': 8},
            {'species': 'Herbivore', 'weight': 50, 'age': 9},
            {'species': 'Carnivore', 'weight': 70, 'age': 10},
            {'species': 'Herbivore', 'weight': 10, 'age': 3},
            {'species': 'Herbivore', 'weight': 60, 'age': 3}]


@pytest.fixture
def list_herbivores():
    return [{'species': 'Herbivore', 'weight': 35, 'age': 5},
            {'species': 'Herbivore', 'weight': 41, 'age': 8},
            {'species': 'Herbivore', 'weight': 50, 'age': 9},
            {'species': 'Herbivore', 'weight': 10, 'age': 3},
            {'species': 'Herbivore', 'weight': 14, 'age': 3},
            {'species': 'Herbivore', 'weight': 13, 'age': 3}]


@pytest.fixture
def list_carnivores():
    return [{'species': 'Carnivore', 'weight': 35, 'age': 5},
            {'species': 'Carnivore', 'weight': 41, 'age': 8},
            {'species': 'Carnivore', 'weight': 50, 'age': 9},
            {'species': 'Carnivore', 'weight': 10, 'age': 3},
            {'species': 'Carnivore', 'weight': 14, 'age': 3},
            {'species': 'Carnivore', 'weight': 13, 'age': 3}]


@pytest.fixture
def list_herbivore_long():
    return [{'species': 'Herbivore', 'weight': 65, 'age': 3},
            {'species': 'Herbivore', 'weight': 41, 'age': 3},
            {'species': 'Herbivore', 'weight': 50, 'age': 3},
            {'species': 'Herbivore', 'weight': 40, 'age': 3},
            {'species': 'Herbivore', 'weight': 41, 'age': 3},
            {'species': 'Herbivore', 'weight': 50, 'age': 9},
            {'species': 'Herbivore', 'weight': 67, 'age': 5},
            {'species': 'Herbivore', 'weight': 41, 'age': 8},
            {'species': 'Herbivore', 'weight': 50, 'age': 9}]


@pytest.fixture
def list_carnivore_long():
    return [{'species': 'Carnivore', 'weight': 65, 'age': 3},
            {'species': 'Carnivore', 'weight': 41, 'age': 3},
            {'species': 'Carnivore', 'weight': 50, 'age': 3},
            {'species': 'Carnivore', 'weight': 40, 'age': 3},
            {'species': 'Carnivore', 'weight': 41, 'age': 3},
            {'species': 'Carnivore', 'weight': 50, 'age': 9},
            {'species': 'Carnivore', 'weight': 67, 'age': 5},
            {'species': 'Carnivore', 'weight': 41, 'age': 8},
            {'species': 'Carnivore', 'weight': 50, 'age': 9}]


# tests for initial values:
def test_lowland_given_fodder():
    """
    When initialising a cell it is given an amount for fodder. The fodder in Lowland is 800
    """
    l = Lowland(population=[{'species': 'Carnivore', 'weight': 50, 'age': 9}])
    assert l.p['f_max'] == 800


def test_highland_given_fodder():
    """
    When initialising a cell it is given an amount for fodder. The fodder in Highland is 300
    """
    h = Highland(population=[{'species': 'Carnivore', 'weight': 50, 'age': 9}])
    assert h.p['f_max'] == 300


def test_water_unhabitable():
    """
    An animal can not enter the water. It is therefore unhabitable.
    """
    w = Water(population=[])
    assert w.habitable is False


def test_desert_habitable():
    """
    An animal can enter the even though there are no food
    """
    d = Desert(population=[])
    assert d.habitable is True


# tests for sorting_animals function
def test_sorting_herb(list_herbivores_and_carnivores):
    """
    This is a test that checks if the herbivores get sorted in a list based on ascending
    phi-value.
    """
    l = Lowland(population=list_herbivores_and_carnivores)
    unsorted_herbs = l.herbivores_pop
    herbs_fitness = [k.phi for k in unsorted_herbs]
    herbs_fitness.sort()
    l.sorting_animals()
    sorted_herbs_fitness = [k.phi for k in l.herbivores_pop]
    assert herbs_fitness == sorted_herbs_fitness


def test_sorting_carn(list_herbivores_and_carnivores):
    """
    This is a test that checks if the carnivores get sorted in a list based on descending
    phi-value.
    """
    l = Lowland(population=list_herbivores_and_carnivores)
    unsorted_carns = l.carnivores_pop
    carns_fitness = [k.phi for k in unsorted_carns]
    carns_fitness.sort()
    carns_fitness.reverse()
    l.sorting_animals()
    sorted_carns_fitness = [k.phi for k in l.carnivores_pop]
    assert carns_fitness == sorted_carns_fitness


# Tests for make_herbivores_eat function:
def test_eats_random(list_herbivores):
    """
    The herbivores should eat in a  random order. To test this, i assign all the herbs a False
    value. I make the herbivores eat. We randomise the list, and everytime they eat, the first
    herb in the list eats and is given a True value. At the end there should be more than one
    herb with a True value.
    """
    l = Lowland(list_herbivores)
    for herb in l.herbivores_pop:
        herb.eaten = False

    for k in range(len(l.herbivores_pop)):
        l.make_herbivores_eat()
        l.herbivores_pop[0].eaten = True

    eaten = 0
    for herb in l.herbivores_pop:
        if herb.eaten:
            eaten += 1

    assert eaten > 1


def test_available_fodder():
    """
    The available fodder should be 800 for lowland
    """
    l = Lowland(population=[{'species': 'Carnivore', 'weight': 50, 'age': 9}])
    l.make_herbivores_eat()
    assert l.available_fodder == 800


def test_consumption_becomes_appetite(list_herbivores):
    """
    When the herbivore has enough fodder the consumption should be the same as the appetite
    """
    l = Lowland(list_herbivores)
    l.make_herbivores_eat()
    for herb in l.herbivores_pop:
        assert herb.F_consumption == herb.p['F']


def test_update_fodder(list_herbivores):
    """
    When a herbivore eats the available fodder should update. When there are six herbivores there
    should be enough fodder for everyone. The updated fodder should then be 800 - 6 * appetite
    """
    l = Lowland(list_herbivores)
    appetite = Herbivore.p['F']
    l.make_herbivores_eat()
    assert l.available_fodder == 800 - len(l.herbivores_pop) * appetite


def test_consumption_when_little_fodder(list_herbivores):
    """
    When there is to little fodder the consumption is not the same as the appetite, but rather
    what is left of the fodder
    """
    l = Lowland(list_herbivores)
    l.p['f_max'] = 8
    l.make_herbivores_eat()
    l.p['f_max'] = 800
    assert l.herbivores_pop[0].F_consumption == 8


def test_fodder_will_stop_at_zero(list_herbivores):
    """
    When there isn't enough fodder the available fodder should stop at 0 after eating and not
    become negative.
    """
    l = Lowland(list_herbivores)
    l.p['f_max'] = 51
    l.make_herbivores_eat()
    #l.p['f_max'] = 800
    assert l.available_fodder == 0


def test_gain_weight_after_eating_herb(list_herbivores):
    """
    After the herbivore eats it should gain weight
    """
    l = Lowland(list_herbivores)
    weight = [k.weight for k in l.herbivores_pop]
    l.make_herbivores_eat()
    weight_after_eating = [k.weight for k in l.herbivores_pop]
    weight.sort()
    weight_after_eating.sort()
    assert [k + 9 for k in weight] == weight_after_eating


def test_fitness_change_after_eating(list_herbivores):
    """
    After the herbivores eats, they should gain weight and therefore have a greater fitness
    """
    l = Lowland(list_herbivores)
    init_fitness = [k.phi for k in l.herbivores_pop]
    l.make_herbivores_eat()
    fitness_after_eating = [k.phi for k in l.herbivores_pop]
    init_fitness.sort()
    fitness_after_eating.sort()
    for k in range(len(l.herbivores_pop)):
        assert init_fitness[k] < fitness_after_eating[k]



# Tests for feed_carnivores_function
def test_carn_appetite(list_herbivores_and_carnivores):
    """
    The carnivores appetite is given as a parameter. It should be 50 before eating
    """
    l = Lowland(list_herbivores_and_carnivores)
    l.feed_carnivores()
    for carn in l.carnivores_pop:
        assert carn.p['F'] == 50


def test_weakest_herb_eaten_first(mocker, list_herbivores_and_carnivores):
    """
    When the carnivores eats, it eats the weakest herbivore first. To check if that happens i
    make sure there are only one carnivore in the cell with appetite equal to the weight of the
    weakest herbivore. After eating we check that the herbivore is no longer in the cell
    """
    mocker.patch('random.random', return_value=0.01)
    l = Lowland(list_herbivores_and_carnivores)
    l.sorting_animals()
    weakest_herb = l.herbivores_pop[0]
    for k in range(len(l.carnivores_pop)):
        l.carnivores_pop[k].p['F'] = weakest_herb.weight + 1
    l.feed_carnivores()
    #for k in range(len(l.carnivores_pop)):
        #l.carnivores_pop[k].p['F'] = 50
    assert weakest_herb not in l.herbivores_pop


def test_strongest_carn_eats_first(mocker):
    """
    When eating the strongest carnivore always eats first. To test this a make sure there are only
    carnivores with a total weight of the carnivores appetite (ie. 50), and make the carnivores eat.
    Later i check that the weight of is the same for all the carnivores, except the fittest.
    """
    mocker.patch('random.random', return_value=0.01)
    population = [{'species': 'Herbivore', 'weight': 25, 'age': 20},
                  {'species': 'Herbivore', 'weight': 25, 'age': 20},
                  {'species': 'Carnivore', 'weight': 50, 'age': 9},
                  {'species': 'Carnivore', 'weight': 70, 'age': 10},
                  {'species': 'Carnivore', 'weight': 10, 'age': 3},
                  {'species': 'Carnivore', 'weight': 90, 'age': 3}]
    l = Lowland(population)
    l.sorting_animals()
    init_weight = [carn.weight for carn in l.carnivores_pop]
    l.feed_carnivores()
    for k in range(1, len(l.carnivores_pop)):
        assert l.carnivores_pop[k].weight == init_weight[k]


def test_eats_until_reaches_appetite(mocker):
    """
    The carnivores does not stop eating until it has eaten herbs with total weight >= appetite.
    To check this I make several carnivores, and enough herbivores for all of them to be full.
    After they eat i check that they have all gained as much weight as they should, which is
    appetite * beta
    """
    mocker.patch('random.random', return_value=0.01)
    population = [{'species': 'Herbivore', 'weight': 23, 'age': 5},
                  {'species': 'Herbivore', 'weight': 23, 'age': 5},
                  {'species': 'Herbivore', 'weight': 23, 'age': 5},
                  {'species': 'Herbivore', 'weight': 23, 'age': 5},
                  {'species': 'Herbivore', 'weight': 23, 'age': 5},
                  {'species': 'Herbivore', 'weight': 23, 'age': 5},
                  {'species': 'Carnivore', 'weight': 100, 'age': 3},
                  {'species': 'Carnivore', 'weight': 100, 'age': 3}]
    l = Lowland(population)
    beta = l.carnivores_pop[0].p['beta']
    appetite = l.carnivores_pop[0].p['F']
    l.sorting_animals()
    init_weight = [carn.weight for carn in l.carnivores_pop]
    l.feed_carnivores()
    for k in range(len(l.carnivores_pop)):
        assert init_weight[k] + appetite * beta <= l.carnivores_pop[k].weight


def test_eats_until_tried_eating_all_the_herbivores(mocker):
    """
    The carnivore eats until it has tried to eat all the herbivores. To test this we create less
    available fodder than there are appetites to see if they are all removed from the list
    """
    mocker.patch('random.random', return_value=0.01)
    population = [{'species': 'Herbivore', 'weight': 23, 'age': 5},
                  {'species': 'Herbivore', 'weight': 23, 'age': 5},
                  {'species': 'Herbivore', 'weight': 23, 'age': 5},
                  {'species': 'Carnivore', 'weight': 100, 'age': 3},
                  {'species': 'Carnivore', 'weight': 100, 'age': 3}]
    l = Lowland(population)
    l.feed_carnivores()
    assert len(l.herbivores_pop) == 0


def test_will_not_eat_stronger_herb(mocker):
    """
    If the herbivore is stronger than the carnivore, the carnivore will not be able to eat. To test
    this the mocker is set very low and we create one strong herbivore and one weak carnivore.
    Later we check if the herbivore is still there
    """
    mocker.patch('random.random', return_value=0.001)
    population = [{'species': 'Herbivore', 'weight': 70, 'age': 5},
                  {'species': 'Carnivore', 'weight': 13, 'age': 5}]
    l = Lowland(population)
    l.feed_carnivores()
    assert len(l.herbivores_pop) != 0


def test_update_fitness_after_eating_carnivores(mocker):
    """
    When a carnivore eats it gains weight, and therefore need to have grater fitness
    """
    mocker.patch('random.random', return_value=0.01)
    population = [{'species': 'Carnivore', 'weight': 70, 'age': 5},
                  {'species': 'Carnivore', 'weight': 80, 'age': 8},
                  {'species': 'Carnivore', 'weight': 90, 'age': 9},
                  {'species': 'Herbivore', 'weight': 25, 'age': 3},
                  {'species': 'Herbivore', 'weight': 25, 'age': 3},
                  {'species': 'Herbivore', 'weight': 25, 'age': 3},
                  {'species': 'Herbivore', 'weight': 25, 'age': 3},
                  {'species': 'Herbivore', 'weight': 25, 'age': 3},
                  {'species': 'Herbivore', 'weight': 25, 'age': 3}]
    l = Lowland(population)
    l.sorting_animals()
    init_fitness = [carn.phi for carn in l.carnivores_pop]
    l.feed_carnivores()
    for k in range(len(l.carnivores_pop)):
        assert l.carnivores_pop[k].phi > init_fitness[k]


# Tests for newborn_animals_function for herbs
def test_newborn_added_to_list_herb(list_herbivore_long):
    """
    When an animal gives birth the newborn must be added to the list. When there are 9 herbivores
    the probability for birth is 1, if the weight is acceptable, and therefore there will be added
    9 herbivores to the list.
    """
    l = Lowland(list_herbivore_long)
    length = len(l.herbivores_pop)
    l.newborn_animals()
    assert len(l.herbivores_pop) == length * 2


def test_mother_lost_weight_herb(list_herbivore_long):
    """
    When an animal gives birth the mother loses weight equivalent to the weight of the
    newborn * zeta. When there are 9 herbivores the probability for birth is 1, if the weight is
    acceptable, and therefore all 9 herbivores will give birth.
    """
    l = Lowland(list_herbivore_long)
    weight = [k.weight for k in l.herbivores_pop]
    l.newborn_animals()
    mothers = l.herbivores_pop[0:9]
    for k in range(len(weight)):
        assert weight[k] > mothers[k].weight


def test_mother_lost_fitness_herb(list_herbivore_long):
    """
    When the mother loses weight, the fitness needs to be updated.
    """
    l = Lowland(list_herbivore_long)
    fitness = [k.phi for k in l.herbivores_pop]
    l.newborn_animals()
    mothers = l.herbivores_pop[0:9]
    for k in range(len(fitness)):
        assert fitness[k] > mothers[k].phi


def test_criteria_for_birth_fitness_herb():
    """
    A criteria for giving birth is that the weight can't be zero, and therefore the fitness can't be
    zero.
    """
    l = Lowland(population=[{'species': 'Herbivore', 'weight': 35, 'age': 5},
                            {'species': 'Herbivore', 'weight': 0, 'age': 8},
                            {'species': 'Herbivore', 'weight': 50, 'age': 9}])
    for k in l.herbivores_pop:
        if k.phi == 0:
            assert k.will_the_animal_give_birth(n=len(l.herbivores_pop)) is False


def test_criteria_for_birth_weight_herb():
    """
    The herbivore cant give birth if it weighs less than zeta*newborn_birth_weight
    """
    l = Lowland(population=[{'species': 'Herbivore', 'weight': 35, 'age': 5},
                            {'species': 'Herbivore', 'weight': 10, 'age': 8},
                            {'species': 'Herbivore', 'weight': 50, 'age': 9}])
    for k in l.herbivores_pop:
        k.birth_probability(n=len(l.herbivores_pop))
        if k.weight <= k.newborn_birth_weight * k.p['zeta']:
            assert k.will_the_animal_give_birth(n=len(l.herbivores_pop)) is False


def test_criteria_for_birth_prob_herb():
    """
    If the criteria for weight and fitness is fulfilled, p = variable.
    variable is gamma * fitness * (N - 1)
    """
    l = Lowland(population=[{'species': 'Herbivore', 'weight': 75, 'age': 5},
                            {'species': 'Herbivore', 'weight': 60, 'age': 8},
                            {'species': 'Herbivore', 'weight': 50, 'age': 9}])
    for k in l.herbivores_pop:
        if k.birth_probability(n=len(l.herbivores_pop)) != 0:
            assert k.birth_probability(n=len(l.herbivores_pop)) == k.p['gamma'] * k.phi * (
                    len(l.herbivores_pop) - 1)


# Tests for newborn_animals for carns
def test_newborn_added_to_list_carn(list_carnivore_long):
    """
    When an animal gives birth the newborn must be added to the list. When there are 9 carnivores
    the probability for birth is 1, if the weight is acceptable, and therefore there will be added
    9 carnivores to the list.
    """
    l = Lowland(list_carnivore_long)
    length = len(l.carnivores_pop)
    l.newborn_animals()
    assert len(l.carnivores_pop) == length * 2


def test_mother_lost_weight_carn(list_carnivore_long):
    """
    When an animal gives birth the mother loses weight equivalent to the weight of the
    newborn * zeta. When there are 9 carnivores the probability for birth is 1, if the weight is
    acceptable, and therefore all 9 carnivores will give birth.
    """
    l = Lowland(list_carnivore_long)
    weight = [k.weight for k in l.carnivores_pop]
    l.newborn_animals()
    mothers = l.carnivores_pop[0:9]
    for k in range(len(weight)):
        assert weight[k] > mothers[k].weight


def test_mother_lost_fitness_carn(list_carnivore_long):
    """
    When the mother loses weight, the fitness needs to be updated.
    """
    l = Lowland(list_carnivore_long)
    fitness = [k.phi for k in l.carnivores_pop]
    l.newborn_animals()
    mothers = l.carnivores_pop[0:9]
    for k in range(len(fitness)):
        assert fitness[k] > mothers[k].phi


def test_criteria_for_birth_fitness_carn():
    """
    A criteria for giving birth is that the weight can't be zero, and therefore the fitness can't be
    zero.
    """
    l = Lowland(population=[{'species': 'Carnivore', 'weight': 35, 'age': 5},
                            {'species': 'Carnivore', 'weight': 0, 'age': 8},
                            {'species': 'Carnivore', 'weight': 50, 'age': 9}])
    for k in l.carnivores_pop:
        if k.phi == 0:
            assert k.will_the_animal_give_birth(n=len(l.carnivores_pop)) is False


def test_criteria_for_birth_weight_carn():
    """
    The herbivore cant give birth if it weighs less than zeta*newborn_birth_weight
    """
    l = Lowland(population=[{'species': 'Carnivore', 'weight': 35, 'age': 5},
                            {'species': 'Carnivore', 'weight': 10, 'age': 8},
                            {'species': 'Carnivore', 'weight': 50, 'age': 9}])
    for k in l.carnivores_pop:
        k.birth_probability(n=len(l.carnivores_pop))
        if k.weight <= k.newborn_birth_weight * k.p['zeta']:
            assert k.will_the_animal_give_birth(n=len(l.carnivores_pop)) is False


def test_criteria_for_birth_prob_carn():
    """
    If the criteria for weight and fitness is fulfilled, p = variable.
    variable is gamma * fitness * (N - 1). If variable > 1, p = 1
    """
    l = Lowland(population=[{'species': 'Carnivore', 'weight': 75, 'age': 5},
                            {'species': 'Carnivore', 'weight': 60, 'age': 8},
                            {'species': 'Carnivore', 'weight': 50, 'age': 9}])
    for k in l.carnivores_pop:
        if k.birth_probability(n=len(l.carnivores_pop)) != 0:
            if k.p['gamma'] * k.phi * (len(l.carnivores_pop) - 1) < 1:
                assert k.birth_probability(n=len(l.carnivores_pop)) == k.p['gamma'] * k.phi * (
                        len(l.carnivores_pop) - 1)
            else:
                assert k.birth_probability(n=len(l.carnivores_pop)) == 1


# Tests for move_animals_from_cell:
def test_herbs_removed_from_list(mocker, list_herbivore_long):
    """
    The animal will move with a probability, when choosing mocker for 0.1 there will definitely some
    animals moving
    """
    mocker.patch('random.random', return_value=0.1)
    l = Lowland(list_herbivore_long)
    length = len(l.herbivores_pop)
    l.move_animals_from_cell()
    assert len(l.herbs_move) == length


def test_carns_removed_from_list(mocker, list_carnivore_long):
    """
    The animal will move with a probability, when choosing mocker for 0.1 there will definitely some
    animals moving
    """
    mocker.patch('random.random', return_value=0.1)
    l = Lowland(list_carnivore_long)
    length = len(l.carnivores_pop)
    l.move_animals_from_cell()
    assert len(l.carns_move) == length


def test_total_moving_animals(mocker, list_carnivore_long, list_herbivore_long):
    """
    The move_animal_from_cell function returns a list with one list for moving herbivores and one
    list for moving carnivores
    """
    mocker.patch('random.random', return_value=0.1)
    l = Lowland(list_herbivore_long + list_carnivore_long)
    total_moving = l.move_animals_from_cell()
    assert len(total_moving[0]) == len(l.herbivores_pop)
    assert len(total_moving[1]) == len(l.carnivores_pop)


# Tests for reset_already_moved:
def test_reset_already_moved_herb(list_carnivore_long, list_herbivore_long):
    """
    After moving, animal.already_moved should be True, so they don't move again from the new cell
    in the same year
    """
    l = Lowland(list_herbivore_long + list_carnivore_long)
    total_moving = l.move_animals_from_cell()

    for herb in total_moving[0]:
        assert herb.already_moved is True


def test_reset_already_moved_carn(list_carnivore_long, list_herbivore_long):
    """
    After moving, animal.already_moved should be True, so they don't move again from the new cell
    in the same year
    """
    l = Lowland(list_herbivore_long + list_carnivore_long)
    total_moving = l.move_animals_from_cell()
    for carn in total_moving[1]:
        assert carn.already_moved is True


def test_reset_already_moved(list_carnivore_long, list_herbivore_long):
    """
    Every year we must reset already moved so that they can move again
    """
    l = Lowland(list_herbivore_long + list_carnivore_long)
    l.move_animals_from_cell()
    l.reset_already_moved()
    for herb in l.carnivores_pop:
        assert herb.already_moved is False


# Tests for counting_animals function
def test_count_animals_herb():
    """
    We test if the counting_animals function give the same results as len()
    """
    l = Lowland(population=[{'species': 'Herbivore', 'weight': 35, 'age': 5},
                            {'species': 'Herbivore', 'weight': 41, 'age': 8},
                            {'species': 'Herbivore', 'weight': 50, 'age': 9}])
    l.counting_animals()
    assert l.N_herb == len(l.herbivores_pop)


def test_count_animals_carn():
    """
    We test if the counting_animals function give the same results as len()
    """
    l = Lowland(population=[{'species': 'Carnivore', 'weight': 35, 'age': 5},
                            {'species': 'Carnivore', 'weight': 41, 'age': 8},
                            {'species': 'Carnivore', 'weight': 50, 'age': 9}])
    l.counting_animals()
    assert l.N_carn == len(l.carnivores_pop)


# Tests for make_animals_age function
def test_aging_herb():
    """
    The animals age each year
    """
    l = Lowland(population=[{'species': 'Herbivore', 'weight': 35, 'age': 5},
                            {'species': 'Herbivore', 'weight': 41, 'age': 8},
                            {'species': 'Herbivore', 'weight': 50, 'age': 9}])
    init_age = [ani.age for ani in l.herbivores_pop]
    l.make_animals_age()
    for k in range(len(l.herbivores_pop)):
        assert l.herbivores_pop[k].age == init_age[k] + 1


def test_fitness_when_aging_herb():
    """
    when an animal age, we must update the fitness
    """
    l = Lowland(population=[{'species': 'Herbivore', 'weight': 35, 'age': 5},
                            {'species': 'Herbivore', 'weight': 41, 'age': 8},
                            {'species': 'Herbivore', 'weight': 50, 'age': 9}])
    init_fitness = [ani.phi for ani in l.herbivores_pop]
    l.make_animals_age()
    for k in range(len(l.herbivores_pop)):
        assert l.herbivores_pop[k].phi < init_fitness[k]


def test_aging_carn():
    """
    The animals age each year
    """
    l = Lowland(population=[{'species': 'Carnivore', 'weight': 35, 'age': 5},
                            {'species': 'Carnivore', 'weight': 41, 'age': 8},
                            {'species': 'Carnivore', 'weight': 50, 'age': 9}])
    init_age = [ani.age for ani in l.carnivores_pop]
    l.make_animals_age()
    for k in range(len(l.carnivores_pop)):
        assert l.carnivores_pop[k].age == init_age[k] + 1


def test_fitness_when_aging_carn():
    """
    when an animal age, we must update the fitness
    """
    l = Lowland(population=[{'species': 'Carnivore', 'weight': 35, 'age': 5},
                            {'species': 'Carnivore', 'weight': 41, 'age': 8},
                            {'species': 'Carnivore', 'weight': 50, 'age': 9}])
    init_fitness = [ani.phi for ani in l.carnivores_pop]
    l.make_animals_age()
    for k in range(len(l.carnivores_pop)):
        assert l.carnivores_pop[k].phi < init_fitness[k]


# Tests for make_animals_lose_weight:
def test_yearly_weight_loss_herb():
    """
    Every year the animal loses weight equivalent to current weight times eta
    """
    l = Lowland(population=[{'species': 'Herbivore', 'weight': 35, 'age': 5},
                            {'species': 'Herbivore', 'weight': 41, 'age': 8},
                            {'species': 'Herbivore', 'weight': 50, 'age': 9}])

    init_weight = [animal.weight for animal in l.herbivores_pop]
    l.make_animals_lose_weight()
    for k in range(len(l.herbivores_pop)):
        assert l.herbivores_pop[k].weight == init_weight[k] - Herbivore.p['eta'] * init_weight[k]


def test_update_fitness_during_weight_loss_herb():
    """
    Every year the animal loses weight and therefore must update the fitness. It becomes less
    than the initial fitness.
    """
    l = Lowland(population=[{'species': 'Herbivore', 'weight': 35, 'age': 5},
                            {'species': 'Herbivore', 'weight': 41, 'age': 8},
                            {'species': 'Herbivore', 'weight': 50, 'age': 9}])
    init_fitness = [animal.phi for animal in l.herbivores_pop]
    l.make_animals_lose_weight()
    for k in range(len(init_fitness)):
        assert l.herbivores_pop[k].phi < init_fitness[k]


def test_yearly_weight_loss_carn():
    """
    Every year the animal loses weight equivalent to current weight times eta
    """
    l = Lowland(population=[{'species': 'Carnivore', 'weight': 35, 'age': 5},
                            {'species': 'Carnivore', 'weight': 41, 'age': 8},
                            {'species': 'Carnivore', 'weight': 50, 'age': 9}])

    init_weight = [animal.weight for animal in l.carnivores_pop]
    l.make_animals_lose_weight()
    for k in range(len(l.carnivores_pop)):
        assert l.carnivores_pop[k].weight == init_weight[k] - Carnivore.p['eta'] * init_weight[k]


def test_update_fitness_during_weight_loss_carn():
    """
    Every year the animal loses weight and therefore must update the fitness. It becomes less
    than the initial fitness.
    """
    l = Lowland(population=[{'species': 'Carnivore', 'weight': 35, 'age': 5},
                            {'species': 'Carnivore', 'weight': 41, 'age': 8},
                            {'species': 'Carnivore', 'weight': 50, 'age': 9}])
    init_fitness = [animal.phi for animal in l.carnivores_pop]
    l.make_animals_lose_weight()
    for k in range(len(init_fitness)):
        assert l.carnivores_pop[k].phi < init_fitness[k]


# Tests for dead_animals_natural_cause:
def test_animal_removed_after_death_when_true_herb():
    """
    Each year we must check if animals die. If weight = 0 the probability for dying is 0.
    Therefore the length of the list will be less than the initial length.
    """
    l = Lowland(population=[{'species': 'Herbivore', 'weight': 5, 'age': 60},
                            {'species': 'Herbivore', 'weight': 41, 'age': 8},
                            {'species': 'Herbivore', 'weight': 0, 'age': 9}])
    init_length = len(l.herbivores_pop)
    l.dead_animals_natural_cause()
    assert len(l.herbivores_pop) < init_length


def test_animal_removed_after_death_when_true_carn():
    """
    Each year we must check if animals die. If weight = 0 the probability for dying is 0.
    Therefore the length of the list will be less than the initial length.
    """
    population = [{'species': 'Carnivore', 'weight': 35, 'age': 5},
                  {'species': 'Carnivore', 'weight': 0, 'age': 8},
                  {'species': 'Carnivore', 'weight': 50, 'age': 9}]
    l = Lowland(population)
    init_length = len(l.carnivores_pop)
    l.dead_animals_natural_cause()
    assert len(l.carnivores_pop) < init_length


def test_animal_removed_after_death_when_false_herb(mocker):
    """
    If the random number is less than the probability for dying, no animal should be removed from
    the list. None of the animals in the list lays grounds for p=1
    """
    mocker.patch('random.random', return_value=1)
    l = Lowland(population=[{'species': 'Herbivore', 'weight': 5, 'age': 60},
                            {'species': 'Herbivore', 'weight': 41, 'age': 8},
                            {'species': 'Herbivore', 'weight': 8, 'age': 9}])
    init_length = len(l.herbivores_pop)
    l.dead_animals_natural_cause()
    assert len(l.herbivores_pop) == init_length


def test_animal_removed_after_death_when_false_carn(mocker):
    """
    If the random number is less than the probability for dying, no animal should be removed from
    the list. None of the animals in the list lays grounds for p=1
    """
    mocker.patch('random.random', return_value=1)
    population = [{'species': 'Carnivore', 'weight': 35, 'age': 5},
                  {'species': 'Carnivore', 'weight': 10, 'age': 8},
                  {'species': 'Carnivore', 'weight': 50, 'age': 9}]
    l = Lowland(population)
    init_length = len(l.carnivores_pop)
    l.dead_animals_natural_cause()
    assert len(l.carnivores_pop) == init_length
