
from pycovjson.model import *
from pycovjson.readNetCDFOOP import NetCDFReader as Reader
import numpy
import time, json, uuid


class Writer(object):

    def __init__(self, file_name, coverage, vars_to_write, range_type):
        self.file_name = file_name
        self.coverage = coverage
        print(coverage)
        self.vars_to_write = vars_to_write
        self.range_type = range_type
        self.Reader = Reader()

    def write(self):
        # TODO Populate coverage, save coverage object as JSON


        return self.coverage



    def _construct_coverage(self):
        # TODO Reconstruct coverage object from individual elements
        ranges = 'ranges'
        params = 'parameters'
        refs = 'references'
        domain = 'domain'
        coverage = self.coverage
        coverage[ranges] = self._construct_range()
        coverage[params] =self._construct_params()
        coverage[refs] = self._construct_refs()
        coverage[domain] = self._construct_domain()
        pass

    def _construct_domain(self):
        domain = self.coverage['domain']
        # domain['axes'] = Reader().get_axes()

        return domain




    def _construct_params(self):
        # TODO
        params = self.coverage['params']
        return params



    def _construct_refs(self):
        # TODO
        refs = self.coverage['refs']
        return refs

    def _construct_range(self):
        # TODO add value insertion and iteration through variable list
        variable = self.vars_to_write[0]

        ranges = 'ranges'
        data_type = self.reader.get_type(variable)
        axes = self.reader.get_axes(variable)
        shape = self.reader.get_shape(variable)
        values = self.reader.dataset[variable].values.tolist()

        # populate function params def populate(self, data_type={}, axes= [],shape=[], values=[], variable_name=''):
        Range.populate(data_type, axes, shape,values,variable)
        coverage = self.coverage
        coverage['dataType'] = self.reader.get_type(variable)
        coverage[ranges]['type'] = self.range_type
        return coverage

    def _save_json(self, covjson_object):
        # TODO Save json object to disk, copy
        pass

    def _save_covjson(self, json_object):
        # TODO generate and save covjson object
        pass

    def set_variables_to_write(self):
        pass


# Adapted from https://github.com/the-iea/ecem/blob/master/preprocess/ecem/util.py - letmaik


def save_json(obj, path, **kw):
    with open(path, 'w') as fp:
        print("Converting....")
        start = time.clock()
        jsonstr = json.dumps(obj, fp, cls=CustomEncoder, **kw)
        fp.write(jsonstr)
        stop = time.clock()
        print("Completed in: ", (stop - start), "seconds.")


def save_covjson(obj, path):
    # skip indentation of certain fields to make it more compact but still human readable
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


