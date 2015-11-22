#!/usr/bin/env python2
from argparse import ArgumentParser, Action
#import greengraph.Greengraph

def entry_point():
    parser = ArgumentParser()
    parser.add_argument('from_arg', metavar='FROM', type=str)
    parser.add_argument('to_arg', metavar='TO', type=str)
    parser.add_argument('dist_file', metavar='OUT', type=str)
    parser.add_argument('--steps', '-s', type=int, default=20)
    arguments = parser.parse_args()

    for idx, arg in enumerate([arguments.from_arg, arguments.to_arg, arguments.dist_file]):
        arg_name = ['FROM', 'TO', 'OUT'][idx]
        arg_len = [2, 2, 5][idx]
        if len(arg) < arg_len:
            parser.error(arg_name + ' argument: ' + arg + ', is too short.')

    if arguments.steps < 3:
        parser.error('STEP argument is below 3.')

    if not arguments.dist_file.lower().endswith('.png'):
        parser.error('OUT argument: ' +  arguments.dist_file + ', lacks the .png extension.')

    print arguments.from_arg, arguments.to_arg, arguments.dist_file, arguments.steps

if __name__ == "__main__":
    entry_point()
