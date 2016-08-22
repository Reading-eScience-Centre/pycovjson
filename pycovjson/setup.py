import os.path
from setuptools import find_packages, setup

# Package data
# ------------
_author       = 'rileywilliams'
_authorEmail  = 'resc@reading.ac.uk'
_classifiers  = [
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'Development Status :: 4 - Beta',
    'License :: Copyright :: University of Reading',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries :: Python Modules',
]
_description  = 'Create CovJSON files from common scientific data formats'
_downloadURL  = 'http://pypi.python.org/pypi/pycovjson/'
_requirements = ["xarray", "netCDF4","numpy"]
_keywords     = ['dataset', 'coverage', 'covjson']
_license      = 'Copyright :: University of Reading'
_long_description    = 'A python utility library for creating CovJSON files from common scientific data formats'
_name         = 'pycovjson'
_namespaces   = []
_testSuite    = 'pycovjson.test'
_url          = 'https://github.com/Reading-eScience-Centre/pycovjson'
_version      = '0.1.0'
_zipSafe      = True

# Setup Metadata
# --------------

def _read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

_header = '*' * len(_name) + '\n' + _name + '\n' + '*' * len(_name)

setup(
    author=_author,
    author_email=_authorEmail,
    classifiers=_classifiers,
    description=_description,
    download_url=_downloadURL,
    include_package_data=True,
    install_requires=_requirements,
    keywords=_keywords,
    license=_license,
    long_description=_long_description,
    name=_name,
    namespace_packages=_namespaces,
    packages=find_packages(),
    test_suite=_testSuite,
    url=_url,
    version=_version,
    zip_safe=_zipSafe,
)
