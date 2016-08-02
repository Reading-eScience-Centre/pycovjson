class Range():
    def __init__(self, rangetype, datatype, axisnames, shape, values):
        self.rangetype = rangetype
        self.datatype = datatype
        self.axisnames = axisnames
        self.shape = shape
        self.values = values


class Reference():
    def __init__(self, components):
        self.components = components


class TemporalReferenceSystem(Reference):
    def __init__(self, cal=None):
        self.type = 'TemporalRS'
        Reference.components = ['t']

        if (cal == None):
            self.cal = "Gregorian"
        else:
            self.cal = cal


class SpatialReferenceSystem2d(Reference):
    def __init__(self, components):
        self.id = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
        self.type = 'GeodeticCRS'
        Reference.components = components

    def set_type(self, new_type):
        """
        :type new_type: str
        """
        self.type = new_type


class SpatialReferenceSystem3d(Reference):
    def __init__(self):
        self.id = "http://www.opengis.net/def/crs/EPSG/0/4979"
        self.type = 'GeodeticCRS'
        Reference.components = ['x', 'y', 'z']

    def set_type(self, new_type):
        """
        :type new_type: str
        """
        self.type = new_type
