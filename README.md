# pycovjson  ![Travis CI](https://travis-ci.org/Reading-eScience-Centre/pycovjson.svg?branch=master)

Create **CovJSON** files from common scientific data formats(e.g NetCDF)

##Installation:

Open up a command line and type the following:

    bash$> pip install pycovjson

## Usage:
Command line interface:

**pycovjson-convert** takes in 6 parameters, and can be run using python cli.py -i *name of input file(NetCDF)*-o *name of output file* -v *variable* -r *range type* [-t] *tiled* [-s] *tile shape as list*


On running the script, a CoverageJSON file will be generated.

**pycovjson-viewer** takes up to 2 parameters: -i *name of inputfile* [*-v display variable information only*] on running will display information about the input file. To be use in conjunction with **pycovjson-convert**.


Examples
--------
    bash$> pycovjson-viewer -i melodies_landcover.nc
    
    bash$> pycovjson-convert -i melodies_landcover.nc -o coverage.json -v land_cover
    
