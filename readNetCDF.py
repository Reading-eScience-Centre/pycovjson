#pycovjson - Utility to convert NetCDF data to CoverageJSON format.
#Version 0.1 Riley Williams 11/07/16 - WORK IN PROGRESS

from netCDF4 import Dataset

#Define dataset
nc_file = 'foam_2011-01-01.nc'
try:
    dset = Dataset(nc_file, 'r')
    print("Dataset:     " , dset)
except:
    print("An error has occured")

def get_var_names(dset):
    var_names = [var for var in dset.variables]
    return var_names

var_names = get_var_names(dset)
print('Variables:\n' ,get_var_names(dset))
print('\n')

def extract_var_data(var_names):
    #Extracts data from each variable
    variable_list = [] #Need to implement more efficient data structure. Dict or Map? var_name as key
    for var in var_names:
        variable_list.append(dset.variables[var][:]) #Appending to list, [:] copies entire array
        #print(var) Debug

    return variable_list


print("dimensions", dset.variables['lat'])

print(dset)

print(len(extract_var_data(var_names)))
print(extract_var_data(var_names))


#print(dset.variables['ICETK'][:])
#depth = dset.variables['depth'][:]



