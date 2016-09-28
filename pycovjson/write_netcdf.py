from netCDF4 import Dataset

from numpy import arange, dtype


nx = 4
ny = 4
nz = 1
ncfile = Dataset('test_xyz.nc', 'w')
# create the output data.
data_out = arange(nx * ny* nz)
print(data_out)
data_out.shape = (nx, ny, nz)  # reshape to 3d array
# create the x and y dimensions.
ncfile.createDimension('x', nx)
ncfile.createDimension('y', ny)
ncfile.createDimension('z', nz)
data = ncfile.createVariable('data', dtype('float32').char, ('x', 'y','z'))

data[:] = data_out
# close the file.
print(ncfile.variables)
print("Wrote file!")
