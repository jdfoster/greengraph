import os
import yaml
import sys
from mock import patch
from nose.tools import assert_raises
from ..entry import entry_point
from numpy.random import choice
from contextlib import contextmanager
from StringIO import StringIO


@contextmanager
def capture_sys_output():
    capture_out, capture_err = StringIO(), StringIO()
    current_out, current_err = sys.stdout, sys.stderr
    try:
        sys.stdout, sys.stderr = capture_out, capture_err
        yield capture_out, capture_err
    finally:
        sys.stdout, sys.stderr = current_out, current_err


def test_entry_point():
    with open(os.path.join(
            os.path.dirname(__file__), 'fixtures',
            'broken_location_pairs_plus_png.yaml')) as fixtures_file:
        fixtures = yaml.load(fixtures_file)
        for fixture in fixtures:
            test_args = ['greengraph_prog', fixture['from'],
                         fixture['to'],fixture['out']]
            switch = choice(['--steps', '-s'])
            test_args.append(switch)
            step_value = fixture['steps']
            if isinstance(step_value, str):
                step_value = '\"' + step_value + '\"'
                test_args.append(step_value)
            else:
                test_args.append(str(step_value))
            print isinstance(step_value,str)
            print test_args
            with patch.object(sys, 'argv', test_args), \
                    assert_raises(SystemExit) as exception, \
                    capture_sys_output() as (stdout, stderr):
                entry_point()
