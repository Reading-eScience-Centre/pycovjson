
import argparse

from pycovjson.write import Writer

parser = argparse.ArgumentParser(description='Convert Scientific Data Formats into CovJSON.')
parser.add_argument('-i', '--input', dest='inputfile', help='Name of input file')
parser.add_argument('-o', '--output', dest='outputfile', help='Name and location of output file')
parser.add_argument('-t', dest='tiled', help='Apply tiling')
parser.add_argument('-v',dest='variable' ,help='Variable to populate coverage with')
parser.add_argument('-r', dest='range_type', help='Range Type. E.g TiledNdArray or NdArray')
args = parser.parse_args()
inputfile = args.inputfile
outputfile = args.outputfile
variable = args.variable
range_type = args.range_type

Writer(outputfile, inputfile, [variable], range_type).write()



