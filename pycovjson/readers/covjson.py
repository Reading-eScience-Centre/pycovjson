"""Code to read CovJSON into Python objects
"""

from model.model import Coverage, Domain
import json
import numpy as np

def decode_domain(dct):
    ''' Decodes a Domain object into a Python object '''

    # Decode the domain type
    domainType = None
    if 'domainType' in dct:
        # TODO: check for URIs or other possibilities
        domainType = dct['domainType']

    # Decode the axes
    if 'axes' not in dct:
        raise ValueError('Domain must have an "axes" property')
    axes = dct['axes']
    # Loop through each axis
    for axis in axes:
        # TODO: deal with start, stop, num syntax
        # TODO: guard method
        values = axes[axis]['values']
        # Replace the Python dictionary with the axis values
        # Should these be numpy arrays for consitency with the ranges?
        axes[axis] = values

    # TODO: deal with referencing properly
    return Domain(axes, dct['referencing'], domainType)

def decode_ndarray(dct):
    ''' Decodes an NdArray object into a numpy array '''

    # Check the array of values
    if 'values' in dct:
        values = dct['values']
    else:
        raise ValueError('NdArray objects must have a "values" property')

    # Check the "shape" property
    if 'shape' in dct:
        shape = dct['shape']
        #TODO: check that product of shape values is the same as len(values)
    elif len(values) == 1:
        # There is only a single value
        shape = []
    else:
        raise ValueError('NdArray objects with >1 data value must have a "shape" property')

    # Check the "axisNames" property
    if 'axisNames' in dct:
        axisNames = dct['axisNames']
    elif len(values) == 1:
        # There is only a single value
        axisNames = []
    else:
        raise ValueError('NdArray objects with >1 data value must have an "axisNames" property')

    # Check that "shape" and "axisNames" are consistent
    if len(shape) != len(axisNames):
        raise ValueError('"shape" and "axisNames" arrays must have the same length')

    # We create a numpy array of the appropriate type from the Python list
    if 'dataType' in dct:
        dataType = dct['dataType']
        if dataType == 'float':
            dtype = np.dtype(float)
        elif dataType == 'integer':
            # TODO: it seems that numpy won't decode an array of integers that
            # has missing values, because it can't convert to NaN. Would need to
            # use a masked array (might be better to do that in general anyway?)
            dtype = np.dtype(int)
        elif dataType == 'string':
            raise ValueError("Can't handle string values at the moment")
        else:
            #TODO: reinstate
            dtype = np.dtype(float)
            #raise ValueError('Invalid dataType property for NdArray')
    else:
        raise ValueError('NdArray objects must have a dataType property')
    # The reshape operation works correctly with respect to axis order because
    # CovJSON NdArrays are encoded in row-major order, which matches numpy
    nparr = np.array(values, dtype=dtype).reshape(shape)

    return { 'axisNames' : axisNames, 'values' : nparr }


def decoder(dct):
    ''' This is passed to the json.loads() method to automatically convert certain
        json objects into Python objects '''
    if 'type' in dct:
        objtype = dct['type']
        if objtype == 'NdArray':
            return decode_ndarray(dct)
        elif objtype == 'Domain':
            return decode_domain(dct)
        elif objtype == 'Parameter':
            return dct #TODO decode parameter
    return dct

def loadCoverage(jsonStr):
    """This method is the public API of this module
    """
    # Could use StringIO to support streaming (using json.load()) but this requires
    # a unicode string
    dct = json.loads(jsonStr, object_hook=decoder)
    return Coverage(dct['domain'], dct['parameters'], dct['ranges'])
