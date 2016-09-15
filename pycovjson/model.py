import numpy as np
import math
from collections import OrderedDict


class Coverage(object):

    def __init__(self, domain, ranges, params, reference):
        self.domain = domain.to_dict()
        self.range = ranges.to_dict()
        self.parameter = params.to_dict()
        self.reference = reference.to_list()
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
        self.referencing = []

    def __str__(self):
        return 'Domain Type: ' + self.domain_type + '\nAxes:' + str(self.axes)

    def to_dict(self):
        domain_dict = OrderedDict()
        domain_dict['domainType'] = self.domain_type
        domain_dict['axes'] = {}

        domain_dict['axes']['x'] = {'values':  self.x_values}

        domain_dict['axes']['y'] = {'values':  self.y_values}

        domain_dict['axes']['t'] = {'values': self.t_values}
        domain_dict['axes']['z'] = {'values': self.z_values}
        if len(self.z_values) == 0:
            # domain_dict['axes']['z']= {'values' :  self.z_values}
            domain_dict['axes'].pop('z', None)
        if len(self.t_values) == 0:
            # domain_dict['axes']['t']= {'values' :  self.t_values}
            domain_dict['axes'].pop('t', None)

        domain_dict['referencing'] = []
        return domain_dict


class Range(object):

    def __init__(self, range_type, data_type={}, axes=[], shape=[], values=[], variable_name='', tile_sets=[]):
        self.range_type = range_type
        self.data_type = data_type
        self.axis_names = axes
        self.shape = shape
        self.values = values
        self.variable_name = variable_name
        self.tile_sets = tile_sets

    def to_dict(self):
        range_dict = OrderedDict()
        range_dict[self.variable_name] = {}

        range_dict[self.variable_name]['type'] = self.range_type
        range_dict[self.variable_name]['dataType'] = self.data_type
        range_dict[self.variable_name]['axisNames'] = self.axis_names
        range_dict[self.variable_name]['shape'] = self.shape
        if self.range_type == 'TiledNdArray':
            range_dict[self.variable_name]['tileSets'] = self.tile_sets

        else:

            range_dict[self.variable_name]['values'] = self.values

        return range_dict

    def populate(self, data_type={}, axes=[], shape=[], values=[], variable_name=''):
        """
        Function to populate Range object with values

        """
        self.data_type = data_type
        self.axis_names = axes
        self.shape = shape
        self.values = values
        self.variable_name = variable_name


class Parameter(object):

    def __init__(self, variable_name='', description='', unit='', symbol='', symbol_type='', observed_property='', op_id=None, label_langtag='en'):
        self.variable_name = variable_name
        self.param_type = 'Parameter'
        self.description = description
        self.unit = unit
        self.label_langtag = label_langtag
        self.symbol = symbol
        self.symbol_type = symbol_type
        self.observed_property = observed_property
        self.op_id = op_id

    def to_dict(self):
        param_dict = OrderedDict()
        param_dict[self.variable_name] = {}
        param_dict[self.variable_name]['type'] = self.param_type
        param_dict[self.variable_name]['description'] = self.description
        param_dict[self.variable_name]['unit'] = {}
        param_dict[self.variable_name]['unit'][
            'label'] = {self.label_langtag: self.unit}
        param_dict[self.variable_name]['symbol'] = {}
        param_dict[self.variable_name]['symbol']['value'] = self.symbol
        param_dict[self.variable_name]['symbol']['type'] = self.symbol_type
        param_dict[self.variable_name]['observedProperty'] = {}
        param_dict[self.variable_name]['observedProperty']['id'] = self.op_id
        param_dict[self.variable_name]['observedProperty'][
            'label'] = {self.label_langtag: self.observed_property}
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

    def to_list(self):
        item_list = []

        for elem in self.obj_list:
            item_list.append(elem.to_dict())
        print('Item list:', item_list)
        return item_list


class TemporalReferenceSystem(Reference):

    def __init__(self, cal=None):
        self.type = 'TemporalRS'
        self.coordinates = ['t']

        if (cal == None):
            self.cal = "Gregorian"
        else:
            self.cal = cal

    def to_dict(self):
        ref_dict = OrderedDict()
        ref_dict['coordinates'] = self.coordinates
        ref_dict['system'] = {}
        ref_dict['system']['type'] = self.type
        ref_dict['system']['calendar'] = self.cal
        return ref_dict


class SpatialReferenceSystem2d(Reference):

    def __init__(self):
        self.id = "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
        self.type = 'GeographicCRS'
        Reference.coordinates = ['x', 'y']

    def set_type(self, new_type):
        """
        :type new_type: str
        """
        self.type = new_type

    def to_dict(self):
        ref_dict = OrderedDict()
        ref_dict['coordinates'] = self.coordinates
        ref_dict['system'] = {}
        ref_dict['system']['type'] = self.type
        ref_dict['system']['id'] = self.id
        return ref_dict


class SpatialReferenceSystem3d(Reference):

    def __init__(self):
        self.id = "http://www.opengis.net/def/crs/EPSG/0/4979"
        self.type = 'GeographicCRS'
        Reference.coordinates = ['x', 'y', 'z']

    def set_type(self, new_type):
        """
        :type new_type: str
        """
        self.type = new_type

    def to_dict(self):
        ref_dict = OrderedDict()
        ref_dict['coordinates'] = self.coordinates
        ref_dict['system'] = {}
        ref_dict['system']['type'] = self.type
        ref_dict['system']['id'] = self.id
        return ref_dict


class TileSet(object):

    def __init__(self, tile_shape, url_template):
        self.tile_shape = tile_shape  # List containing shape
        self.url_template = url_template

    def create_tileset(self):
        tileset = []
        tile_dict = {}
        tile_dict['tileShape'] = self.tileShape
        tile_dict['urlTemplate'] = self.urlTemplate
        tileset.append(tile_dict)
        return tileset

    def get_url_template(self, val):
        self.val = val

        import re
        subject = self.url_template
        subject = re.sub(r"({).(})", self.val, subject, 0, re.IGNORECASE)

    def generate_url_template(self, axis_names):
        axis_names = axis_names
        if len(axis_names) == 1:
            url_template = '{' + axis_names[0] + '}.covjson'
        elif len(axis_names) == 2:
            url_template = '{' + axis_names[0] + \
                '}-{' + axis_names[1] + '}.covjson'
        elif len(axis_names) == 3:
            url_template = '{' + axis_names[0] + '}-{' + \
                axis_names[1] + '}-{' + axis_names[2] + '}.covjson'

        return url_template

    def get_tiles(self, tile_shape: object,  array) -> object:
        """
        Function which yields a generator which can be leveraged to return tile arrays from an input array
        :param tile_shape:

        :param variable:
        :return:
        """
        array = array
        self.shape = array.shape
        # print(self.shape)

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
