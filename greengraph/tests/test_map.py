from mock import patch
from nose.tools import assert_raises, assert_equal
import requests
from matplotlib import image as img
import os
import yaml
from StringIO import StringIO
import numpy as np
from ..map import Map


def test_init_type_fail():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'broken_map_init.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            location = fixture['coordinate']
            satellite = fixture['satellite']
            zoom = fixture['zoom']
            size = fixture['size']
            sensor = fixture['sensor']
            with assert_raises(TypeError) as exception:
                assert Map(location[0], location[1], satellite, zoom, size, sensor)


def test_URL_format():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'random_map_init.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            location = fixture['coordinate']
            satellite = fixture['satellite']
            zoom = fixture['zoom']
            size = fixture['size']
            sensor = fixture['sensor']
            expected_url='http://maps.googleapis.com/maps/api/staticmap?'
            expected_params = {
                'sensor':str(sensor).lower(),
                'zoom':zoom,
                'size':'x'.join([str(val) for val in size]),
                'center':','.join([str(val) for val in location]),
                'style':'feature:all|element:labels|visibility:off'}
            if satellite:
                expected_params['maptype']='satellite'
            with patch.object(requests, 'get') as mock_get, patch.object(img, 'imread') as mock_img:
                green = Map(location[0], location[1], satellite, zoom, size, sensor).count_green()
                mock_get.assert_called_with(expected_url, params=expected_params)

def test_green():
    for _ in range(20):
        img_pixel_dim = np.random.randint(2, 800, 2)
        thres_val = np.random.uniform(1, 100)
        thres_val_nudge = thres_val + 0.1
        expected_mask = np.random.randint(0, 2, img_pixel_dim)
        sub_mask_a = expected_mask.copy()
        sub_mask_b = expected_mask.copy()
        non_green_count = np.count_nonzero(expected_mask - 1)
        sub_mask_a[sub_mask_a != 1] = np.random.randint(0, 2, non_green_count)
        sub_mask_b[sub_mask_b != 1] = np.random.randint(0, 2, non_green_count)
        RGB_stack_base = np.stack((sub_mask_a, expected_mask, sub_mask_b), axis = 2)
        RGB_stack_elevate = RGB_stack_base.astype(np.float64)
        RGB_stack_elevate[:,:,1] *= thres_val_nudge
        first_pass = RGB_stack_elevate.copy()
        second_pass = first_pass.copy()
        np.swapaxes(second_pass,1,0)
        third_pass = first_pass.copy()
        np.swapaxes(third_pass,1,0)
        fourth_pass = RGB_stack_base.copy()
        with patch.object(requests, 'get') as mock_get, patch.object(img, 'imread') as mock_img:
            mock_img.side_effect = [first_pass, second_pass, third_pass, fourth_pass]
            first_actual  = Map(1., 1.).green(thres_val)
            expected_bool = expected_mask != 0
            second_actual = Map(1., 1.).green(thres_val)
            third_actual = Map(1., 1.).green(thres_val)
            fourth_actual = Map(1., 1.).green(thres_val)
            expected_null = np.zeros(img_pixel_dim, dtype=bool)
            np.testing.assert_array_equal(first_actual, expected_bool)
            np.testing.assert_array_equal(second_actual, expected_bool)
            np.testing.assert_array_equal(third_actual, expected_bool)
            np.testing.assert_array_equal(fourth_actual, expected_null)


def test_count_green():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'example_images_filelist.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            loc_name = fixture['loc_nom']
            location = fixture['location']
            map_filename = fixture['map_filename']
            green_mask_filename = fixture['green_mask_filename']
            green_count_values = fixture['green_count']
            with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'images', map_filename)) as image_file:
                return_pixels = img.imread(image_file)
            with patch.object(requests, 'get') as mock_get, patch.object(img, 'imread') as mock_img:
                mock_img.return_value = return_pixels
                green = Map(*location)
                for threshold, expected_green_count in green_count_values:
                    actual_green_count = green.count_green(threshold)
                    assert_equal(expected_green_count, actual_green_count)
