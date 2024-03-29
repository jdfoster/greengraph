import requests
from matplotlib import image as img
from StringIO import StringIO
import numpy as np

class Map(object):
    def __init__(self, lat, long, satellite=True, zoom=10, size=(400,400), sensor=False):
        def bool_iter_integer(container):
            return all(isinstance(item, int) for item in container)
        def iter_greater_than(container, value):
            return all(item > value for item in container)
        if not (isinstance(lat, float) & isinstance(long, float)):
            raise TypeError('Coordinates need to be floats')
        if not (isinstance(satellite, bool) & isinstance(sensor, bool)):
            raise TypeError('Satellite and senor variables need to be Boolean values (either True or False')
        if not (isinstance(zoom, int) & (zoom > 0)):
            raise TypeError('Zoom variable need to be a positive interger')
        if not len(size) == 2:
            raise TypeError('Size variable should be an iterable container with two float values')
        if not (bool_iter_integer(size) & iter_greater_than(size, 1)):
            raise TypeError('Size values within iterable container should be positive integers')

        base="http://maps.googleapis.com/maps/api/staticmap?"
        params=dict(
            sensor= str(sensor).lower(),
            zoom= zoom,
            size= "x".join(map(str, size)),
            center= ",".join(map(str, (lat, long) )),
            style="feature:all|element:labels|visibility:off"
        )

        if satellite:
            params["maptype"]="satellite"

        self.image = requests.get(base, params=params).content
        # Fetch our PNG image data
        self.pixels= img.imread(StringIO(self.image))
        # Parse our PNG image as a numpy array

    def green(self, threshold):
        if not (isinstance(threshold, float) & (threshold > 0.)):
            raise TypeError('Threshold value should be a float value above 0')

        # Use NumPy to build an element-by-element logical array
        greener_than_red = self.pixels[:,:,1] > threshold* self.pixels[:,:,0]
        greener_than_blue = self.pixels[:,:,1] > threshold*self.pixels[:,:,2]
        green = np.logical_and(greener_than_red, greener_than_blue)
        return green

    def count_green(self, threshold = 1.1):
        if not (isinstance(threshold, float) & (threshold > 0.)):
            raise TypeError('Threshold value should be a float value above 0')
        
        return np.sum(self.green(threshold))

    def show_green(self, threshold = 1.1):
        if not (isinstance(threshold, float) & (threshold > 0.)):
            raise TypeError('Threshold value should be a float value above 0')
        
        green = self.green(threshold)
        out = green[:,:,np.newaxis]*np.array([0,1,0])[np.newaxis,np.newaxis,:]
        buffer = StringIO()
        result = img.imsave(buffer, out, format='png')
        return buffer.getvalue()
