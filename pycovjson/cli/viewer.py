"""
Pycovjson - Command line viewer
Author: rileywilliams
Version: 0.1.0
TODO - Add support for other formats and more customisation
"""
import argparse


from pycovjson.readNetCDFOOP import NetCDFReader as Reader


def main():
    parser = argparse.ArgumentParser(description='View Scientific Data files.')
    parser.add_argument('-i', '--input', dest='inputfile',
                        help='Name of input file', required=True)

    parser.add_argument('-v', '--variables,', dest='variables',
                        help='Display variables', action='store_true')

    args = parser.parse_args()
    inputfile = args.inputfile
    variables = args.variables
    reader = Reader(inputfile)
    ds = reader.get_xarray()
    # TODO
    # if variables:
    #     reader.get_vars_with_long_name(inputfile)

    print(ds)


if __name__ == '__main__':
    main()
