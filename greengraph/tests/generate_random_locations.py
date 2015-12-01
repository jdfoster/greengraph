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


def save_random_place_names(num_names=40):
    output_file = "random_locations.yaml"
    place_names_fixture = []
    for _ in range(num_names):
        random_place = random_place_name_generator()
        random_location = random_coordinate_generator()
        place_names_fixture.append({'name': random_place,
                                    'location': random_location})
    with open(os.path.join(os.path.dirname(__file__),
                           'fixtures', output_file), 'w') as target:
        target.write(yaml.dump(place_names_fixture))
