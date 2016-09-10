#Initial Documentation - Full Documentation in progress

Implementations
---------------

* **model.py**
 * model.py contains all of the classes for each component of the coverage object, as well as helper methods to generate dictionaries and create tilesets.

* **write.py** 
  * write.py contains all of the code for constructing and writing to CoverageJSON

* **readNetCDFOOP.py**
readNetCDFOOP.py contains all of the code for reading the NetCDF data, as well as code for reformatting data.

* **convert.py**
convert.py is the command line interface for pycovjson, used to convert files to CoverageJSON

* **viewer.py**
viewer.py is the command line viewer, used to view netCDF files.

In Progress
-----------
* API Docs

Incomplete
----------

* Tiling should be working in the current version of **pycovjson**, 
however it has not been tested properly.
* Test classes still need to be implemented
* convert.py could be extended to allow for slicing by dimension instead of specifying a shape manually
* Support for more data formats

