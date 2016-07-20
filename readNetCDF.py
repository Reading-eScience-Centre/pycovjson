#pycovjson - Utility to convert NetCDF data to CoverageJSON format.
#Version 0.1 Riley Williams 11/07/16 - WORK IN PROGRESS

from netCDF4 import Dataset

#Define dataset
nc_file = 'foam_2011-01-01.nc'


def load_netcdf(nc_file):
    try:
        dset = Dataset(nc_file, 'r')
    except:
        print("An error has occured")
    return dset

dset = load_netcdf(nc_file)


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
    shape_list =[]
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
    var_type = dset.variables[variable].datatype
    return var_type

def get_dimensions(variable):
    """
    Return dimension of specified variable
    :param variable: Input variable
    :return: Tuple - Array dimension of specified variable
    """
    var_dimension = dset.variables[variable].dimensions
    return var_dimension


def get_long_name(variable):
    long_name = dset.variables[variable].name
    return long_name


def get_units(variable):
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
    for var in var_names:
        get_dimensions(var)
    return 0


print(dset.variables)
print(get_type('SALTY'))
print(get_dimensions('SALTY'))
print(get_long_name('SALTY'))