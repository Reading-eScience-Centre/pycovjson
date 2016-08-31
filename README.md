# pycovjson  ![Travis CI](https://travis-ci.org/Reading-eScience-Centre/pycovjson.svg?branch=master)

Create **CovJSON** files from common scientific data formats(e.g NetCDF)


## Usage:
Command line interface:

**convert.py** takes in 6 parameters, and can be run using python cli.py -i *name of input file(NetCDF)*-o *name of output file* -v *variable* -r *range type* [-t] *tiled* [-s] *tile shape as list*


On running the script, a CoverageJSON file will be generated.

**viewer.py** takes up to 2 parameters: -i *name of inputfile* [*-v display variable information only*] on running will display information about the input file. To be use in conjunction with **convert.py**.

[] = optional args


