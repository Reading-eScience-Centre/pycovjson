import json
from collections import OrderedDict
import netCDF4
import readNetCDF as rnc
import numpy as np
import uuid
import util

import util

#File Locations
json_template_path = 'jsont_template.json'
#nc_file = 'foam_2011-01-01.nc'
nc_file = rnc.nc_file
json_file = 'json_output_test.json'
json_ranges = 'ranges.json'
json_parameter ='parameter.json'


domain_type = "Grid" # Default

#Creating NetCDF dataset object
dset = rnc.load_netcdf(nc_file)

# ReadNetCDF data
var_names = rnc.get_var_names(dset)
rnc.extract_var_data(var_names)

#TEST - REPLACE WITH FUNCTION TO TAKE OPTIONS FROM USER
user_opts = ['ICEC']

print(rnc.get_var_names(dset))



def load_json(path):
    with open(path, 'r') as fp:
        return json.load(fp, object_pairs_hook=OrderedDict)

json_template = load_json(json_template_path)


def construct_range(var_name):

    ranges = load_json(json_ranges)
    ranges['dataType'] = str(rnc.get_type(var_name))
    ranges['shape'] = rnc.get_shape(var_name)

    return ranges

def construct_parameters(var_name):
    parameters = load_json(json_parameter)
    #parameters[var_name]['description'] = rnc.get_long_name(var_name)
    return parameters


def update_domain(json_template, data):

    return 0



def update_json(json_template, data, domain_type, user_opts):

    """
    :param json_template:
    :param data:
    :param domain_type:
    :return:
    """

    json_template['domain']['domainType'] = domain_type

    # Coordinate data
    json_template['domain']['axes']['x']['values'] = (data['lon'].tolist())
    json_template['domain']['axes']['y']['values'] = (data['lat'].tolist())


    #Variable data
    # json_template['ranges'][main_var]['values'] = (data[main_var].ravel().tolist())[0:1]

    for var in user_opts:

        json_template['ranges'][var] = construct_range(var)
        json_template['ranges'][var]['values'] = (data[var].ravel().tolist()) #For testing, limit dataset

        json_template['parameters'][var] = construct_parameters(var)
        json_template['parameters'][var]['description'] = rnc.get_long_name(var)


    # Debug
    #print(json.dumps(json_template,indent=4))

    return json_template


def save_json(obj, path, **kw):
    with open(path, 'w') as fp:
        jsonstr = json.dumps(obj, fp, cls=CustomEncoder, **kw)
        fp.write(jsonstr)



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


out_file = open(json_file, "w")

json.dumps(json_template,indent=4)


# Test parameters
var_names = rnc.get_var_names(dset)
data = rnc.extract_var_data(var_names)
json_obj = update_json(json_template, rnc.extract_var_data(var_names), "Grid", user_opts)

save_json(json_obj,json_file, indent=4)

util.save_covjson(json_obj, json_file)


# util.save_covjson(update_json(json_template,rnc.extract_var_data(rnc.get_var_names(dset)),"Grid"),'prettyjson.json')









