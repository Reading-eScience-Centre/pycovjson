"""Simple nosetests
"""

import readers.covjson as reader
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "testdata")

def testReadGrid():
    """Tests reading gridcov.json
    """
    #TODO: this only works if we run from the root of the repository
    #Can we make the file paths relative to this script?
    with open(os.path.join(DATA_PATH, "gridcov.json"), 'r') as myfile:
        data = myfile.read()
    cov = reader.loadCoverage(data)
    assert len(cov.domain.axes['y']) == 2
