#pycovjson - Utility to convert NetCDF data to CoverageJSON format.
#Version 0.1 Riley Williams 11/07/16 - WORK IN PROGRESS

from netCDF4 import Dataset, num2date
import netCDF4 as nc
import datetime
import numpy



#Define dataset
# ncdf_file = 'foam_2011-01-01.nc'


file_dict = {}
file_dict[0] = 'foam_2011-01-01.nc'
file_dict[1] ='melodies_lc-latlon.nc'
file_dict[2] = 'simple_xy.nc'

dset = ''


def get_user_selection(file_dict):
    print(file_dict)
    selection = int(input("Enter the number of the file you would like to use:"))
    return file_dict[selection]

ncdf_file = get_user_selection(file_dict)


def load_netcdf(ncdf_file):
    try:
        dset = Dataset(ncdf_file, 'r')
        return dset
    except Exception as e:
        print("An error has occured", e)


dset = load_netcdf(ncdf_file)
def get_var_names(dset):
    var_names = [var for var in dset.variables]
    return var_names

var_names = get_var_names(dset)


def get_shape(variable):
    """
    Get shape of specifed variable, as list
    :param variable: String specifying variable name
    :return: shape_list - List containing shape of specified variable
    """
    shape = dset[variable].shape
    shape_list = []
    print(len(shape))

    if len(shape) > 1:
        for val in shape:
            shape_list.append(val)
    else:
        shape_list.append(shape[0])

    return shape_list


def get_type(variable):
    """
    :param dset: NetCDF dataset object
    :param variable: Specified
    :return: var_type
    """
    var_type = type(dset.variables[variable].datatype)
    return var_type

def get_dimensions(variable):
    """
    Return dimension of specified variable
    :param variable: Input variable
    :return: Tuple - Array dimension of specified variable
    """
    var_dimension = dset.variables[variable].dimensions
    return var_dimension


def get_std_name(variable):
    std_name = dset.variables[variable].standard_name
    return std_name


def get_units(variable):
    """
    Return
    :param variable:
    :return: units
    """
    units = dset.variables[variable].units
    return units


def get_metadata(variable):
    """
    Returns metadata for a specified variable

    :param variable: Name of specified
    :return: dset.variables[variable]
    """
    return dset.variables[variable]


def get_var_group(variable):
    """

    :param variable:
    :return: Group that specifed variable belongs to
    """
    return dset.variables[variable].group()

def convert_time(t_variable):
    date_list =[]
    times = dset.variables[t_variable][:]
    units = dset.variables[t_variable].units
    cal = dset.variables[t_variable].calendar
    dates = (num2date(times[:], units=units,calendar=cal)).tolist()
    #print('{:%Y%m%d%H}'.format(dates))
    for date in dates:
        date_list.append(date.strftime('%Y-%m-%dT%H:%M:%SZ'))

    #date_list = [dates.stfrtime('%Y-%m-%dT:%H') for date in dates]
    return date_list

def extract_var_data(var_names):

    """
    Returns dictionary containing the values in each variable specified in the variable list
    :type var_names: object
    :return variable_dict - Dictionary containing key-val pairs
    """
    variable_dict = {} #Declaring dictionary used to store key-val pairs, var_name as key and the array as the value
    for var in var_names:
        variable_dict[var] = dset.variables[var][:]
    return variable_dict



def group_vars(var_names):
    dim_list =[]
    for var in var_names:
      dim_list.append(get_dimensions(var))
    return dim_list

def get_var_dimensions():
    return 0

def get_attr_names(variable):
    return dset[variable].ncattrs()



print("ATTR NAMES: ", get_attr_names('ICEC'))
print(dset.variables)
print(group_vars(var_names))
# print(get_type(''))
# print(get_dimensions('SALTY'))
#print(convert_time('time'))
