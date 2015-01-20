from __future__ import print_function
import numpy as np
from astropy.io import fits


class CubeCollection(object):
    pass


class Cube(object):
    """
    Core data object. A consistent format for all data-cube-style data. To
    be used with all IFU functionality.
    """
    def __init__(self, name='', size=(1,), data=None):
        self.name = name
        self._array = np.array(size)

        if data is not None:
            self._array = np.array(data)

    def shape(self):
        return self._array.shape

    def __add__(self, other):
        return np.add(self, other)

    def __sub__(self, other):
        return np.add(self, -other)

    def __mul__(self, other):
        return np.multiply(self, other)

    def __div__(self, other):
        return np.division(self, other)

    def __call__(self):
        return self._array


if __name__ == '__main__':
    first = Cube([3,3])
    second = Cube([3,3]) * 10
    print(first + second)