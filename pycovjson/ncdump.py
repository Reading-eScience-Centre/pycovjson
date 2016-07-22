from netCDF4 import Dataset

file_path = 'foam_2011-01-01.nc'

ncdf_dataset = Dataset(file_path, 'r')
def ncdump(ncdf_dataset, output=True):

    if output == True:
        print_attributes()
    def print_attributes(key):
        nc_vars = [var for var in ncdf_dataset.variables]
        print(nc_vars)





ncdump(ncdf_dataset)