import json
from collections import OrderedDict
import netCDF4
import readNetCDF as rnc
import numpy as np
import uuid

import util

#File Locations
json_template_path = 'jsont_template.json'
nc_file = 'foam_2011-01-01.nc'
json_file = 'json_output_test.json'
json_ranges = 'ranges.json'

domain_type = "Grid" # Default

#Creating NetCDF dataset object
dset = rnc.load_netcdf(nc_file)

# ReadNetCDF data
rnc.extract_var_data(rnc.get_var_names(dset))
var_names = rnc.get_var_names(dset)

print(rnc.get_var_names(dset))



def load_json(path):
    with open(path, 'r') as fp:
        return json.load(fp, object_pairs_hook=OrderedDict)

json_template = load_json(json_template_path)

def construct_range(json_ranges,var_name):

    ranges = load_json(json_ranges)
    ranges['dataType'] = str(rnc.get_type(var_name))
    ranges['shape'] = rnc.get_shape(var_name)





    return ranges



def update_coord(json_template, data):
    return 0


def update_json(json_template, data, domain_type):

    """

    :param json_template:
    :param data:
    :param domain_type:
    :return:
    """
    main_var = 'ICEC'
    json_template['domain']['domainType'] = domain_type

    # Coordinate data
    json_template['domain']['axes']['x']['values'] = data['lat'].tolist()
    json_template['domain']['axes']['y']['values'] = data['lon'].tolist()


    #Variable data
    # json_template['ranges'][main_var]['shape'] = rnc.get_shape(dset,main_var)
    # json_template['ranges'][main_var]['values'] = (data[main_var].ravel().tolist())[0:1]

    for var in var_names:

        json_template['ranges'][var] = construct_range(json_ranges, var)


    print(json.dumps(json_template, indent=4))

    json_template['ranges']['SALTY']['shape'] = rnc.get_shape('SALTY')
    json_template['ranges']['SALTY']['values'] = (data['SALTY'].ravel().tolist())[0:1]

    # Debug
    print(json.dumps(json_template,indent=4))

    json_template['domain']['axes']['z']['values'] = [5]

    return json.dumps(json_template,indent=4)


def save_json():
    return 0


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
data =rnc.extract_var_data(rnc.get_var_names(dset))
update_json(json_template,rnc.extract_var_data(rnc.get_var_names(dset)), "Grid")


#util.save_covjson(update_json(json_template,rnc.extract_var_data(rnc.get_var_names(dset)),"Grid"),'prettyjson.json')









