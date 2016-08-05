import numpy as np
class Coverage(object):
    def __init__(self):
        self.type = 'Coverage'

class Domain(object):
    def __init__(self, domainType):
        self.domainType = domainType



class Range(object):
    def __init__(self, rangetype, datatype, axisnames, shape, values):
        self.rangetype = rangetype
        self.datatype = datatype
        self.axisnames = axisnames
        self.shape = shape
        self.values = values

class Parameter(object):
    def __init__(self, description, unit, label, symbol, observedProperty):
        self.description = description
        self.unit = unit
        self.label = label
        self.symbol = symbol
        self.observedProperty = observedProperty



class Reference(object):
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
        Reference.components = ['x', 'y']

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

class TileSet(object):
    def __init__(self, tileShape, urlTemplate, dataset):
        self.tileShape = tileShape #List containing shape
        self.urlTemplate = urlTemplate
        self.dataset = dataset

    def create_tileset(self):
        tileset = []
        tile_dict = {}
        tile_dict['tileShape'] = self.tileShape
        tile_dict['urlTemplate'] = self.urlTemplate
        tileset.append(tile_dict)
        return tileset


    def set_dataset(self, dataset):
        pass

    def get_tiles(self, tileShape, variable):
        array = self.dataset[variable][:]
        shape = array.shape

        def step(b, dim, tileIndices):
            if dim == len(array.shape):
                yield (b, tileIndices)
                return

            tileCount = shape[dim] // tileShape[dim]
            for i in range(tileCount):
                c = b[tileShape[dim] * i:tileShape[dim] * (i + 1)]
                c = np.rollaxis(c, 1)
                tileIndices[dim] = i
                yield from step(c, dim + 1, tileIndices)

        yield from step(array, 0, [0] * len(shape))











