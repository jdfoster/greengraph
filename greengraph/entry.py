from argparse import ArgumentParser, Action, RawDescriptionHelpFormatter
from greengraph import Greengraph
from matplotlib import pyplot as plt


def entry_point():
    parser = ArgumentParser(
        description = 'Generates a graph of the green space between two geographical locations.',
        epilog = 'Examples:\n greengraph Norwich London NOR-LON.PNG\n greengraph Edinburgh Dundee EDI-DUN.PNG --steps 30\n greengraph Chicago "New York" CHI-NYC.PNG -s 15',
        formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('from_arg', metavar='FROM', type=str,
                        help='First geographical location should be given using the Latin alphabet with a minimum size of 2 characters. For a location with more than 2 words using quotation marks to denote a single location, e.g. "New York".')
    parser.add_argument('to_arg', metavar='TO', type=str,
                        help='Second geographical location, must be different to the argument given as FROM. See FROM for more details.')
    parser.add_argument('dist_file', metavar='OUT', type=str,
                        help='Filename for the returned PNG image of the generated graph. Filename needs to have the extension png/PNG.')
    parser.add_argument('--steps', '-s', type=int, default=20,
                        help='Number of images to sample between the two locations. The first and last images are taken at the given locations, therefore the minmum value is 2. Default value is 20 steps.')
    arguments = parser.parse_args()

    for idx, arg in enumerate([arguments.from_arg, arguments.to_arg, arguments.dist_file]):
        arg_name = ['FROM', 'TO', 'OUT'][idx]
        arg_len = [2, 2, 5][idx]
        if len(arg) < arg_len:
            parser.error(arg_name + ' argument: ' + arg + ', is too short.')

    if arguments.steps < 2:
        parser.error('STEPS argument is below 2.')

    if not arguments.dist_file.lower().endswith('.png'):
        parser.error('OUT argument: ' +  arguments.dist_file + ', lacks the .png extension.')

    mygraph = Greengraph(arguments.from_arg, arguments.to_arg)
    data = mygraph.green_between(arguments.steps)
    plot, plot_axes = plt.subplots()
    plot_axes.plot(data)
    plot.savefig(arguments.dist_file)

    
if __name__ == "__main__":
    entry_point()
