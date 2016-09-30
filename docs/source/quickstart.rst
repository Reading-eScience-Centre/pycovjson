.. # encoding: utf-8

Quickstart
**********

Purpose
-------
The following document explains how to quickly get up and running with pycovjson. It explains how to execute the key commands and explains (at a high level) what those commands are doing e.g. what input and output we can expect. More detail on expressive use of the various API's including function level API documentation can be found in subsequent pages of this documentation guide.

.. _data:

CoverageJSON Generation
-----------------------

pycovjson-viewer
^^^^^^^^^^^^^^^^
To quickly view the structure of a NetCDF file, pycovjson-viewer can be used. Usage is simple: ::

   $ pycovjson-viewer (netcdf file)

   Dimensions:  (depth: 20, lat: 171, lon: 360)
   Coordinates:
      * depth    (depth) float32 5.0 15.0 25.0 35.0 48.0 67.0 96.0 139.0 204.0 ...
      * lat      (lat) float32 -81.0 -80.0 -79.0 -78.0 -77.0 -76.0 -75.0 -74.0 ...
      * lon      (lon) float32 0.0 1.0 2.0 3.0 4.0 5.0 6.0 7.0 8.0 9.0 10.0 11.0 ...
   Data variables:
    ICEC     (lat, lon) float64 nan nan nan nan nan nan nan nan nan nan nan ...
    ICETK    (lat, lon) float64 nan nan nan nan nan nan nan nan nan nan nan ...
    M        (lat, lon) float64 nan nan nan nan nan nan nan nan nan nan nan ...
    SALTY    (depth, lat, lon) float64 nan nan nan nan nan nan nan nan nan ...
    TMP      (depth, lat, lon) float64 nan nan nan nan nan nan nan nan nan ...
    U        (lat, lon) float64 nan nan nan nan nan nan nan nan nan nan nan ...
    V        (lat, lon) float64 nan nan nan nan nan nan nan nan nan nan nan ...
    Attributes:
    title: MET OFFICE FOAM GLOBAL 1 DEG DATA
    field_date: 2011-01-01 00:00:00


pycovjson-convert
^^^^^^^^^^^^^^^^^
This is very simple... ::

  #

  # pycovjson-convert -i foam.nc -o coverage.covjson -v [SALTY]

More on using pycovjson functions later...


.. _concl:

Conclusion
----------
That concludes the quick start. Hopefully this has been helpful in providing an overview of the main pycovjson features. If you have any issues with this document then please register them at the `issue tracker <https://github.com/Reading-eScience-Centre/pycovjson/issues>`_. Please use `labels <https://help.github.com/articles/applying-labels-to-issues-and-pull-requests/>`_ to classify your issue.
