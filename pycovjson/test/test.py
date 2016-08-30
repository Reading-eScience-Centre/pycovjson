

from pycovjson.model import TileSet, Coverage, Reference
import os, numpy as np
import pycovjson
from pycovjson.readNetCDFOOP import NetCDFReader

def test():
    dir_name = os.path.dirname(__file__)

    json_template = os.path.join(dir_name, '..', 'data', 'jsont_template.json')

    testfile = 'test_xy.nc'
    dataset_path = os.path.join(dir_name, 'testdata', testfile)

    dataset = np.arange(60)
    dataset.reshape(10,6)

    urlTemplate = 'localhost:8080/'



    coverage =  (dataset_path, 'Grid', 'NdArray')
    coverage = Coverage()

    print(coverage.coverage.domain)


    netcdf_dataset = coverage.dataset
    tile_shape = [2, 1]
    # tileSet = TileSet(tile_shape, urlTemplate, dataset)


    variable_names = coverage.get_var_names(netcdf_dataset)
    # for tile in tileSet.get_tiles(tile_shape, 'data'):
    #     print(tile, '\n')
    # variable_names = pycovjson.readNetCDFOOP.get_var_names(netcdf_dataset)
    print(variable_names)
    print()
    assert len(variable_names) > 0

def read():
    dir_name = os.path.dirname(__file__)
    testfile = 'test_xy.nc'
    dataset_path = os.path.join(dir_name, 'testdata', testfile)

    # 1.
    reader = NetCDFReader(dataset_path)
    coverage = reader.read()
    reader.close()

    #2.
    coverage = NetCDFReader.read(dataset_path)

ref = Reference()

import re
subject = "localhost:8080/{t}tile.json"
subject = re.sub(r"({).(})", val, subject , 0, re.IGNORECASE)


test()
