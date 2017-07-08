from pycovjson.model import Coverage, Domain, Parameter, Range, Reference, SpatialReferenceSystem2d, SpatialReferenceSystem3d, TemporalReferenceSystem, TileSet
from pycovjson.read_netcdf import NetCDFReader as Reader
import time
import json
import uuid


class Writer(object):
    """Writer class"""

    def __init__(self, output_name: object, dataset_path: object, vars_to_write: object, tiled=False, tile_shape=[]) -> object:
        """
        Writer class constructor

        :parameter output_name: Name of output file
        :parameter dataset_path: Path to dataset
        :parameter vars_to_write: List of variables to write
        :parameter tiled: Boolean value (default False)
        :parameter tile_shape: List containing shape of tiles
        """
        self.output_name = output_name
        self.dataset_path = dataset_path
        self.tile_shape = tile_shape
        self.vars_to_write = vars_to_write
        self.url_template = 'localhost:8080/{t}.covjson'
        self.tiled = tiled
        if tiled:
            self.range_type = 'TiledNdArray'
        else:
            self.range_type = 'NdArray'
        self.dataset_path = dataset_path
        self.reader = Reader(dataset_path)
        self.axis_dict = self.Reader.get_axes()
        self.axis_list = list(self.axis_dict.keys())
        self.ref_list = []
        if 't' in self.axis_list and 'z' in self.axis_list:
            self.ref_list.append(TemporalReferenceSystem())
            self.ref_list.append(SpatialReferenceSystem3d())

        if 't' in self.axis_list and 'z' not in self.axis_list:
            self.ref_list.append(TemporalReferenceSystem())
            self.ref_list.append(SpatialReferenceSystem2d())
        elif 't' not in self.axis_list and 'z' not in self.axis_list:
            self.ref_list.append(SpatialReferenceSystem2d())

    def write(self):
        """
        Writes Coverage object to disk
        """

        coverage = self._construct_coverage()
        if self.tiled:
            self.save_covjson_tiled(coverage, self.output_name)
        else:
            self._save_covjson(coverage, self.output_name)


    def _construct_coverage(self):
        """
        Constructs Coverage object from constituent parts
        :return: coverage object
        """
        coverage = Coverage(self._construct_domain(), self._construct_range(
        ), self._construct_params(), self._construct_refs()).to_dict()
        return coverage

    def _construct_domain(self):
        """
        Constructs Domain object, populates with values
        :return: domain object
        """

        domain_type = 'Grid'
        x_values = self.Reader.get_x().flatten().tolist()
        y_values = self.Reader.get_y().flatten().tolist()
        t_values = []
        z_values = []

        if 't' in self.axis_list:

            t_values = self.Reader.get_t()

        if 'z' in self.axis_list:

            z_values = self.Reader.get_z().flatten().tolist()

        domain = Domain(domain_type, x_values, y_values, z_values, t_values)

        return domain

    def _construct_params(self):
        """
        Construct parameter object from constituent parts
        :return: Parameter object
        """
        for variable in self.vars_to_write:
            description = self.Reader.get_std_name(variable)
            unit = self.Reader.get_units(variable)
            symbol = self.Reader.dataset[variable].units
            label = self.Reader.dataset[variable].long_name
            params = Parameter(description=description, variable_name=variable,
                               symbol=symbol, unit=unit, observed_property=label)

        return params

    def _construct_refs(self):
        """
        Construct reference object
        :return: refs
        """
        refs = Reference(self.ref_list)

        return refs

    def _construct_range(self):
        """
       Construct range object
       :return: range
       """
        for variable in self.vars_to_write:
            print("wrote variable:", variable)

            axis_names = list(map(str.lower, list(self.Reader.get_axis(variable))))

            if self.tiled:
                tile_set_obj = TileSet(self.tile_shape, self.urlTemplate)
                variable_type = self.Reader.get_type(variable)
                variable_shape = self.Reader.get_shape(variable)
                print('Variable shape:', variable_shape)

                count = 0
                for tile in tile_set_obj.get_tiles(self.tile_shape, self.Reader.dataset[variable].values):
                    count += 1
                    range = {'ranges': Range('NdArray', data_type=variable_type, axes=tile[
                                             1], shape=variable_shape, values=tile[0].flatten().tolist()).to_dict()}
                    self.save_covjson_range(range, str(count) + '.covjson')
                url_template = tile_set_obj.generate_url_template(base_url='localhost:8080',
                    axis_names=['t'])
                tileset = TileSet(variable_shape, url_template).create_tileset(self.tile_shape)

                range = Range('TiledNdArray', data_type=variable_type, variable_name=variable,
                              axes=axis_names, tile_sets=tileset, shape=variable_shape)
                return range
            else:

                shape = self.Reader.get_shape(variable)
                values = self.Reader.get_values(variable).flatten().tolist()
                data_type = self.Reader.get_type(variable)
                axes = self.Reader.get_axis(variable)
                range = Range(range_type='NdArray',  data_type=data_type, values=values, shape=shape,
                              variable_name=variable, axes=axis_names)

                return range

    # Adapted from
    # https://github.com/the-iea/ecem/blob/master/preprocess/ecem/util.py -
    # letmaik
    @staticmethod
    def _save_json(self, obj, path, **kw):
        """Save json object to disk"""
        with open(path, 'w') as fp:
            print("Converting....")
            start = time.clock()
            jsonstr = json.dumps(obj, fp, cls=CustomEncoder, **kw)
            fp.write(jsonstr)
            stop = time.clock()
            print("Completed in: '%s' seconds." % (stop - start))

    def _save_covjson(self, obj, path):
        """
        Skip indentation of certain fields to make JSON more compact but still human readable
        :param obj:
        :param path:

        """

        for axis in obj['domain']['axes'].values():
            self.compact(axis, 'values')
        for ref in obj['domain']['referencing']:
            self.no_indent(ref, 'coordinates')
        for range in obj['ranges'].values():
            self.no_indent(range, 'axisNames', 'shape')
            self.compact(range, 'values')
        self.save_json(obj, path, indent=2)

    def save_covjson_tiled(self, obj, path):
        """
              Skip indentation of certain fields to make JSON more compact but still human readable
              :param obj:
              :param path:

              """

        for axis in obj['domain']['axes'].values():
            self.compact(axis, 'values')
        for ref in obj['domain']['referencing']:
            self.no_indent(ref, 'coordinates')

        self.save_json(obj, path, indent=2)

    @staticmethod
    def save_json(self, obj, path, **kw):
        with open(path, 'w') as fp:
            print("Converting....")
            start = time.clock()
            jsonstr = json.dumps(obj, fp, cls=CustomEncoder, **kw)
            fp.write(jsonstr)
            stop = time.clock()
            print("Completed in: '%s' seconds." % (stop - start))

    def save_covjson_range(self, obj, path):
        for range in obj['ranges'].values():
            self.no_indent(range, 'axisNames', 'shape')
            self.compact(range, 'values')
        self.save_json(obj, path, indent=2)

    @staticmethod
    def compact(self, obj, *names):
        for name in names:
            obj[name] = Custom(obj[name], separators=(',', ':'))

    @staticmethod
    def no_indent(self, obj, *names):
        for name in names:
            obj[name] = Custom(obj[name])


# From http://stackoverflow.com/a/25935321
class Custom(object):

    def __init__(self, value, **custom_args):
        self.value = value
        self.custom_args = custom_args


class CustomEncoder(json.JSONEncoder):
    """Custom Json Encoder class - Allows Json to be saved using custom format (no_indent, compact)"""

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
