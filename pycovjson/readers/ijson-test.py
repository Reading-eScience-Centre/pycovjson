"""Just a test of reading JSON data in a streaming fashion using ijson. Not
   currently used.
"""

import ijson

# Note: to build a numpy array from an iterator:
# def myfunc(n):
#    for i in range(n):
#        yield i**2

# np.fromiter(myfunc(5), dtype=int)

# From http://stackoverflow.com/questions/2641691/building-up-an-array-in-numpy-scipy-by-iteration-in-python

# Problem - what if we haven't parsed the dataType before building the numpy array?
# Of course, if we know the shape in advance we also know the size and can pre-allocate

# And what about parsing axis values, where we don't have an explicit data type?

def load_json(filename):
    with open(filename, 'r') as fd:
        parser = ijson.parse(fd)
        ret = {'builders': {}}
        for prefix, event, value in parser:
            print prefix, event, value
            raw_input("Press Enter to continue...")
            if (prefix, event) == ('builders', 'map_key'):
                buildername = value
                ret['builders'][buildername] = {}
            elif prefix.endswith('.shortname'):
                ret['builders'][buildername]['shortname'] = value

        return ret

if __name__ == "__main__":
    print load_json('gridcov.json')
