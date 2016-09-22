# pycovjson  
[![Build Status](https://travis-ci.org/Reading-eScience-Centre/pycovjson.svg?branch=master)](https://travis-ci.org/Reading-eScience-Centre/pycovjson)
[![PyPI](https://img.shields.io/pypi/v/pycovjson.svg?maxAge=2592000?style=plastic)](https://pypi.python.org/pypi/pycovjson)
[![Python Badge](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/downloads/)
[![Anaconda-Server Badge](https://anaconda.org/auto/flask-neo4j/badges/version.svg)](https://anaconda.org/auto/flask-neo4j)
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
$ python cli/viewer.py [*-v display variable information only*] on running will display information about the input file. To be use in conjunction with **pycovjson-convert**.
```

Examples
--------
```
$ python cli/viewer.py 
    
$ python cli/convert.py -i melodies_landcover.nc -o coverage.json -v land_cover
``` 

##Library
###Convert.py
Once pycovjson is installed, type the following at the top of your code:
```
import pycovjson.convert
```
Once imported you can then use the convert function within your projects.
###Examples
```
pycovjson.convert('polcoms.nc', 'coverage.covjson', [sst])
```
This will generate a file called coverage.covjson in the directory where
the script is located.

Project Roadmap
---------------
The project roadmap can be found [here.](https://github.com/Reading-eScience-Centre/pycovjson/projects/1)