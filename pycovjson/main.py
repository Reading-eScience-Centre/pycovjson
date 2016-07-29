#import readNetCDF as rnc
#import writeJSON
import sys, getopt
import argparse
import pycovjson.readNetCDF as rnc
from pycovjson.writeJSON import TransformNC

# parser = argparse.ArgumentParser(description='Convert Scientific Data Formats into CovJSON.')
# parser.add_argument('inputfile', metavar='file', type=str, help ='path to file(s) for conversion')
# parser.add_argument('-o', '--output', dest='outputfile', help='name and location of output file')
# args = parser.parse_args()
# inputfile = args.inputfile
# outputfile = args.outputfile
# var_list = args.vars




dset = ''


def get_user_selection(file_dict):
    print(file_dict)
    selection = int(input("Enter the number of the file you would like to use:"))
    return file_dict[selection]








input('\n')