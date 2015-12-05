import geopy
import string
import random
import numpy as np
import os
import yaml


def google_map_search(place, domain="maps.google.co.uk"):
    search = geopy.geocoders.GoogleV3(domain="maps.google.co.uk")
    found_location = search.geocode(place, exactly_one=False)
    if not found_location:
        return None
    else:
        return found_location[0][1]


def random_place_name_generator(max_num_chars=20, suffix=False):
    name_len = random.randint(4, max_num_chars)
    name_gen = ''.join(random.choice(string.lowercase)
                       for _ in range(name_len))
    if suffix:
        name_gen = name_gen + random.choice(['berg', 'brough',
                                             'burgh', 'ford',
                                             'ham', 'mouth'])
    return name_gen


def random_coordinate_generator():
    latitude = np.random.uniform(-1, 1)*180
    longitude = np.random.uniform(-1, 1)*180
    return (latitude, longitude)


def random_coordinate_pair():
    return random_coordinate_generator(), random_coordinate_generator()


def broken_coordinate_pair():
            init_list = np.random.uniform(-180,180, size=4).tolist()
            brake_type = np.random.choice([str, int])
            brake_index = np.random.randint(0,4)
            return_list = [brake_type(item) if index == brake_index
                           else item for index, item in enumerate(init_list)]
            return (return_list[0], return_list[1]), (return_list[2],
                                                      return_list[3])


def random_step_generator():
    return np.random.randint(2, 40)


def broken_steps_value():
    def make_negative(value):
        return value * -1
    brake_type = np.random.choice([str, float, make_negative])
    return brake_type(random_step_generator())


def brake_either_coordinate_steps():
    broken_coordin = (random_coordinate_pair, broken_steps_value)
    broken_step = (broken_coordinate_pair, random_step_generator)
    chosen_index = np.random.choice([0, 1])
    coordin_fun, step_fun  = (broken_coordin, broken_step)[chosen_index]
    start_coordin, end_coordin = coordin_fun()
    step_value = step_fun()
    return start_coordin, end_coordin, step_value

def save_random_place_names(size=40):
    output_file = "random_locations.yaml"
    place_names_fixture = []
    for _ in range(size):
        random_place = random_place_name_generator()
        random_location = random_coordinate_generator()
        random_step = random_step_generator()
        place_names_fixture.append({'name': random_place,
                                    'location': random_location,
                                    'steps': random_step})
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', output_file), 'w') as target:
        target.write(yaml.dump(place_names_fixture))


def save_random_coordinate_pairs(size=80):
    output_file = "random_coordinate_pairs.yaml"
    coordinate_fixture = []
    for _ in range(size):
        first, second, third = brake_either_coordinate_steps()
        coordinate_fixture.append({'start': first,
                                   'end': second,
                                   'steps': third})
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', output_file), 'w') as target:
        target.write(yaml.dump(coordinate_fixture))
