import geopy
import numpy as np
import map


class Greengraph(object):
    def __init__(self, start, end):
        if not (isinstance(start, str) & isinstance(end, str)):
            raise TypeError('Geographical locations need given as strings')
        if (len(start) < 2) | (len(end) < 2):
            raise TypeError('Locations need to be two characters or more')
        self.start = start
        self.end = end
        self.geocoder = geopy.geocoders.GoogleV3(domain="maps.google.co.uk")

    def geolocate(self, place):
        found_location = self.geocoder.geocode(place, exactly_one=False)
        if not found_location:
            raise NameError('Geographical location not found')
        return found_location[0][1]

    def location_sequence(self, start, end,  steps):
        lats = np.linspace(start[0], end[0], steps)
        longs = np.linspace(start[1], end[1], steps)
        return np.vstack([lats, longs]).transpose()

    def green_between(self, steps):
        return [map.Map(*location).count_green()
                for location in self.location_sequence(
                        self.geolocate(self.start),
                        self.geolocate(self.end),
                        steps)]
