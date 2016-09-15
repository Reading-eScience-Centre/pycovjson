import json
import os.path
import uuid
import time
from collections import OrderedDict
from pycovjson.model import *
import numpy as np
import pycovjson.readNetCDFOOP
import pycovjson.readNetCDF as rnc
# File Locations

json_template_path = 'data/jsont_template.json'
ncdf_file = rnc.ncdf_file
json_file = 'json_output_test.json'
json_ranges = 'data/ranges.json'
json_parameter = 'data/parameter.json'
json_referencing = 'data/referencing.json'
json_referencing3d = 'data/referencing3d.json'

domain_type = "Grid"  # Default

PATH_DATA = os.path.join(os.path.dirname(__file__), '..', 'data')

# Creating NetCDF dataset object

dset = rnc.load_netcdf(ncdf_file)

# ReadNetCDF data
var_names = rnc.get_var_names(dset)
rnc.extract_var_data(var_names)

# TEST - REPLACE WITH FUNCTION TO TAKE OPTIONS FROM USER
dim_list = rnc.group_vars(var_names)
num_list = list(range(0, len(dim_list)))

variable_dimensions = dict(zip(num_list, dim_list))


def get_variables():
    var_names = rnc.get_var_names(dset)
    num_list = list(range(0, len(var_names)))
    var_dict = dict(zip(num_list, var_names))
    print(var_dict)
    print(variable_dimensions)
    choice = int(input("Enter number of variable: "))
    return var_dict[choice]

user_opts = []
choice = get_variables()
user_opts.append(choice)


def load_json(path):
    with open(path, 'r') as fp:
        return json.load(fp, object_pairs_hook=OrderedDict)


json_template = load_json(json_template_path)


def construct_range(var_name, tiled):
    ranges = load_json(json_ranges)
    ranges['dataType'] = str(rnc.get_type(var_name))
    if tiled:
        ranges['type'] = 'TiledNdArray'
    else:
        ranges['type'] = 'NdArray'
    ranges['shape'] = rnc.get_shape(var_name)
    if rnc.has_time():
        ranges['axisNames'] = ['t', 'y', 'x']
    else:
        ranges['axisNames'] = ['y', 'x']
    # Debug
    print("Construct range ran successfully...")
    return ranges


def construct_parameters(var_name):
    parameters = load_json(json_parameter)

    # parameters[var_name]['description'] = rnc.get_long_name(var_name)
    return parameters


def construct_referencing(var_name):
    """

    :param var_name: name of variable
    :return: list of referencing objects
    """
    var_dim_length = len(rnc.get_dimensions(var_name))

    referencing = load_json(json_referencing)

    refObj = SpatialReferenceSystem2d(['x', 'y'])
    referencing_dict = {}
    referencing_dict['coordinates'] = refObj.coordinates
    referencing_dict['system'] = {}
    referencing_dict['system']['type'] = refObj.type
    referencing_dict['system']['id'] = refObj.id
    ref_list = [referencing_dict]
    if rnc.has_time():
        t_dict = {}
        trefObj = TemporalReferenceSystem()
        t_dict['coordinates'] = trefObj.coordinates
        t_dict['system'] = {}
        t_dict['system']['type'] = trefObj.type
        t_dict['system']['calendar'] = trefObj.cal
        ref_list.append(t_dict)

    print(ref_list)
    print('Construct Referencing ran successfuly...')

    # referencing_list.append(referencing[0])
    # referencing_list.append(referencing[1])

    return ref_list


def construct_tiles(var_name):
    tileObj = TileSet([None, 'x', 'y'], 'https://www.googledrive.com/host//')
    tileObj.create_tileset('TEST')
    return tileObj


def construct_covjson(json_template, data,  variables, domain_type="Grid", time=False, tiled=False):
    """
    Create covJSON object, fill with data values
    :rtype: object
    :param json_template:
    :param data:
    :param domain_type:
    :return:
    """

    longitude = detect_coords(dset)[0]
    latitude = detect_coords(dset)[1]

    json_template['domain']['domainType'] = domain_type

    # Coordinate data x - longitude y- latitude
    json_template['domain']['axes']['x']['values'] = (data[longitude].tolist())
    json_template['domain']['axes']['y']['values'] = data[latitude].tolist()
    # Melodies landcover dataset, latitude values flipped, use flipup to correct
    #json_template['domain']['axes']['y']['values'] = np.flipud(data[latitude]).tolist()

    # json_template['domain']['referencing'] = construct_referencing(user_opts[0])
    if time:
        json_template['domain']['axes']['t'] = {'values': []}
        json_template['domain']['axes']['t'][
            'values'] = rnc.convert_time(rnc.get_time())
    json_template['domain']['referencing'] = construct_referencing(choice)
    for var in variables:

        if tiled:
            tile_shape = [1, 1, 1]
            variable = 'SALTY'
            tiles = TileSet(tile_shape, 'localhost:8080/{t}tile.json', dset,)
            json_template['ranges']
            json_template['ranges'][var] = construct_range(var, tiled=True)
            json_template['ranges'][var]['shape'] = rnc.get_shape(var)
            json_template['ranges'][var]['tileSets'] = {}

            for tile in range(len(tiles.get_array_shape())):
                json_template['ranges'][var][
                    'tileSets']['tileShape'] = tile_shape
                json_template['ranges'][var]['tileSets'][
                    'urlTemplate'] = tiles.get_url_template(tile)

            json_tile = {}
            tile_list = list(tiles.get_tiles(tile_shape, variable))
            for tile in tile_list:
                json_tile = construct_range(var, tiled=False)
                json_tile['values'] = tile
                save_json(json_tile, 'json_tile.json')

        else:
            json_template['ranges']
            json_template['ranges'][var] = construct_range(var, tiled=False)
            json_template['ranges'][var]["values"] = {}
            json_template['ranges'][var]['values'] = (
                data[var].ravel().tolist())

        json_template['parameters'][var] = construct_parameters(var)
        json_template['parameters'][var][
            'description'] = rnc.get_description(var)
        json_template['parameters'][var]['unit'][
            'label']['en'] = rnc.get_units(var)
        if rnc.get_std_name(var) != None:
            json_template['parameters'][var]['observedProperty'][
                'id'] = 'http://vocab.nerc.ac.uk/standard_name/' + str(rnc.get_std_name(var))
        else:
            json_template['parameters'][var]['observedProperty']['id'] = None

        json_template['parameters'][var][
            'observedProperty']['label']['en'] = var

    return json_template


# Adapted from
# https://github.com/the-iea/ecem/blob/master/preprocess/ecem/util.py -
# letmaik


def save_json(obj, path, **kw):
    with open(path, 'w') as fp:
        print("Converting....")
        start = time.clock()
        jsonstr = json.dumps(obj, fp, cls=CustomEncoder, **kw)
        fp.write(jsonstr)
        stop = time.clock()
        print("Completed in: ", (stop - start), "seconds.")


def save_covjson(obj, path):
    # skip indentation of certain fields to make it more compact but still
    # human readable
    for axis in obj['domain']['axes'].values():
        compact(axis, 'values')
    for ref in obj['domain']['referencing']:
        no_indent(ref, 'coordinates')
    for range in obj['ranges'].values():
        no_indent(range, 'axisNames', 'shape')
        compact(range, 'values')
    save_json(obj, path, indent=2)


def compact(obj, *names):
    for name in names:
        obj[name] = Custom(obj[name], separators=(',', ':'))


def no_indent(obj, *names):
    for name in names:
        obj[name] = Custom(obj[name])


# From http://stackoverflow.com/a/25935321
class Custom(object):

    def __init__(self, value, **custom_args):
        self.value = value
        self.custom_args = custom_args


class CustomEncoder(json.JSONEncoder):

    def __init__(self, *args, **kwargs):
        super(CustomEncoder, self).__init__(*args, **kwargs)
        self._replacement_map = {}

    def default(self, o):
        if isinstance(o, Custom):
            key = uuid.uuid4().hex
            self._replacement_map[key] = json.dumps(o.value, **o.custom_args)
            return "@@%s@@" % (key,)
        else:
            return super(CustomEncoder, self).default(o)

    def encode(self, o):
        result = super(CustomEncoder, self).encode(o)
        for k, v in self._replacement_map.items():
            result = result.replace('"@@%s@@"' % (k,), v)
        return result


def set_coords(coord_list, t):
    t = t
    x = coord_list[0]
    y = coord_list[1]
    z = coord_list[2]
    return tuple([x, y, z, t])


def detect_coords(dset):
    """
    :return: Tuple containing lat and lon var names
    """
    for var in dset.variables:
        if rnc.is_x(var):
            x = var
        if rnc.is_y(var):
            y = var

    return tuple([x, y])


out_file = open(json_file, "w")
json.dumps(json_template, indent=4)

# Test parameters

print("Coords are: ", detect_coords(dset))
print(dset)

var_names = rnc.get_var_names(dset)
data = rnc.extract_var_data(var_names)
json_obj = construct_covjson(json_template, rnc.extract_var_data(
    var_names), user_opts, domain_type="Grid", time=rnc.has_time(), tiled=True)

save_covjson(json_obj, json_file)
