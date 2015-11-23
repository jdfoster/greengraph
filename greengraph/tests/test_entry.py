import os, yaml, sys
from mock import patch
from nose.tools import assert_raises
from ..entry import entry_point
from numpy.random import random, randint, choice
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

def test_parse_args_fail():
    # Testing entry_point function using default step value
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'entry_point_fails.yaml')) as fixures_file:
        fixtures = yaml.load(fixures_file)
        for fixture in fixtures:
            test_args = [fixture['program'], fixture['from'], fixture['to'], fixture['out']]
            test_args = [item if item else '' for item in test_args]
            with patch.object(sys, 'argv', test_args):
                with assert_raises(SystemExit) as exception:
                    entry_point()

def test_parse_args_negative_steps_fail():
    # Testing entry_point function using random interger below 3 as step value
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'entry_point_passes.yaml')) as fixures_file:
        fixtures = yaml.load(fixures_file)
        fixture = fixtures[0]
        step_values = randint(-20, 3, 10)
        for step_value in step_values:
            test_args = [fixture['program'], fixture['from'], fixture['to'], fixture['out']]
            switch = choice(['--steps', '-s'])
            test_args.append(switch)
            test_args.append(str(step_value))
            with patch.object(sys, 'argv', test_args):
                with assert_raises(SystemExit) as exception:
                    entry_point()

def test_parse_args_float_steps_fail():
    # Testing entry_point function using random float as step value
    with open(os.path.join(os.path.dirname(__file__), 'fixtures', 'entry_point_passes.yaml')) as fixures_file:
        fixtures = yaml.load(fixures_file)
        fixture = fixtures[0]
        step_values = random(10)*100
        for step_value in step_values:
            test_args = [fixture['program'], fixture['from'], fixture['to'], fixture['out']]
            switch = choice(['--steps', '-s'])
            test_args.append(switch)
            test_args.append(str(step_value))
            with patch.object(sys, 'argv', test_args):
                with assert_raises(SystemExit) as exception:
                    entry_point()
