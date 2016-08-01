"""Simple nosetests
"""

import readers.covjson

def testReadGrid():
    """Tests reading gridcov.json
    """
    #TODO: this only works if we run from the root of the repository
    #Can we make the file paths relative to this script?
    with open('pycovjson/test/testdata/gridcov.json', 'r') as myfile:
        data = myfile.read()
    cov = readers.covjson.loadCoverage(data)
    assert len(cov.domain.axes['y']) == 2
