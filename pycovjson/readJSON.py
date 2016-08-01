"""Test of reading CovJSON data
"""

import readers.covjson

if __name__ == '__main__':
    with open('test/testdata/gridcov.json', 'r') as myfile:
        data = myfile.read()
    cov = readers.covjson.loadCoverage(data)
    print(cov.domain.axes['y'])
    dataset = cov.toXarray()
    print(dataset)
    #print cov.ranges['ICEC']['values'].shape
    dataset['ICEC'].plot()
    import matplotlib.pyplot as plt
    plt.show()
