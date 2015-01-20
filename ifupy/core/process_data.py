from astropy.io import fits
from data_cube import Cube


def read_data(data_file):
    if ".fits" in data_file:
        name = data_file.split("/")[-1].split(".")[-2]
        hdulist = fits.open(str(data_file))
        data_collection = []

        for i in range(len(hdulist)):
            if hdulist[i].data.size > 0:
                data_cube = Cube(data=hdulist[i].data, name=name + str(i+1))
                data_collection.append(data_cube)

        return name, data_collection
