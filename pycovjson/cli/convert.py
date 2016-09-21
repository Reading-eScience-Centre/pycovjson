"""
Pycovjson - Command line interface
Author: rileywilliams
Version: 0.1.0
"""
import argparse

from pycovjson.write import Writer
from pycovjson.read_netcdf import NetCDFReader as Reader


def main():
    parser = argparse.ArgumentParser(
        description='Convert Scientific Data Formats into CovJSON.')
    parser.add_argument('-i', '--input', dest='inputfile',
                        help='Name of input file', required=True)
    parser.add_argument('-o', '--output', dest='outputfile',
                        help='Name and location of output file', default='coverage.covjson')
    parser.add_argument(
        '-t', '--tiled', action='store_true', help='Apply tiling')
    parser.add_argument('-s', '--shape', nargs='+',
                        help='Tile shape, list', type=int)
    parser.add_argument('-v', dest='variable',
                        help='Variable to populate coverage with')
    args = parser.parse_args()
    inputfile = args.inputfile
    outputfile = args.outputfile
    variable = args.variable
    tiled = args.tiled
    tile_shape = args.shape

    if tiled and len(tile_shape) == 0:
        reader = Reader(inputfile)
        shape_list = reader.get_shape(variable)
        dims = reader.get_dimensions(variable)
        print(list(zip(dims, shape_list)))
        tile_shape = input(
            'Enter the shape tile shape as a list of comma separated  integers')
        tile_shape = tile_shape.split(',')
        tile_shape = list(map(int, tile_shape))
        print(tile_shape)
    if outputfile == None:
        outputfile = outputfile.default

    Writer(outputfile, inputfile, [variable],
           tiled=tiled, tile_shape=tile_shape).write()

if __name__ == '__main__':
    main()
