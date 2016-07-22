#Adapted from letmaik
import uuid
import json
import os.path
from collections import OrderedDict

PATH_DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
PATH_GENERATED = os.path.join(os.path.dirname(__file__), '..', 'generated')
PATH_APP_DATA = os.path.join(os.path.dirname(__file__), '..', '..', 'public', 'app', 'data')



def save_json(obj, path, **kw):
  with open(path, 'w') as fp:
    jsonstr = json.dumps(obj, fp, cls=CustomEncoder, **kw)
    fp.write(jsonstr)
    
def save_covjson(obj, path):
  # skip indentation of certain fields to make it more compact but still human readable
  for axis in obj['domain']['axes'].values():
    compact(axis, 'values')
  for ref in obj['domain']['referencing']:
    no_indent(ref, 'components')
  for range in obj['ranges'].values():
    no_indent(range, 'axisNames', 'shape')
    compact(range, 'values')
  save_json(obj, path, indent=2)

def minify_json (path):
  with open(path, 'r') as fp:
    jsonstr = fp.read()
  with open(path, 'w') as fp:
    json.dump(json.loads(jsonstr, object_pairs_hook=OrderedDict), fp, separators=(',', ':'))

def compact(obj, *names):
  for name in names:
    obj[name] = Custom(obj[name], separators=(',', ':'))

def no_indent(obj, *names):
  for name in names:
    obj[name] = Custom(obj[name])

# adapted from http://stackoverflow.com/a/25935321  
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
      