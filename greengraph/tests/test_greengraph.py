import os
import yaml
import mock
from nose.tools import assert_raises, assert_almost_equal, assert_equal, assert_sequence_equal
import geopy
import numpy as np
from ..greengraph import Greengraph
from generate_fixtures import broken_steps_value

def test_init_type_fail():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'broken_locations_pairs.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            test_locations = [fixture['from'], fixture['to']]
            test_locations = [item if item else '' for item in test_locations]
            with assert_raises(TypeError) as exception:
                assert Greengraph(test_locations[0], test_locations[1])


def test_init_implementation_fail():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'random_coordinate_pairs.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            test_locations = [fixture['start_nom'], fixture['start_nom']]
            test_locations = [item if item else '' for item in test_locations]
            with assert_raises(NotImplementedError) as exception:
                assert Greengraph(test_locations[0], test_locations[1])


def test_geolocate_pass():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'random_coordinate_pairs.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            test_name = fixture['start_nom']
            test_location = fixture.pop('start_loc')
            return_geocoder = [geopy.Location(test_name, test_location)]
            with mock.patch('geopy.geocoders.GoogleV3.geocode') as mock_geocoder:
                mock_geocoder.return_value = return_geocoder
                given_loc = Greengraph('first', 'second').geolocate(test_name)
                mock_geocoder.assert_any_call(test_name, exactly_one=False)
                assert_sequence_equal(test_location, given_loc)


def test_geolocate_notfound():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'random_coordinate_pairs.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            test_name = fixture['start_nom']
            test_location = fixture.pop('start_loc')
            return_geocoder = None
            with mock.patch('geopy.geocoders.GoogleV3.geocode') as mock_geocoder, assert_raises(NameError) as exception:
                mock_geocoder.return_value = return_geocoder
                assert Greengraph('first', 'second').geolocate(test_name)
                mock_geocoder.assert_any_call(test_name, exactly_one=False)


def test_location_sequence_type_fail():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'broken_coordinate_pairs.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            start = fixture['start']
            end = fixture['end']
            steps = fixture['steps']
            with assert_raises(TypeError) as exception:
                assert Greengraph('first', 'second').location_sequence(start, end, steps)


def test_location_sequence_diff():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'random_coordinate_pairs.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            start = fixture['start_loc']
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


def test_green_between_steps_fail():
    for _ in range(40):
        steps_value = broken_steps_value()
        with assert_raises(TypeError) as exception:
            assert Greengraph('first', 'second').green_between(steps_value)


def test_green_between_component():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'random_coordinate_pairs.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            start_nom = fixture['start_nom']
            start_loc = fixture.pop('start_loc')
            end_nom = fixture['end_nom']
            end_loc = fixture.pop('end_loc')
            return_geocoder = [[geopy.Location(start_nom, start_loc)], [geopy.Location(end_nom, end_loc)]]
            steps = fixture['steps']
            with mock.patch('greengraph.map.Map') as mock_Map, mock.patch('geopy.geocoders.GoogleV3.geocode') as mock_geocoder:
                mock_geocoder.side_effect = return_geocoder
                green = Greengraph(start_nom, end_nom).green_between(steps)
                mock_Map.assert_any_call(*start_loc)
                mock_Map.assert_any_call(*end_loc)
                assert_equal(len(mock_Map.mock_calls), steps*2)
