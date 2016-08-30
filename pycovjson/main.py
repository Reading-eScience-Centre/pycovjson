# import sys
# sys.path.insert(0, "pycovjson")
#
# from pycovjson.readNetCDF import *
#
# import pycovjson.readNetCDF as rnc
#
# #import writeJSON
# import getopt
# import argparse
#
# parser = argparse.ArgumentParser(description='Convert Scientific Data Formats into CovJSON.')
# parser.add_argument('-i', '--input', dest='inputfile', help='Name of input file')
# parser.add_argument('-o', '--output', dest='outputfile', help='Name and location of output file')
# args = parser.parse_args()
# inputfile = args.inputfile
# outputfile = args.outputfile
# args = vars(parser.parse_args())
#
# print(args)
# dset = ''
#
# def main():
#
#     dset = load_netcdf(args['inputfile'])
#
#     print(dset)


from pycovjson.readNetCDFOOP import NetCDFReader as Reader
from pycovjson.write import Writer

path = 'polcoms.nc'
reader = Reader()

coverage = reader.read(file_path='polcoms.nc')
coverage
print(coverage.domain)
vars = ['temperature', 'salinity']



Writer('file_name.json', coverage, vars, 'NdArray').write()
