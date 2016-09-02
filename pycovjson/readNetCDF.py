#pycovjson - Utility to convert NetCDF data to CoverageJSON format.
#Version 0.1 Riley Williams 11/07/16 - WORK IN PROGRESS

from netCDF4 import Dataset, num2date

import datetime
import numpy
import re


#Define dataset

def get_user_selection():
    file_dict = {}
    file_dict[0] = 'foam_2011-01-01.nc'
    file_dict[1] = 'melodies_lc-latlon.nc'
    file_dict[2] = 'simple_xyz.nc'
    file_dict[3] = 'polcoms_irish_hourly_20090320.nc'
    print(file_dict)
    selection = int(input("Enter the number of the file you would like to use:"))
    return file_dict[selection]




def load_netcdf(ncdf_file):
    try:
        dset = Dataset(ncdf_file, 'r')
        return dset
    except Exception as e:
        print("An error has occured", e)



def get_var_names(dset):
    try:
        var_names = [var for var in dset.variables]
        return var_names
    except Exception as e:
        print("Failed", e)
        return None



def get_shape(variable):
    """
    Get shape of specifed variable, as list
    :param variable: String specifying variable name
    :return: shape_list - List containing shape of specified variable
    """
    shape = dset[variable].shape
    shape_list = []

    if len(shape) > 1:
        for val in shape:
            shape_list.append(val)
    else:
        shape_list.append(shape[0])

    return shape_list


def is_y(var):
    """
    Detect whether or not specified variable is a y coord
    :param var:
    :return: Boolean value
    """
    y_list = ['lat', 'latitude', 'LATITUDE','Latitude', 'y']
    if get_units(var) == 'degrees_north':
        return True
    elif get_name(var) in y_list:
        return True
    else:
        return False


def is_x(var):
    """
    Detect whether or not specified variable is an x coord
    :param var:
    :return: Boolean value
    """
    x_list = ['lon', 'longitude', 'LONGITUDE','Longitude', 'x']


    if get_units(var) == 'degrees_east':

        return True
    if get_name(var) in x_list:
        return True
    if get_description(var) in x_list:
        return True
    else:
        return False

def has_time():
    time_list = ['t', 'TIME', 'time', 's', 'seconds', 'Seconds',]
    for var in var_names:
        if (get_units(var) in time_list):return True
        if (get_name in time_list): return True
        if (var in time_list): return True
        else: return False

def get_time():
    time_list = ['t', 'TIME', 'time', 's', 'seconds', 'Seconds']
    time_dict ={}
    for var in var_names:
        if get_units(var) in time_list or get_name(var) in time_list:
            time_dict[var] = True
            if len(get_shape(var)) == 1:
                time_var = var
            else: return False
    return  time_var

def get_type(variable):
    """
    :param dset: NetCDF dataset object
    :param variable: Specified
    :return: var_type with digits stripped
    """
    try:
        var_type = str(dset.variables[variable].dtype)

        return re.sub(r'[0-9]+', '', var_type)

    except Exception as e:
        return None


def get_dimensions(variable):
    """
    Return dimension of specified variable
    :param variable: Input variable
    :return: Tuple - Array dimension of specified variable
    """
    try:
        var_dimension = dset.variables[variable].dimensions
        return var_dimension
    except:
        return None

def get_std_name(variable):
    """

    :param variable: input variable
    :return: standard_name
    """
    try:
        std_name = dset.variables[variable].standard_name
        return std_name
    except: return None
def get_description(variable):
    """

    :param variable: input variable
    :return: long_name
    """
    try:
        return dset.variables[variable].long_name
    except:
        return None

def get_name(variable):
    """

    :param variable: input variable
    :return: name - string
    """
    try:
        return dset.variables[variable].name
    except:
        return None


def get_units(variable):
    """
    Return
    :param variable:
    :return: units
    """
    try:
        units = dset.variables[variable].units
        return units
    except:
        return None



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
    """
    Formats time objects to CovJSON compliant strings
    :param t_variable:
    :return: list of datetime strings
    """
    date_list =[]
    times = dset.variables[t_variable][:]
    units = dset.variables[t_variable].units
    cal = dset.variables[t_variable].calendar
    dates = (num2date(times[:], units=units, calendar=cal)).tolist()
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
    try:
        for var in var_names:
            variable_dict[var] = dset.variables[var][:]
        return variable_dict
    except Exception as e:
        print("An Error occured:", e)
        raise e



def group_vars(var_names):
    dim_list =[]
    for var in var_names:
      dim_list.append(get_dimensions(var))
    return dim_list


def get_attr_names(variable):
    try:
        return dset[variable].ncattrs()
    except:
        return None
if __name__ == '__main__':

    #Main
    Debug = False
    if not Debug:
        ncdf_file = get_user_selection()
    else:
        ncdf_file = 'foam_2011-01-01.nc'
    dset = load_netcdf(ncdf_file)
    var_names = get_var_names(dset)
