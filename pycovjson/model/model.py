"""Data model for CovJSON.
"""


class Domain(object):
    ''' A domain '''

    def __init__(self, axes, referencing, domainType = None):
        ''' axes is a dictionary of numpy arrays, referencing is a dictionary '''
        self.domainType = domainType
        self.axes = axes
        self.referencing = referencing

class Coverage(object):
    ''' A coverage '''
    # TODO: parameter groups

    def __init__(self, domain, parameters, ranges):
        ''' Simply takes a decoded JSON object (as a dictionary) and turns the dictionaries into
            Python objects. Is there a quicker way to do this? '''
        #TODO: internal consistency checks, e.g. domain axes and ranges.axisNames
        self.domain = domain
        self.params = parameters
        self.ranges = ranges

    def toXarray(self):
        ''' Returns a representation of this coverage as an xarray.Dataset '''
        # TODO: work out what to do with parameters and referencing information
        # prepare the dictionary of data variables
        import xarray as xr
        datavars = {}
        for rangekey in self.ranges:
            rangeval = self.ranges[rangekey]
            datavars[rangekey] = (rangeval['axisNames'], rangeval['values'])
        # prepare the dictionary of coordinate variables
        # TODO: don't know if this works for non-primitive axes or time axes
        coordvars = {}
        for axis in self.domain.axes:
            # TODO: does it matter if axes have integer values or should they always be floats?
            coordvars[axis] = ([axis], self.domain.axes[axis])

        # TODO: units etc, recorded as attributes on the variables
        return xr.Dataset(datavars, coordvars)
