"""
Pycovjson - Command line interface
Author: rileywilliams
Version: 0.1.0
"""
import argparse

from pycovjson.write import Writer

parser = argparse.ArgumentParser(description='Convert Scientific Data Formats into CovJSON.')
parser.add_argument('-i', '--input', dest='inputfile', help='Name of input file', required=True)
parser.add_argument('-o', '--output', dest='outputfile', help='Name and location of output file')
parser.add_argument('-t', '--tiled', action='store_true', help='Apply tiling')
parser.add_argument('-s', '--shape', nargs='+', help='Tile shape, list', type=int)
parser.add_argument('-v',dest='variable' ,help='Variable to populate coverage with')
args = parser.parse_args()
inputfile = args.inputfile
outputfile = args.outputfile
variable = args.variable
tiled = args.tiled
tile_shape = args.shape

def main():
    Writer(outputfile, inputfile, [variable], tiled=tiled, tile_shape=tile_shape).write()

if __name__ == '__main__':
    main()



