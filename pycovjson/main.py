#import readNetCDF as rnc
#import writeJSON
import sys, getopt
import argparse



parser = argparse.ArgumentParser(description='Convert Scientific Data Formats into CovJSON.')
parser.add_argument('inputfile', metavar='file', type=str, help ='path to file(s) for conversion')
parser.add_argument('-o', dest='outputfile', help='name and location of output file')

args = parser.parse_args()
inputfile = args.inputfile
outputfile = args.outputfile




input('\n')