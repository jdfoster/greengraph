import os, yaml
#from mock import patch
from nose.tools import assert_raises
from ..greengraph import Greengraph

def test_greengraph_init_fail():
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'greengraph_fails.yaml')) as fixures_file:
        fixtures = yaml.load(fixures_file)
        for fixture in fixtures:
            test_locations = [fixture['from'], fixture['to']]
            test_locations = [item if item else '' for item in test_locations]
            with assert_raises(TypeError) as exception:
                Greengraph(test_locations[0], test_locations[1])
