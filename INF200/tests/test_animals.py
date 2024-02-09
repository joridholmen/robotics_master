# -*- encoding: utf-8 -*-

"""
"""

__author__ = 'Christianie Torres'
__email__ = 'christianie.torres@nmbu.no'

from biosim.Animals import Herbivore, Carnivore
import pytest


@pytest.fixture
def age5_weight20():
    return {'age': 5, 'weight': 20}


@pytest.fixture
def age10_weight40():
    return {'age': 10, 'weight': 40}


# Tests for initial value:
def test_parameters_herb(age5_weight20):
    """
    Checking if the correct parameters for herbivores is given
    It is given that the w_birth is 8.0 for herbivores
    """
    with pytest.raises(ValueError):
        p = {
            "w_birth": -6.0,
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
        h = Herbivore(age5_weight20)
        h.set_given_parameters(p)


def test_parameters_carn(age10_weight40):
    """
    Checking if the correct parameters for carnivores is given
    It is given that the w_birth is 6.0 for carnivores
    """
    h = Carnivore(age10_weight40)
    assert h.p['w_birth'] == 6.0


def test_herbivore_age(age5_weight20):
    """
    The herbivore shall be given an age when it is created
    It is given age = 5
    """
    h = Herbivore(age5_weight20)
    assert h.age == 5


def test_carnivore_age(age10_weight40):
    """
    The herbivore shall be given an age when it is created
    It is given age = 10
    """
    c = Carnivore(age10_weight40)
    assert c.age == 10


def test_herbivore_weight(age5_weight20):
    """
    The herbivore shall be given an weight when it is created
    It is given weight = 20
    """
    h = Herbivore(age5_weight20)
    assert h.weight == 20


def test_carnivore_weight(age10_weight40):
    """
    The carnivore shall be given an weight when it is created
    It is given weight = 40
    """
    c = Carnivore(age10_weight40)
    assert c.weight == 40


def test_herb_given_fitness(age5_weight20):
    """
    When a herbivore is created the fitness is automatically updated
    """
    h = Herbivore(age5_weight20)
    assert h.phi is not None


def test_carn_given_fitness(age10_weight40):
    """
    When a carnivore is created the fitness is automatically updated
    """
    c = Carnivore(age10_weight40)
    assert c.phi is not None


# Tests for aging function
def test_herbivore_aging():
    """
    A herbivore ages each year, and there are therefore created a function for it
    The herbivore has age = 0, each year it ages and the age should be year + 1
    """
    h = Herbivore({'age': 0, 'weight': 20})
    for year in range(10):
        h.aging()
        assert h.age == year + 1


def test_carnivore_aging():
    """
    A carnivore ages each year, and there are therefore created a function for it
    The carnivore has age = 0, each year it ages and the age should be year + 1
    """
    c = Carnivore({'age': 0, 'weight': 20})
    for year in range(10):
        c.aging()
        assert c.age == year + 1


def test_update_fitness_when_aging_herb(age5_weight20):
    """
    When a herbivore ages the fitness changes, since age is used to calculate fitness
    First the initial fitness is saved in init_phi, and compared with the new fitness after aging
    The initial fitness should ble slightly greater than the new fitness
    """
    h = Herbivore(age5_weight20)
    init_phi = h.phi
    h.aging()
    assert h.phi < init_phi


def test_update_fitness_when_aging_carn(age10_weight40):
    """
    When a carnivore ages the fitness changes, since age is used to calculate fitness
    First the initial fitness is saved in init_phi, and compared with the new fitness after aging
    The initial fitness should ble slightly greater than the new fitness
    """
    c = Carnivore(age10_weight40)
    init_phi = c.phi
    c.aging()
    assert c.phi < init_phi


# Tests for birth_weight_function:
def test_birth_weight_function_herb(age5_weight20):
    """
    When a new herbivore is born it needs to be given a weight
    The newborns weight is calculated with the birth_weight_function function
    To use this function the newborn has to be given a mother, which is h
    """
    h = Herbivore(age5_weight20)
    newborn = Herbivore({'age': 0, 'weight': h.birth_weight_function()})
    assert newborn.weight is not None


def test_birth_weight_function_carn(age10_weight40):
    """
    When a new carnivore is born it needs to be given a weight
    The newborns weight is calculated with the birth_weight_function function
    To use this function the newborn has to be given a mother, which is c
    """
    c = Carnivore(age10_weight40)
    newborn = Herbivore({'age': 0, 'weight': c.birth_weight_function()})
    assert newborn.weight is not None


# Tests for weight_loss function:
def test_herbivore_weight_loss(age5_weight20):
    """
    The herbivore loses weight each year.
    The weight loss is equivalent to the initial weight times eta = 0.05
    """
    h = Herbivore(age5_weight20)
    initial_weight = h.weight
    eta = h.p['eta']
    h.weight_loss()
    assert h.weight == initial_weight - initial_weight * eta


def test_carnivore_weight_loss(age10_weight40):
    """
    The carnivore loses weight each year.
    The weight loss is equivalent to the initial weight times eta = 0.125
    """
    c = Carnivore(age10_weight40)
    initial_weight = c.weight
    eta = c.p['eta']
    c.weight_loss()
    assert c.weight == initial_weight - initial_weight * eta


def test_update_fitness_during_weight_loss_herb(age5_weight20):
    """
    When the herbivore loses weight the fitness must be updates.
    It is updated in the weight_loss function.
    The initial fitness should be greater than the new fitness.
    """
    h = Herbivore(age5_weight20)
    init_phi = h.phi
    h.weight_loss()
    assert h.phi < init_phi


def test_update_fitness_during_weight_loss_carn(age10_weight40):
    """
    When the carnivore loses weight the fitness must be updates.
    It is updated in the weight_loss function.
    The initial fitness should be greater than the new fitness.
    """
    c = Carnivore(age10_weight40)
    init_phi = c.phi
    c.weight_loss()
    assert c.phi < init_phi


# Tests for weight_gain function:
def test_weight_gain_herb(age5_weight20):
    """
    When the herbivore eats it gains weight.
    Before it eats we save the initial weight in init_weight.
    We use the weight_gain function to calculate the new weight, where the input is the amount
    it eats. For convenience the amount it eats is the same as the appetite.
    """
    h = Herbivore(age5_weight20)
    init_weight = h.weight
    beta = h.p['beta']
    F = h.p['F']
    new_weight = init_weight + beta * F  # for comparing with the weight given in the function
    h.weight_gain(consumption=F)
    assert h.weight == new_weight


def test_weight_gain_carn(age10_weight40):
    """
    When the carnivore eats it gains weight.
    Before it eats we save the initial weight in init_weight.
    We use the weight_gain function to calculate the new weight, where the input is the amount
    it eats. For convenience the amount it eats is the same as the appetite.
    """
    c = Carnivore(age10_weight40)
    init_weight = c.weight
    beta = c.p['beta']
    F = c.p['F']
    new_weight = init_weight + beta * F  # for comparing with the weight given in the function
    c.weight_gain(consumption=F)
    assert c.weight == new_weight


def test_updated_fitness_during_weight_gain_herb(age5_weight20):
    """
    When the herbivore gains weight the fitness must be updates.
    It is updated in the weight_gain function.
    The initial fitness should be lower than the new fitness.
    """
    h = Herbivore(age5_weight20)
    init_phi = h.phi
    h.weight_gain(consumption=h.p['F'])
    assert h.phi > init_phi


def test_updated_fitness_during_weight_gain_carn(age10_weight40):
    """
    When the carnivore gains weight the fitness must be updates.
    It is updated in the weight_gain function.
    The initial fitness should be lower than the new fitness.
    """
    c = Carnivore(age10_weight40)
    init_phi = c.phi
    c.weight_gain(consumption=c.p['F'])
    assert c.phi > init_phi


# Tests for fitness function:
def test_valid_fitness_herb():
    """
    The phi-value should be between 0 and 1.
    To test this we calculate the fitness for several herbivores
    """
    for age in range(0, 50):
        for weight in range(10, 60):
            h = Herbivore({'age': age, 'weight': weight})
            assert 0 <= h.phi <= 1


def test_valid_fitness_carn():
    """
    The phi-value should be between 0 and zero.
    To test this we calculate the fitness for several carnivores
    """
    for age in range(0, 50):
        for weight in range(10, 60):
            c = Carnivore({'age': age, 'weight': weight})
            assert 0 <= c.phi <= 1


def test_fitness_when_weight_is_zero():
    """
    When the weight = 0, the fitness should be zero
    """
    h = Herbivore({'age': 5, 'weight': 0})
    assert h.phi == 0


# Tests for birth_probability function:
def test_no_newborn_when_mother_weighs_too_little_herb(age5_weight20):
    """
    If the mother weighs less than zeta * (w_birth + sigma_birth) the birth will not take place
    For herbivores: zeta * (w_birth * sigma_birth) = 3.5 * (8 - 1.5) = 22.75
    For the test we use weight = 20, since 20 < 22.75
    The input in birth_probability is how many herbivores in the cell.
    """
    h = Herbivore(age5_weight20)
    assert h.birth_probability(n=3) == 0


def test_no_newborn_when_mother_weighs_too_little_carn():
    """
    If the mother weighs less than zeta * (w_birth + sigma_birth) the birth will not take place
    For carnivores: zeta * (w_birth * sigma_birth) = 3.5 * (6 - 1) = 17.5
    For the test we use weight = 15, since 15 < 17.5
    The input in birth_probability is how many carnivores in the cell.
    """
    c = Carnivore({'age': 10, 'weight': 15})
    assert c.birth_probability(n=3) == 0


def test_no_newborn_if_mother_weighs_less_than_newborn_times_zeta_herb(age5_weight20):
    """
    There will be no birth if the mother weighs less than the newborn times zeta.
    If we run the birth_probability function 50 times, the mother will weigh less at least once
    """
    h = Herbivore(age5_weight20)
    for k in range(50):
        h.birth_probability(n=10)
        if h.weight < h.newborn_birth_weight * h.p['zeta']:
            assert h.birth_probability(n=10) == 0


def test_no_newborn_if_mother_weighs_less_than_newborn_times_zeta_carn(age5_weight20):
    """
    There will be no birth if the mother weighs less than the newborn times zeta.
    If we run the birth_probability function 50 times, the mother will weigh less at least once
    """
    c = Carnivore(age5_weight20)
    for k in range(50):
        c.birth_probability(n=10)
        if c.weight < c.newborn_birth_weight * c.p['zeta']:
            assert c.birth_probability(n=10) == 0


def test_correct_newborn_prob_herb():
    """
    If the mother weighs enough the probability will be a variable or 1, whichever is less.
    The variable is gamma * fitness (N - 1), where N is the amount of herb in the cell.
    To check if it works for p = variable and p = 1, we test for N from 2-20
    """
    h = Herbivore({'age': 5, 'weight': 50})
    gamma = h.p['gamma']
    fitness = h.phi
    for N in range(2, 20):
        if gamma * fitness * (N - 1) > 1:
            assert h.birth_probability(N) == 1
        else:
            assert h.birth_probability(N) == gamma * fitness * (N - 1)


def test_correct_newborn_prob_carn():
    """
    If the mother weighs enough the probability will be a variable or 1, whichever is less.
    The variable is gamma * fitness (N - 1), where N is the amount of carnivores in the cell.
    To check if it works for p = variable and p = 1, we test for N from 2-20
    """
    c = Carnivore({'age': 10, 'weight': 50})
    gamma = c.p['gamma']
    fitness = c.phi
    for N in range(2, 20):
        if gamma * fitness * (N - 1) > 1:
            assert c.birth_probability(N) == 1
        else:
            assert c.birth_probability(N) == gamma * fitness * (N - 1)


def test_no_birth_when_too_few_herbs():
    """
    The herbivores can't procreate if there are only one herbivore
    """
    h = Herbivore({'age': 5, 'weight': 50})
    assert h.birth_probability(n=1) == 0


def test_no_birth_when_too_few_carns():
    """
    The carnivores can't procreate if there are only one carnivore
    """
    c = Carnivore({'age': 10, 'weight': 50})
    assert c.birth_probability(n=1) == 0


# Tests for will_the_animal_give_birth_function:
def test_will_the_animal_give_birth_correct_return_herb():
    """
    If the birth_probability returns 1 the will_the_animal_give_birth function will return True.
    The birth_probability=1 if N=10
    """
    h = Herbivore({'age': 5, 'weight': 50})
    N = 10
    for _ in range(10):
        assert h.will_the_animal_give_birth(N) is True


def test_will_the_animal_give_birth_correct_return_carn():
    """
    If the birth_probability returns 1 the will_the_animal_give_birth function will return True.
    The birth_probability=1 if N=10
    """
    c = Carnivore({'age': 10, 'weight': 50})
    N = 10
    for _ in range(10):
        assert c.will_the_animal_give_birth(N) is True


def test_will_the_animal_give_birth_return_false_carn():
    """
    If the birth_probability=0 the will_the_animal_give_birth function should return False.
    birth_probability=0 happens eg. when N=1
    """
    c = Carnivore({'age': 10, 'weight': 50})
    N = 1
    for _ in range(10):
        assert c.will_the_animal_give_birth(N) is False


# Tests for birth_weight_loss function
def test_birth_weight_loss_herb():
    """
    If the birth_probability returns 1 and will_the_animal_give_birth is True, the mother should
    lose weight.
    She loses zeta times the weight of the newborn. The weight is calculated in birth_probability
    which we use in will_the_animal_give_birth
    """
    h = Herbivore({'age': 5, 'weight': 50})
    weight_mother = h.weight
    zeta = h.p['zeta']
    h.will_the_animal_give_birth(n=10)
    h.birth_weight_loss(h.newborn_birth_weight)
    assert h.weight == weight_mother - zeta * h.newborn_birth_weight


def test_birth_weight_loss_carn():
    """
    If the birth_probability returns 1 and will_the_animal_give_birth is True, the mother should
    lose weight.
    She loses zeta times the weight of the newborn. The weight is calculated in birth_probability
    which we use in will_the_animal_give_birth
    """
    c = Herbivore({'age': 10, 'weight': 50})
    weight_mother = c.weight
    zeta = c.p['zeta']
    c.will_the_animal_give_birth(n=10)
    c.birth_weight_loss(c.newborn_birth_weight)
    assert c.weight == weight_mother - zeta * c.newborn_birth_weight


def test_fitness_after_birth_herb():
    """
    When the herbivore loses weight after birth the fitness should be less
    """
    h = Herbivore({'age': 5, 'weight': 50})
    fitness_mother = h.phi
    h.will_the_animal_give_birth(n=10)
    h.birth_weight_loss(h.newborn_birth_weight)
    assert h.phi < fitness_mother


# Tests for death_probability function
def test_return_1_when_phi_zero_herb():
    """
    When the fitness of a herbivore is zero the animal will definitely die. When a herbivore dies
    death_probability = 1. The fitness=0 if the weight of the herbivore is zero
    """
    h = Herbivore({'age': 5, 'weight': 0})
    assert h.death_probability() == 1


def test_return_1_when_phi_zero_carn():
    """
    When the fitness of a carnivore is zero the animal will definitely die. When a carnivore dies
    death_probability = 1. The fitness=0 if the weight of the carnivore is zero
    """
    c = Carnivore({'age': 10, 'weight': 0})
    assert c.death_probability() == 1


def test_return_correct_death_probability_herb():
    """
    If the fitness is not 0, p = omega * (1 - fitness)
    """
    h = Herbivore({'age': 5, 'weight': 50})
    omega = h.p['omega']
    fitness = h.phi
    assert h.death_probability() == omega * (1 - fitness)


def test_return_correct_death_probability_carn():
    """
    If the fitness is not 0, p = omega * (1 - fitness)
    """
    c = Carnivore({'age': 10, 'weight': 50})
    omega = c.p['omega']
    fitness = c.phi
    assert c.death_probability() == omega * (1 - fitness)


# Tests for will_the_animal_die_function:
def test_will_the_animal_die_herb(mocker):
    """
    When finding out if a herbivore will die or not, we get a random number and if it's less than
    p, will_the_animal_die = True. If not it returns False.
    If the animal weighs 10, p will be approximately 0.2 and therefore I use mocker to make the
    random number 0.1
    """
    mocker.patch('random.random', return_value=0.1)
    h = Herbivore({'age': 5, 'weight': 10})
    for _ in range(50):
        assert h.will_the_animal_die() is True


def test_will_the_animal_die_carn(mocker):
    """
    When finding out if a carnivore will die or not, we get a random number and if it's less than
    p, will_the_animal_die = True. If not it returns False.
    If the animal weighs 10, p will be approximately 0.321 and therefore I use mocker to make the
    random number 0.1
    """
    mocker.patch('random.random', return_value=0.1)
    c = Carnivore({'age': 10, 'weight': 5})
    for _ in range(50):
        assert c.will_the_animal_die() is True


# Tests for move_move_single_animal function
def test_will_animal_move_herb(mocker):
    """
    The probability of a animal moving is mu * fitness. In the function we draw a random number. If
    the random number is less than the probability the animal will move. In addition the animal
    can't have moved earlier that year and the variable already_moved must be false.
    When the animal weighs 50 and has age 5, p = 0.2455.
    """
    mocker.patch('random.random', return_value=0.1)
    h = Herbivore({'age': 5, 'weight': 50})
    h.already_moved = False
    for _ in range(20):
        assert h.move_single_animal() is True


def test_will_animal_move_carn(mocker):
    """
    The probability of a animal moving is mu * fitness. In the function we draw a random number. If
    the random number is less than the probability the animal will move. In addition the animal
    can't have moved earlier that year and the variable already_moved must be false.
    When the animal weighs 50 and has age 10, p = 0.4.
    """
    mocker.patch('random.random', return_value=0.1)
    c = Carnivore({'age': 10, 'weight': 50})
    c.already_moved = False
    for _ in range(20):
        assert c.move_single_animal() is True


def test_already_moved(mocker):
    """
    if the animal has already moved, move=False
    """
    mocker.patch('random.random', return_value=0.1)
    c = Carnivore({'age': 10, 'weight': 50})
    c.already_moved = True
    for _ in range(20):
        c.move_single_animal()
        assert c.move_single_animal() is False


# Tests for eat_fodder function
def test_consumption():
    """
    If the available fodder in the cell is greater than the appetite, f_consumption should be
    the same as the appetite.
    """
    h = Herbivore({'age': 5, 'weight': 50})
    h.eat_fodder(F_cell=800)
    assert h.F_consumption == h.p['F']


def test_negative_consumption():
    """
    The herbivore should stop eating if there is no more available fodder. Therefore there
    the eat_fodder function should give an error if the fodder is negative
    """
    with pytest.raises(ValueError):
        h = Herbivore({'age': 5, 'weight': 50})
        h.eat_fodder(F_cell=-10)


def test_to_little_fodder():
    """
    If there is not enough fodder in the cell, F_consumption should be the same as the available
    fodder
    """
    h = Herbivore({'age': 5, 'weight': 50})
    F_cell = 2
    h.eat_fodder(F_cell)
    assert h.F_consumption == F_cell


def test_weight_gain_when_after_eat_fodder():
    """
    When the herbivore eats, it should gain weight = consumption * beta
    """
    h = Herbivore({'age': 5, 'weight': 50})
    init_weight = h.weight
    beta = h.p['beta']
    h.eat_fodder(F_cell=800)
    assert h.weight == init_weight + beta * h.F_consumption


def test_fitness_after_eating():
    """
    When the herbivore gains weight after eating the fitness should be greater
    """
    h = Herbivore({'age': 5, 'weight': 50})
    init_fitness = h.phi
    h.eat_fodder(F_cell=800)
    assert h.phi > init_fitness


# Tests for probability_kill_herbivore:
def test_kill_probability_zero_when_bad_fitness():
    """
    If the carnivore has worse fitness than the herbivore it tries to eat, the probability of
    killing is zero.
    """
    h = Herbivore({'age': 5, 'weight': 40})
    c = Carnivore({'age': 10, 'weight': 10})
    assert c.probability_kill_herbivore(h) == 0


def test_probability_kill_better_fitness():
    """
    When the carnivores fitness is greater than the herbivores fitness the probability for killing
    is (carn.fitness-herb_fitness)/DeltaPhiMax
    """
    h = Herbivore({'age': 5, 'weight': 40})
    c = Carnivore({'age': 10, 'weight': 50})
    assert c.probability_kill_herbivore(h) == (c.phi - h.phi) / c.p['DeltaPhiMax']


# Tests for will carn kill
def test_will_carn_kill_true(mocker):
    """
    Probability_kill returns p. In will_carn_kill we generate a random number, and if its less than
    p the carnivore will kill, and the function returns True.
    """
    mocker.patch('random.random', return_value=0.01)
    h = Herbivore({'age': 5, 'weight': 10})
    c = Carnivore({'age': 10, 'weight': 70})
    assert c.will_carn_kill(h) is True


def test_will_carn_kill_false():
    """
    If p = 0, will_carn_kill returns False
    """
    h = Herbivore({'age': 5, 'weight': 40})
    c = Carnivore({'age': 10, 'weight': 30})
    for _ in range(50):
        assert c.will_carn_kill(h) is False


# Tests for weight_gain_after_eating_herb
def test_weight_gain_after_eating_herb():
    """
    After the carnivore eats a herbivore it will gain weight. It gains consumption * beta.
    The consumption is the weight of the eaten herbivore
    """
    h = Herbivore({'age': 5, 'weight': 40})
    c = Carnivore({'age': 10, 'weight': 70})
    init_weight_carn = c.weight
    weight_herb = h.weight
    beta = c.p['beta']
    c.weight_gain_after_eating_herb(h)
    assert c.weight == init_weight_carn + beta * weight_herb


def test_fitness_after_eating_herb():
    """
    When the carnivore gains weight after eating the herb, the fitness should also be greater
    """
    h = Herbivore({'age': 5, 'weight': 40})
    c = Carnivore({'age': 10, 'weight': 70})
    init_fitness_carn = c.phi
    c.weight_gain_after_eating_herb(h)
    assert init_fitness_carn < c.phi
