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


def random_place_name_generator(min_num_chars=4, max_num_chars=20,
                                suffix=False):
    name_len = random.randint(min_num_chars, max_num_chars)
    name_gen = ''.join(random.choice(string.lowercase)
                       for _ in range(name_len))
    if suffix:
        name_gen = name_gen + random.choice(['berg', 'brough',
                                             'burgh', 'ford',
                                             'ham', 'mouth'])
    return name_gen


def broken_place_name():
    return random_place_name_generator(0,1)


def broken_place_name_pair():
    first_place_broke = (broken_place_name, random_place_name_generator)
    second_place_broke = (random_place_name_generator, broken_place_name)
    both_broke = (broken_place_name, broken_place_name)
    choice_array = [first_place_broke, second_place_broke, both_broke]
    first_fun, second_fun = choice_array[np.random.choice([0, 1, 2])]
    return first_fun(), second_fun()

def random_png_name_generator():
    return random_place_name_generator(4,4) + '.png'


def broken_png_name():
    correct_name = random_png_name_generator()
    del_index = np.random.choice([4,5,6,7])
    return_name = correct_name[:del_index] + correct_name[del_index+1:]
    return return_name


def random_coordinate_generator():
    latitude = np.random.uniform(-1, 1)*180
    longitude = np.random.uniform(-1, 1)*180
    return (latitude, longitude)


def random_coordinate_pair():
    return random_coordinate_generator(), random_coordinate_generator()


def broken_coordinate_pair():
            init_list = np.random.uniform(-180, 180, size=4).tolist()
            brake_type = np.random.choice([str, int])
            brake_index = np.random.randint(0, 4)
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


def brake_either_place_steps_png():
    broken_name = (broken_place_name, random_step_generator,
                   random_png_name_generator)
    broken_step = (random_place_name_generator, broken_steps_value,
                   random_png_name_generator)
    broken_png = (random_place_name_generator, random_step_generator,
                  broken_png_name)
    chosen_index = np.random.choice([0, 1, 2])
    first_name = np.random.choice([0, 1])
    second_name = (first_name+1) % 2
    name_fun, step_fun, png_fun = (broken_name, broken_step,
                                   broken_png)[chosen_index]
    name_array = [name_fun(), random_place_name_generator()]
    step_value = step_fun()
    png_value = png_fun()
    return_array = [name_array[first_name], name_array[second_name],
                    step_value, png_value]
    return return_array


def brake_either_coordinate_steps():
    broken_coordin = (broken_coordinate_pair, random_step_generator)
    broken_step = (random_coordinate_pair, broken_steps_value)
    chosen_index = np.random.choice([0, 1])
    coordin_fun, step_fun = (broken_coordin, broken_step)[chosen_index]
    start_coordin, end_coordin = coordin_fun()
    step_value = step_fun()
    return start_coordin, end_coordin, step_value


def save_broken_place_names_pairs(size=80):
    output_file = "broken_locations_pairs_plus_png.yaml"
    place_names_fixture = []
    for _ in range(size):
        from_nom, to_nom, steps, out_nom = brake_either_place_steps_png()
        place_names_fixture.append({'from': from_nom,
                                    'to': to_nom,
                                    'steps': steps,
                                    'out': out_nom})
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', output_file), 'w') as target:
        target.write(yaml.dump(place_names_fixture))


def save_random_coordinate_single(size=80):
    output_file = "random_coordinate_single.yaml"
    place_names_fixture = []
    for _ in range(size):
        random_place = random_place_name_generator()
        random_location = random_coordinate_generator()
        steps = random_step_generator()
        place_names_fixture.append({'name': random_place,
                                    'location': random_location,
                                    'steps': steps})
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', output_file), 'w') as target:
        target.write(yaml.dump(place_names_fixture))


def save_random_coordinate_pairs(size=80):
    output_file = "broken_coordinate_pairs.yaml"
    coordinate_fixture = []
    for _ in range(size):
        first, second, third = brake_either_coordinate_steps()
        coordinate_fixture.append({'start': first,
                                   'end': second,
                                   'steps': third})
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', output_file), 'w') as target:
        target.write(yaml.dump(coordinate_fixture))


def save_broken_location_pair(size=80):
    output_file = "broken_location_pair.yaml"
    place_names_fixture = []
    for _ in range(size):
        from_nom, to_nom = broken_place_name_pair()
        place_names_fixture.append({'from': from_nom,
                                    'to': to_nom})
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', output_file), 'w') as target:
        target.write(yaml.dump(place_names_fixture))
