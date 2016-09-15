# pycovjson  
[![Build Status](https://travis-ci.org/Reading-eScience-Centre/pycovjson.svg?branch=master)](https://travis-ci.org/Reading-eScience-Centre/pycovjson)
[![PyPI](https://img.shields.io/pypi/v/pycovjson.svg?maxAge=2592000?style=plastic)](https://pypi.python.org/pypi/pycovjson)
[![Python Badge](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/)

Create **[CovJSON](https://covjson.org/)** files from common scientific data formats(e.g NetCDF)

##Installation:

Open up a command line and type the following:
```
$ pip install pycovjson
```
## Usage:
Command line interface:

**[pycovjson-convert](https://github.com/Reading-eScience-Centre/pycovjson/blob/master/pycovjson/cli/convert.py)** accepts 6 parameters, and can be run as followed 
```
$ python cli/convert.py -i *name of input file(NetCDF)* -o *name of output file* -v *variable* -r *range type* [-t] *tiled* [-s] *tile shape as list*
```


On running the script, a CoverageJSON file will be generated.

**[pycovjson-viewer](https://github.com/Reading-eScience-Centre/pycovjson/blob/master/pycovjson/cli/viewer.py)** accepts up to 2 parameters: 
```
$ python cli/viewer.py -i *name of inputfile* [*-v display variable information only*] on running will display information about the input file. To be use in conjunction with **pycovjson-convert**.
```

Examples
--------
```
$ python cli/viewer.py -i melodies_landcover.nc
    
$ python cli/convert.py -i melodies_landcover.nc -o coverage.json -v land_cover
``` 

Project Roadmap
---------------
The project roadmap can be found [here.](https://github.com/Reading-eScience-Centre/pycovjson/projects/1)