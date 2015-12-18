import geopy
import string
import random
import numpy as np
import os
import yaml
import requests
from StringIO import StringIO
from greengraph import Map


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
    latitude = np.random.uniform(-89.5, 89.5)
    longitude = np.random.uniform(-179.5, 179.5)
    return (latitude, longitude)


def random_coordinate_pair():
    return random_coordinate_generator(), random_coordinate_generator()


def broken_coordinate_single():
    init_coordinate = random_coordinate_generator()
    brake_type = np.random.choice([str, int])
    brake_index =np.random.randint(0,1)
    return_list = [brake_type(item) if index == brake_index
                   else item for index, item in enumerate(init_coordinate)]
    return (return_list[0], return_list[1])


def broken_coordinate_pair():
    init_list = np.random.uniform(-180, 180, size=4).tolist()
    brake_type = np.random.choice([str, int])
    brake_index = np.random.randint(0, 3)
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


def save_random_coordinate_pairs(size=80):
    output_file = "random_coordinate_pairs.yaml"
    place_names_fixture = []
    for _ in range(size):
        random_places = [random_place_name_generator(),
                        random_place_name_generator()]
        random_locations = [random_coordinate_generator(),
                           random_coordinate_generator()]
        steps = random_step_generator()
        place_names_fixture.append({'start_nom': random_places[0],
                                    'end_nom': random_places[1],
                                    'start_loc': random_locations[0],
                                    'end_loc': random_locations[1],
                                    'steps': steps})
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', output_file), 'w') as target:
        target.write(yaml.dump(place_names_fixture))


def save_broken_coordinate_pairs(size=80):
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

        
def google_map_search(place, domain="maps.google.co.uk"):
    search = geopy.geocoders.GoogleV3(domain="maps.google.co.uk")
    found_location = search.geocode(place, exactly_one=False)
    if not found_location:
        return None
    else:
        return found_location[0][1]


def fetch_map(latitude, longitude, satellite=True, zoom=10, size=(400,400), sensor=False):
    base="http://maps.googleapis.com/maps/api/staticmap?"
    params=dict(
        sensor= str(sensor).lower(),
        zoom= zoom,
        size= "x".join(map(str, size)),
        center= ",".join(map(str, (latitude, longitude) )),
        style="feature:all|element:labels|visibility:off"
    )
    if satellite:
            params["maptype"]="satellite"
    return requests.get(base, params=params).content


def create_map_image(place, output_file, green_mask=False):
    place_location = google_map_search(place)
    place_image = fetch_map(*place_location)
    place_image_green = Map(*place_location).show_green()
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', 'images', output_file), 'w') as target:
        if green_mask:
            target.write(place_image_green)
        else:
            target.write(place_image)


def return_green_values(place, threshold_values):
    place_location = google_map_search(place)
    place_Map_class = Map(*place_location)    
    return [(float(val), int(place_Map_class.count_green(val))) for val in threshold_values]

def save_map_images():
    output_filelist = 'example_images_filelist.yaml'
    filename_fixture = []
    collect_maps = [['Norwich', 'example_map_01a.png', 'example_map_01b.png'], ['London', 'example_map_02a.png', 'example_map_02b.png']]
    for collect_map in collect_maps:
        params = {'loc_nom':collect_map[0], 'map_filename':collect_map[1], 'green_mask_filename':collect_map[2]}
        params['location'] = google_map_search(collect_map[0])
        params['green_count'] = return_green_values(collect_map[0], np.linspace(0.2,2.0,10))
        filename_fixture.append(params)
        create_map_image(collect_map[0], collect_map[1], green_mask=False)
        create_map_image(collect_map[0], collect_map[2], green_mask=True)
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', output_filelist), 'w') as target:
        target.write(yaml.dump(filename_fixture))


def random_map_init():
    def bool_working():
        return bool(np.random.choice([True, False]))
    def zoom_working():
        return np.random.randint(1, 200)
    def size_working():
        return (np.random.randint(2, 800), np.random.randint(2, 800))
    return [random_coordinate_generator(), bool_working(), zoom_working(), size_working(), bool_working()]


def brake_map_init():
    def bool_working():
        return bool(np.random.choice([True, False]))
    def zoom_working():
        return np.random.randint(1, 200)
    def size_working():
        return (np.random.randint(2, 800), np.random.randint(2, 800))
    def make_negative(value):
        return value * -1
    def bool_broken():
        return str(bool_working())
    def zoom_broken():
        brake_with = np.random.choice([str, float, make_negative])
        return brake_with(zoom_working())
    def size_broken():
        init_values = size_working()
        brake_with = np.random.choice([str, float, make_negative])
        brake_index = np.random.randint(0, 1)
        return_values = [brake_with(item) if index == brake_index
                         else item for index, item in enumerate(init_values)]
        return_values = tuple(return_values)
        return return_values
    all_working = [random_coordinate_generator(), bool_working(), zoom_working(), size_working(), bool_working()]
    all_broken = [broken_coordinate_single(), bool_broken(), zoom_broken(), size_broken(), bool_broken()]
    brake_index = np.random.randint(0,4)
    return_array = all_working
    return_array[brake_index] = all_broken[brake_index]
    return return_array


def save_broken_map_init(size=80):
    output_file = "broken_map_init.yaml"
    map_init_fixture = []
    for _ in range(size):
        first, second, third, fourth, fifth = brake_map_init()
        map_init_fixture.append({'coordinate': first,
                                   'satellite': second,
                                   'zoom': third,
                                   'size':fourth,
                                   'sensor':fifth})
    with open(os.path.join(os.path.dirname(__file__),
                          'fixtures', output_file), 'w') as target:
        target.write(yaml.dump(map_init_fixture))


def save_working_map_init(size=80):
    output_file = "random_map_init.yaml"
    map_init_fixture = []
    for _ in range(size):
        first, second, third, fourth, fifth = random_map_init()
        map_init_fixture.append({'coordinate': first,
                                   'satellite': second,
                                   'zoom': third,
                                   'size':fourth,
                                   'sensor':fifth})
    with open(os.path.join(os.path.dirname(__file__),
                          'fixtures', output_file), 'w') as target:
        target.write(yaml.dump(map_init_fixture))
