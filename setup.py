from setuptools import setup, find_packages
from greengraph import __version__ as version
import os

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    DESCRIPTION = readme.read()

setup(
    name = "greengraph",
    version = version,
    packages = find_packages(exclude=["*tests",]),
    test_suite = 'nose.collector',
    tests_require = ['mock', 'nose', 'pyyaml'],
    scripts = ['scripts/greengraph'],
    install_requires = ['argparse', 'geopy', 'numpy', 'requests', 'matplotlib'],
    author = "Joshua D. Foster",
    author_email = "joshua.foster@ucl.ac.uk",
    description = "Command line tool to return a graph of green space between two geographical locations.",
    long_description = DESCRIPTION,
    license = "MIT",
    keywords = "greenspace geographical graph",
    url = "https://github.com/jdfoster/greengraph",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: GIS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"
    ]
)
