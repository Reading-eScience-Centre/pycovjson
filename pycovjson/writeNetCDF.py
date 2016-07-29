from netCDF4 import Dataset

from numpy import arange, dtype


nx = 3; ny = 3
ncfile = Dataset('test_xy.nc','w')
# create the output data.
data_out = arange(nx*ny)
data_out.shape = (nx,ny) # reshape to 2d array
# create the x and y dimensions.
ncfile.createDimension('x',nx)
ncfile.createDimension('y',ny)
data = ncfile.createVariable('data',dtype('float32').char,('x','y'))


data[:] = data_out
# close the file.
print(ncfile.variables)
print("Wrote file!")