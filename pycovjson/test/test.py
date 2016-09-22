

from pycovjson.model import TileSet, Coverage, Reference
import os
import numpy as np
import pycovjson
from pycovjson.read_netcdf import NetCDFReader


def test():
    dir_name = os.path.dirname(__file__)

    json_template = os.path.join(dir_name, '..', 'data', 'jsont_template.json')

    testfile = 'test_xy.nc'
    dataset_path = os.path.join(dir_name, 'testdata', testfile)

    dataset = np.arange(60)
    dataset.reshape(10, 6)

    urlTemplate = 'localhost:8080/'

    tile_shape = [2, 1]
    # tileSet = TileSet(tile_shape, urlTemplate, dataset)

    try:
        variable_names = NetCDFReader(testfile).get_var_names()
    except OSError:
        print('Error: ', OSError)
    # for tile in tileSet.get_tiles(tile_shape, 'data'):
    #     print(tile, '\n')
    # variable_names = pycovjson.readNetCDFOOP.get_var_names(netcdf_dataset)

    assert len(variable_names) > 0


def read():
    dir_name = os.path.dirname(__file__)
    testfile = 'test_xy.nc'
    dataset_path = os.path.join(dir_name, 'testdata', testfile)

    # 1.
    reader = NetCDFReader(dataset_path)
    coverage = reader.read()

def test_convert():
    import pycovjson.convert
    pycovjson.convert('foam_2011-01-01.nc','coverage.covjson', ['SALTY'])

test()
test_convert()
