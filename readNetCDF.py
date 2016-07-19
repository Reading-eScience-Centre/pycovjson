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
print(dset)


def get_var_names(dset):
    var_names = [var for var in dset.variables]
    return var_names

var_names = get_var_names(dset)
# print('Variables:\n' , var_names)
print('\n')

def get_shape(variable):

    shape = dset[variable].shape

    if len(shape) > 1:
        for val in shape:
            shape_list = val

        return shape_list
    else:
        shape = shape[0]

    return shape

def get_type(variable):
    """


    :param dset: NetCDF dataset object
    :param variable: Specified
    :return:
    """

    # var_type = dset.variables[variable].values()
    var_type = dset.variables[variable][0].dtype

    return var_type

def get_dimension(variable):
    """
    Return dimension of specified variable
    :param variable: Input variable
    :return: Tuple - Array dimension of specified variable
    """
    var_dimension = dset.variables[variable].dimensions
    return var_dimension


def extract_var_data(var_names):

    """

    :type var_names: object
    :return variable_dict - Dictionary containing key-val pairs
    """
    variable_dict = {} #Declaring dictionary used to store key-val pairs, var_name as key and the array as the value
    for var in var_names:
        variable_dict[var] = dset.variables[var][:] #Adding values to dict, [:] copies entire array
        #print(var) Debug

    return variable_dict

