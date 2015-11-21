#!/usr/bin/env python2
from argparse import ArgumentParser, FileType
import greengraph

def entry_point():
    parser = ArgumentParser()
    parser.add_argument('from_arg', metavar='FROM', type=str)
    parser.add_argument('to_arg', metavar='TO', type=str)
    parser.add_argument('dist_file', metavar='OUT', type=FileType('w'))
    parser.add_argument('--steps', '-s', type=int, default=20)
    arguments = parser.parse_args()
    print arguments.from_arg, arguments.to_arg, arguments.dist_file, arguments.steps

if __name__ == "__main__":
    entry_point()
