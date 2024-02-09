import unittest
import pytest
from biosim.Animals import Herbivore, Carnivore
from biosim.Cell import Lowland, Highland, Desert, Water
from biosim.MapIsland import Map_Island

if __name__ == '__main__':
    unittest.main()


@pytest.fixture
def island1():
    island_geo = """\
                    WWW
                    WLW
                    WWW"""
    init_pop = [{'loc': (2, 2),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(50)]}]
    return Map_Island(island_geo, init_pop)


# tests for checking_island_boundaries function
def test_checking_island_boundaries():
    """
    In order for the simulation to work the boundaries must be water. The checking island_boundaries
    function gives an error if the boundaries is not water
    """
    with pytest.raises(ValueError):
        island_geo = """\
                        WWW
                        WLW
                        WWL"""
        init_pop = [{'loc': (2, 2),
                     'pop': [{'species': 'Herbivore',
                              'age': 5,
                              'weight': 20}
                             for _ in range(50)]}]
        m = Map_Island(island_geo, init_pop)
        m.check_island_boundaries()


# Tests for check_for_equal_map_lines function
def test_check_for_equal_map_lines():
    """
    All the lines in the map should have equal length
    """
    with pytest.raises(ValueError):
        island_geo = """\
                        WWW
                        WLW
                        WW"""
        init_pop = [{'loc': (2, 2),
                     'pop': [{'species': 'Herbivore',
                              'age': 5,
                              'weight': 20}
                             for _ in range(50)]}]
        m = Map_Island(island_geo, init_pop)
        m.check_for_equal_map_lines()


# Tests for create_geography_dict function
def test_geography_dict1():
    """
        Testing if each coordinate receives a letter
        """
    island_geo = """\
                    WWW
                    WLW
                    WWW"""
    m = Map_Island(island_geo, init_pop=[])
    m.check_island_boundaries()
    m.check_for_equal_map_lines()
    m.create_geography_dict()
    for x in range(1, 3):
        for y in range(1, 3):
            assert m.geography[(x, y)] == 'W' or 'L'


def test_geography_dict2():
    """
    Testing to see if Lowland receives correct coordinates
    """
    island_geo = """\
                    WWW
                    WLW
                    WWW"""
    m = Map_Island(island_geo, init_pop=[])
    m.create_geography_dict()
    assert m.geography[(2, 2)] == 'L'


# Tests for create_population_dict function
def test_population_dict(island1):
    """
        The coordinate 2,2 should receive a population, where all of them have age=5
        """
    m = island1
    m.check_island_boundaries()
    m.check_for_equal_map_lines()
    m.create_population_dict()
    for animal in m.population[(2, 2)]:
        assert animal["age"] == 5


# Tests for add_population function
def test_add_population():
    """
    We first simulate herbivores, and later we add carnivores. We need a function for adding the
    carnivores later, that we call add_population. To tests that this function work we check that
    the population has a list called carnivores_pop
    """
    geogr = """\
                WWW
                WLW
                WWW"""
    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]
    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 60}
                          for _ in range(20)]}]
    m = Map_Island(island_geo=geogr, init_pop=ini_herbs)
    m.create_map_dict()
    m.add_population(ini_carns)
    for loc, cell in m.map.items():
        if cell.habitable == True:
            assert len(cell.carnivores_pop) == 20

def test_add_population_age():
    """
    If add_population works correctly the age of all the carnivores should be 5
    """
    geogr = """\
                WWW
                WLW
                WWW"""
    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]
    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 60}
                          for _ in range(20)]}]
    m = Map_Island(island_geo=geogr, init_pop=ini_herbs)
    m.create_map_dict()
    m.add_population(ini_carns)
    for carn in m.map[(2, 2)].carnivores_pop:
        assert carn.age == 5


# Tests for create_map_dict
def test_create_map_dict(island1):
    """
    Create_map_dict takes in population and geography dictionaries and creates a new dictionary of
    the entire map.
    To test if it receives the correct population we compare it to the length of the population
    dictionary
    In island1 the herbivores are in coordinates (2,2)
    """
    m = island1
    m.create_map_dict()
    assert len(m.population[(2, 2)]) == len(m.map[(2, 2)].herbivores_pop)


# Tests for neighbours_of_current_cell function
def test_neighbours_of_current_cell1(island1):
    """
    neighbours_of_current_cell  is given the current coordinates, checks for possible neighbour
    coordinates, and then checks if the coordinates is on the map. If it is on the map it is put in
    a list that the function returns. Later the function chooses a random cell for the animals to
    migrate to.
    In island1 the herbivores are in coordinates (2,2)
    """
    m = island1
    coordinates = [(1, 2), (2, 1), (2, 3), (3, 2)]
    m.create_map_dict()
    m.neighbours_of_current_cell((2, 2))
    for cell in range(len(m.neighbour_cells)):
        assert m.neighbour_cells[cell] == m.map[coordinates[cell]]


# Tests for year cycle
def test_year_cycle_change_weight(island1):
    """
    During a year the weight of the animals should change. In island1 the initial weight of
    herbivores are 20.
    """
    m = island1
    m.create_map_dict()
    m.year_cycle()
    for k in m.map[(2, 2)].herbivores_pop:
        assert k.weight != 20


def test_fodder_in_cell_after_fodder_eaten(mocker, island1):
    """
    Check if make_herbivores eat works in year_cycle by checking if fodder in cell has the right
    amount. During the first year there should be enough fodder for all 50 animals
    """
    mocker.patch('random.random', return_value=1)
    m = island1
    m.create_map_dict()
    m.year_cycle()
    assert m.map[(2, 2)].available_fodder == 800 - len(m.map[(2, 2)].herbivores_pop) * Herbivore.p[
        'F']


def test_year_cycle_weight_change(island1):
    """
    During year_cycle they eat and gain weight, but later they lose weight again. In the first year
    they gain F * beta, and later lose current weight * eta
    Since they all initially weigh 20, there will be no procreation, and therefore that will not
    affect the weight
    """
    m = island1
    m.create_map_dict()
    current_weight = []
    for k in m.map[(2, 2)].herbivores_pop:
        after_eating = Herbivore.p['beta'] * Herbivore.p['F']
        weight_loss = (k.weight + after_eating) * Herbivore.p['eta']
        current_weight.append(k.weight + after_eating - weight_loss)
    m.year_cycle()
    for k in range(len(m.map[(2, 2)].herbivores_pop)):
        assert m.map[(2, 2)].herbivores_pop[k].weight == current_weight[k]


def test_year_cycle_eating_carnivores():
    """
    In year_cycle the carnivores should eat herbivores. To test if this happens, we make sure no one
    dies of natural causes and compare the lengths of the new list and the initial list of
    herbivores
    """
    geogr = """\
                WWW
                WLW
                WWW"""
    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]
    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 60}
                          for _ in range(20)]}]
    m = Map_Island(island_geo=geogr, init_pop=ini_herbs + ini_carns)
    m.create_map_dict()
    init_length_herb = len(m.map[(2, 2)].herbivores_pop)
    m.year_cycle()
    assert len(m.map[(2, 2)].herbivores_pop) < init_length_herb

'''
def test_year_cycle_carnivore_weight_gain(mocker):
    """
    When the carnivore eats it should gain weight, weight of the herbivores * beta. Later in the
    year they should lose weight, initial weight * eta .
    The herbivores eats before the carnivores and therefore their weight is 10 + 10 * beta = 19
    """
    mocker.patch('random.random', return_value=0.01)
    geogr = """\
                WWW
                WLW
                WWW"""
    ini_herbs = [{'loc': (2, 2),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 10}
                          for _ in range(80)]}]
    ini_carns = [{'loc': (2, 2),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 60}
                          for _ in range(10)]}]
    m = Map_Island(island_geo=geogr, init_pop=ini_herbs + ini_carns)
    m.create_map_dict()
    current_weight = []
    for carn in m.map[(2, 2)].carnivores_pop:
        weight_gain = m.map[(2, 2)].herbivores_pop[0].weight * 3 * Carnivore.p['beta']
        weight_loss = (carn.weight + weight_gain) * Carnivore.p['eta']
        current_weight.append(carn.weight + weight_gain - weight_loss)
    m.year_cycle()
    for k in range(len(current_weight)):
        assert m.map[(2, 2)].carnivores_pop[k].weight == current_weight[k]
    # assert m.map[(2, 2)].af == len(m.map[(2, 2)].carnivores_pop)
    # m.map[(2, 2)].herbivores_pop[0].weight
'''

def test_year_cycle_newborn_animals(mocker):
    """
    Checking the length of the initial population and comparing it to the length of the new
    population  after year_cycle. When there are this many animals the probability for birth is 1.
    The probability for death however is a lot smaller. Therefore the mocker gives a random value of
    1, so that no one will die, and the length of the list should be twice as long as the original
    """
    mocker.patch('random.random', return_value=1)
    island_geo = """\
                            WWW
                            WLW
                            WWW"""
    init_pop = [{'loc': (2, 2),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 60}
                         for _ in range(50)]}]
    m = Map_Island(island_geo, init_pop)
    m.create_map_dict()
    init_amount = len(m.map[(2, 2)].herbivores_pop)
    m.year_cycle()
    assert len(m.map[(2, 2)].herbivores_pop) == init_amount * 2


def test_mother_weight_loss(mocker):
    """
    To test if the mother loses weight we have to check that the weight is less than
    initial_weight + weight gain after eating - yearly weight loss
    """
    mocker.patch('random.random', return_value=1)
    island_geo = """\
                            WWW
                            WLW
                            WWW"""
    init_pop = [{'loc': (2, 2),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 60}
                         for _ in range(50)]}]
    m = Map_Island(island_geo, init_pop)
    m.create_map_dict()
    init_length = len(m.map[(2, 2)].herbivores_pop)
    current_weight = []
    for k in m.map[(2, 2)].herbivores_pop:
        after_eating = Herbivore.p['beta'] * Herbivore.p['F']
        weight_loss = (k.weight + after_eating) * Herbivore.p['eta']
        current_weight.append(k.weight + after_eating - weight_loss)
    m.year_cycle()
    for k in range(init_length):
        assert m.map[(2, 2)].herbivores_pop[k].weight < current_weight[k]


def test_migration(mocker):
    """
    In year_cycle we first iterate through all the cells and use neighbours_of_current_cell with
    the coordinates for each of the cells as input. Neighbours_of_current_cell gives a random
    cell for the animals to migrate to, and checks if the new sell i habitable. If it's not
    habitable the animal will stay put. If it is habitable the cell will receive a list of animals
    and put it in the neighbouring cell
    If the cell is not habitable, the animals needs to be put back in the original cell
    """
    island_geo = """\
                            WWWW
                            WLLW
                            WWWW"""
    init_pop = [{'loc': (2, 2),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 60}
                         for _ in range(50)]}]
    m = Map_Island(island_geo, init_pop)
    m.create_map_dict()
    m.neighbours_of_current_cell((2, 2))
    mocker.patch('random.choice', return_value=3)
    m.year_cycle()
    assert len(m.map[(3, 2)].herbivores_pop) != 0


def test_migration_when_water(mocker):
    """
    If random.choice chooses water, all the animals should stay in the original cell.
    With the weight set to 20, the probability for death and birth is low, so with a mocker set to 1
    the length of the list should stay the same
    """
    island_geo = """\
                            WWWW
                            WLLW
                            WWWW"""
    init_pop = [{'loc': (2, 2),
                 'pop': [{'species': 'Herbivore',
                          'age': 5,
                          'weight': 20}
                         for _ in range(50)]}]
    m = Map_Island(island_geo, init_pop)
    m.create_map_dict()
    mocker.patch('random.choice', return_value=m.map[(2, 1)])
    mocker.patch('random.random', return_value=1)
    init_pop = len(m.map[(2, 2)].herbivores_pop)
    m.year_cycle()
    assert len(m.map[(2, 2)].herbivores_pop) == init_pop


def test_age(island1):
    """
    Will the animals age in accordance with the year?
    In island1 the initial age is 5
    """
    m = island1
    m.create_map_dict()
    m.year_cycle()
    for k in m.map[(2, 2)].herbivores_pop:
        assert k.age == 6


def test_remove_dead_animals(mocker, island1):
    """
    Will the dead animals be removed from the list. To test this we set a low random value, so that
    there will definitely be dead animals
    """
    mocker.patch('random.random', return_value=0.01)
    m = island1
    m.create_map_dict()
    init_length = len(m.map[(2, 2)].herbivores_pop)
    m.year_cycle()
    assert len(m.map[(2, 2)].herbivores_pop) < init_length
