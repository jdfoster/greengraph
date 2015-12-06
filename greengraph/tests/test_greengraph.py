import os
import yaml
import mock
from nose.tools import assert_raises, assert_almost_equal, assert_equal
import geopy
import numpy as np
from ..greengraph import Greengraph


def test_greengraph_init_type_fail():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'broken_location_pair.yaml')) as fixutres_file:
        fixtures = yaml.load(fixutres_file)
        for fixture in fixtures:
            test_locations = [fixture['from'], fixture['to']]
            test_locations = [item if item else '' for item in test_locations]
            with assert_raises(TypeError) as exception:
                Greengraph(test_locations[0], test_locations[1])


def test_greengraph_init_implementation_fail():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'random_coordinate_single.yaml')) as fixutres_file:
        fixtures = yaml.load(fixutres_file)
        for fixture in fixtures:
            test_locations = [fixture['name'], fixture['name']]
            test_locations = [item if item else '' for item in test_locations]
            with assert_raises(NotImplementedError) as exception:
                Greengraph(test_locations[0], test_locations[1])


def test_greengraph_geolocate_pass():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'random_coordinate_single.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            test_name = fixture['name']
            test_location = fixture.pop('location')
            return_geocoder = geopy.Location(test_name, test_location)
            with mock.patch('geopy.geocoders.GoogleV3.geocode') as mock_geocoder:
                mock_geocoder.return_value = return_geocoder
                Greengraph('first', 'second').geolocate(test_name)
                mock_geocoder.assert_any_call(test_name, exactly_one=False)


def test_greengraph_geolocate_notfound():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'random_coordinate_single.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            test_name = fixture['name']
            test_location = fixture.pop('location')
            return_geocoder = None
            with mock.patch('geopy.geocoders.GoogleV3.geocode') as mock_geocoder, assert_raises(NameError) as exception:
                mock_geocoder.return_value = return_geocoder
                Greengraph('first', 'second').geolocate(test_name)
                mock_geocoder.assert_any_call(test_name, exactly_one=False)


def test_greengraph_location_sequence_type_fail():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'broken_coordinate_pairs.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            start = fixture['start']
            end = fixture['end']
            steps = fixture['steps']
            with assert_raises(TypeError) as exception:
                Greengraph('first', 'second').location_sequence(start, end, steps)


def test_greengraph_location_sequence_diff():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'random_coordinate_single.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            start = fixture['location']
            delta = (np.random.uniform(1, 40), np.random.uniform(1, 40))
            end = (start[0]+delta[0], start[1]+delta[1])
            steps = fixture['steps']
            test_array = Greengraph('first', 'second').location_sequence(start, end, steps)
            tp_test_array = test_array.transpose()
            first_array = tp_test_array[0]
            second_array = tp_test_array[1]
            len_array = np.mean([len(first_array), len(second_array)])
            first_diff_sum = sum(np.diff(first_array))
            second_diff_sum = sum(np.diff(second_array))
            assert_almost_equal(first_diff_sum, delta[0])
            assert_almost_equal(second_diff_sum, delta[1])
            assert_equal(len_array, steps)
