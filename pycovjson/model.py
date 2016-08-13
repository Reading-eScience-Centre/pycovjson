import numpy as np, math
from collections import OrderedDict

class Coverage(object):
    def __init__(self,domain, ranges, params, reference):
        self.domain = domain.to_dict()
        self.range = ranges.to_dict()
        self.parameter = params.to_dict()
        self.reference = reference.get_list()
        self.type = 'Coverage'

    def to_dict(self):
        cov_dict = OrderedDict()
        cov_dict['type'] = self.type
        cov_dict['domain'] = self.domain
        cov_dict['domain']['referencing'] = self.reference
        cov_dict['parameters'] = self.parameter
        cov_dict['ranges'] = self.range

        return cov_dict


class Domain(object):
    def __init__(self, domain_type, x_values=[], y_values=[], z_values=[], t_values=[]):
        self.domain_type = domain_type

        self.x_values = x_values
        self.y_values = y_values
        self.z_values = z_values
        self.t_values = t_values
    def __str__(self):
        return 'Domain Type: ' +  self.domain_type + '\nAxes:'+  str(self.axes)

    def to_dict(self):
        count = 0
        domain_dict = OrderedDict()
        domain_dict['type'] = self.domain_type
        domain_dict['axes'] = {}
        print(domain_dict['axes'])
        if not self.x_values :
            domain_dict['axes']['x'] = {'values' :  self.x_values}
        if not self.y_values :
            domain_dict['axes']['y']= {'values' :  self.y_values}
        if not self.z_values :
            domain_dict['axes']['z']= {'values' :  self.z_values}
        if not self.t_values :
            domain_dict['axes']['t']= {'values' :  self.t_values}


        return domain_dict


class Range(object):
    def __init__(self, range_type,data_type={}, axes= [],shape=[], values=[], variable_name=''):
        self.range_type = range_type
        self.data_type = data_type
        self.axis_names = axes
        self.shape = shape
        self.values = values
        self.variable_name = variable_name


    def to_dict(self):
        range_dict = OrderedDict()
        range_dict[self.variable_name] = {}
        print(range_dict)
        range_dict[self.variable_name]['type'] = self.range_type
        range_dict[self.variable_name]['dataType'] = self.data_type
        range_dict[self.variable_name]['axisNames'] = self.axis_names
        range_dict[self.variable_name]['shape'] = self.shape
        range_dict[self.variable_name]['values'] = self.values
        print(range_dict)
        return range_dict

    def populate(self, data_type={}, axes= [],shape=[], values=[], variable_name=''):
        """
        Function to populate Range object with values

        """
        self.data_type = data_type
        self.axis_names = axes
        self.shape = shape
        self.values = values
        self.variable_name = variable_name


class Parameter(object):
    def __init__(self, variable_name, description , unit, symbol,symbol_type,observed_property,op_id, label_langtag='en' ):
        self.variable_name = variable_name
        self.param_type = 'Parameter'
        self.description = description
        self.unit =  unit
        self.label_langtag = label_langtag
        self.symbol = symbol
        self.symbol_type = symbol_type
        self.observed_property = observed_property
        self.op_id = op_id


    def to_dict(self):
        param_dict = OrderedDict()
        param_dict[self.variable_name] = {}
        param_dict[self.variable_name]['type'] = self.param_type
        param_dict[self.variable_name]['unit'] ={}
        param_dict[self.variable_name]['unit']['label'] = {self.label_langtag : self.unit}
        param_dict[self.variable_name]['symbol']={}
        param_dict[self.variable_name]['symbol']['value'] = self.symbol
        param_dict[self.variable_name]['symbol']['type'] = self.symbol_type
        param_dict[self.variable_name]['observedProperty']={}
        param_dict[self.variable_name]['observedProperty']['id'] = self.op_id
        param_dict[self.variable_name]['observedProperty']['label'] = {self.label_langtag : self.observed_property}
        return param_dict



class Reference(object):
    def __init__(self, obj_list):
        self.coordinates = []
        self.obj_list = obj_list
        print('Object list : ', self.obj_list)
    def get_temporal(self, *args):
        return self.TemporalReferenceSystem(*args)

    def get_spatial2d(self, *args):
        return self.SpatialReferenceSystem2d(*args)

    def get_spatial3d(self, *args):
        return self.SpatialRefrenceSystem3d(*args)

    def get_list(self):
        item_list = []

        for elem in self.obj_list:
            print('get_list')
            item_list.append(elem.to_dict())

        return item_list


class TemporalReferenceSystem(Reference):
    def __init__(self, cal=None):
        self.type = 'TemporalRS'
        Reference.coordinates = ['t']

        if (cal == None):
            self.cal = "Gregorian"
        else:
            self.cal = cal
    def to_dict(self):
        ref_dict = OrderedDict()
        ref_dict['coordinates'] = self.coordinates
        ref_dict['system'] ={}
        ref_dict['system']['type'] = self.type
        ref_dict['system']['calendar'] = self.cal
        return ref_dict



class SpatialReferenceSystem2d(Reference):
    def __init__(self):
        self.id = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
        self.type = 'GeodeticCRS'
        Reference.coordinates = ['x', 'y']

    def set_type(self, new_type):
        """
        :type new_type: str
        """
        self.type = new_type

    def to_dict(self):
        ref_dict = OrderedDict()
        ref_dict['coordinates'] = self.coordinates
        ref_dict['system'] ={}
        ref_dict['system']['type'] = self.type
        ref_dict['system']['is'] = self.id
        return ref_dict



class SpatialReferenceSystem3d(Reference):
    def __init__(self):
        self.id = "http://www.opengis.net/def/crs/EPSG/0/4979"
        self.type = 'GeodeticCRS'
        Reference.coordinates = ['x', 'y', 'z']

    def set_type(self, new_type):
        """
        :type new_type: str
        """
        self.type = new_type

    def to_dict(self):
        ref_dict = OrderedDict()
        ref_dict['coordinates'] = self.coordinates
        ref_dict['system'] ={}
        ref_dict['system']['type'] = self.type
        ref_dict['system']['id'] = self.id
        return ref_dict


class TileSet(object):
    def __init__(self, tile_shape, urlTemplate, dataset):
        self.tile_shape = tile_shape #List containing shape
        self.urlTemplate = urlTemplate
        self.dataset = dataset
        self.shape = []

    def create_tileset(self):
        tileset = []
        tile_dict = {}
        tile_dict['tileShape'] = self.tileShape
        tile_dict['urlTemplate'] = self.urlTemplate
        tileset.append(tile_dict)
        return tileset


    def set_dataset(self, dataset):
        pass

    def get_url_template(self, val):
        self.val = val

        import re
        subject = self.urlTemplate
        subject = re.sub(r"({).(})", self.val, subject, 0, re.IGNORECASE)


        return self.urlTemplate
    def get_tiles(self, tile_shape: object, variable: object) -> object:
        """
        Function which returns tile arrays from an input array
        :param tile_shape:

        :param variable:
        :return:
        """
        array = self.dataset[variable][:]
        self.shape = array.shape
        print(self.shape)

        def step(b, dim, tile_indices):
            if dim == len(array.shape):
                yield (b, tile_indices)
                return

            tile_count = math.ceil(self.shape[dim] / tile_shape[dim])


            for i in range(tile_count):
                c = b[tile_shape[dim] * i:tile_shape[dim] * (i + 1)]
                c = np.rollaxis(c, 1)
                tile_indices[dim] = i
                yield from step(c, dim + 1, tile_indices)

        yield from step(array, 0, [0] * len(self.shape))

    def get_array_shape(self):
        print(self.shape)
        return self.shape











