from setuptools import setup, find_packages

setup(
    name = "greengraph",
    version = 0.1,
    packages = find_packages(exclude=['*test']),
    scripts = ['scripts/greengraph'],
    install_requires = ['argparse', 'geopy', 'numpy', 'requests', 'matplotlib'],
    author = "Joshua D. Foster",
    author_email = "joshua.foster@ucl.ac.uk",
    description = "Command line tool to return a graph of green space between two geographical locations.",
    license = "MIT",
    keywords = "greenspace geographical graph",
    url = "https://github.com/jdfoster/greengraph"
)
