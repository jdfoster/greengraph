# greengraph

greengraph is a python 2.7 program that generates a graph of the green
space between two geographical locations. Green space is calculated as
counts of green pixels from a series of google map satellite images at
uniformly spaced steps between the two given locations.

Please refer to [CITATION](https://github.com/jdfoster/greengraph/blob/master/CITATION.md) for information
regarding cite this package.

© Joshua D. Foster 2015-2016 under [MIT License](https://github.com/jdfoster/greengraph/blob/master/LICENSE.md).


### Installation

Install using pip with:

``` sh
pip install -e git+https://github.com/jdfoster/greengraph.git#egg=greengraph
```

Alternatively, this repository can be cloned and then installed with:

``` sh
python setup.py install
```


### Usage

``` sh
greengraph TO FROM OUT [--steps/-s STEPS]
```

The arguments TO, FROM and OUT are mandatory. Whereas, the --steps/-s
switch for the STEPS value is optional.

| Argument | Description |
| -------- | ----------- |
| FROM     | First geographical location should be given using the Latin alphabet with a minimum size of 2 characters. For locations with more than 2 words names use quotation marks to denote it as a single location, e.g. "New York". |
| TO       | Second geographical location, must be differ to that given as the FROM argument. See FROM for more details. |
| OUT      | Filename for the PNG image of the generated graph. Filename needs to have the extension png or PNG. |
| STEPS    | Number of images to sample between the two locations. The first and last images are taken at the given locations. The steps value should be an integer with a minimum value of 2. Default value is 20 steps. |


### Examples - Terminal

To generate a PNG image (NOR-LON.PNG) of the green count between
Norwich and London with the default (20) steps:

``` sh
greengraph Norwich London NOR-LON.PNG
```

To create the graph (EDI-DUN.PNG) of the green count between Edinburgh
and Dundee with 30 steps:

``` sh
greengraph Edinburgh Dundee EDI-DUN.PNG --steps 30
```

For locations with more than a one word in there place name quotation
marks are required to group words as a single place name. For example,
to create the graph green between Chicago and New York with 15 steps:

``` sh
greengraph Chicago "New York" CHI-NYC.PNG -s 15
```

### Example - Python

The Greengraph class can be imported directly into python and used as
shown. This will generate a matplotlib graph showing the 20 counts of
green between Manchester and London.

``` python
from greengraph import Greengraph
from matplotlib import pyplot as plt
green = Greengraph('Manchester', 'London')
data = green.green_between(20)
plot, plot_axes = plt.subplots()
plot_axes.plot(data)
```
