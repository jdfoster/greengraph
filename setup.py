from setuptools import setup, find_packages
from greengraph import __version__ as version

DESCRIPTION = """ """ # Place holder for long description

setup(
    name = "greengraph",
    version = version,
    packages = find_packages(exclude=['*test']),
    scripts = ['scripts/greengraph'],
    install_requires = ['argparse', 'geopy', 'numpy', 'requests', 'matplotlib'],
    author = "Joshua D. Foster",
    author_email = "joshua.foster@ucl.ac.uk",
    description = "Command line tool to return a graph of green space between two geographical locations.",
    long_description = DESCRIPTION
    license = "MIT",
    keywords = "greenspace geographical graph",
    url = "https://github.com/jdfoster/greengraph"
)
