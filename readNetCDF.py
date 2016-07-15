#pycovjson - Utility to convert NetCDF data to CoverageJSON format.
#Version 0.1 Riley Williams 11/07/16 - WORK IN PROGRESS

from netCDF4 import Dataset

#Define dataset
#nc_file = 'foam_2011-01-01.nc'
nc_file = 'melodies_lc-latlon.nc'


def load_netcdf(nc_file):
    try:
        dset = Dataset(nc_file, 'r')
        # print("Dataset:     ", dset) debug
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

def get_shape(dset, variable):

    shape = dset[variable].shape

    if len(shape) > 1:
        for val in shape:
            shape_list = val

        return shape_list
    else:
        shape = shape[0]

    return shape




def extract_var_data(var_names):
    # Extracts data from each variable
    """

    :type var_names: object
    """
    variable_dict = {} #Declaring dictionary used to store key-val pairs, var_name as key and the array as the value
    for var in var_names:
        variable_dict[var] = dset.variables[var][:] #Adding values to dict, [:] copies entire array
        #print(var) Debug

    return variable_dict

# print(extract_var_data(var_names).get('lat'))
# print("dimensions", dset.variables['lat'])
#
#
# print(load_netcdf(nc_file))
#
# print(len(extract_var_data(var_names)))
# print(extract_var_data(var_names))


#print(dset.variables['ICETK'][:])

