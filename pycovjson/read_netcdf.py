from pycovjson.model import Domain, Range, Parameter, Reference
import xarray as xr
from collections import OrderedDict
import pandas as pd
import numpy as np
import re


class NetCDFReader(object):

    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        try:
            self.dataset = xr.open_dataset(self.dataset_path)

        except OSError:
            print('File not found.')
            exit()

    def read(self, file_path):
        self.file_path = file_path
        self.dataset = xr.open_dataset(self.file_path)
        self.var_names = self.get_var_names(self.dataset)

    def print(self):
        print(self.dataset)
        return self.dataset

    def get_xarray(self):
        self.dataset = xr.open_dataset(self.dataset_path)
        return self.dataset

    def close(self):
        self.dataset.close()

    @staticmethod
    def _get_domain(self):
        domain = Domain('Grid')
        return domain

    @staticmethod
    def _get_ranges(self):
        _range = Range()
        return _range

    @staticmethod
    def _get_params(self):
        params = Parameter()
        return params

    @staticmethod
    def _get_reference(self):
        reference = Reference()
        return reference

    @staticmethod
    def get_var_names(self, dataset):
        try:
            variable_names = [var for var in dataset.variables]
            return variable_names
        except Exception as e:
            print("Failed", e)
            return None

    def get_long_names(self, dataset):
        long_names = []
        for variable in self.get_var_names(dataset):
            try:
                long_names.append(dataset[variable].long_name)
            except:
                long_names.append(dataset[variable].name)
        return long_names

    def get_vars_with_long_name(self, dataset):
        try:
            long_names = self.get_long_names(dataset)
            vars_long_names = list(
                zip(self.get_var_names(dataset), long_names))
            return vars_long_names
        except:
            pass

    def get_shape(self, variable):
        """
        Get shape of specifed variable, as list
        :param variable: String specifying variable name
        :return: shape_list - List containing shape of specified variable
        """
        shape = self.dataset[variable].shape
        shape_list = []

        if len(shape) > 1:
            for val in shape:
                shape_list.append(val)
        else:
            shape_list.append(shape[0])

        return shape_list

    def is_y(self, var):
        """
        Detect whether or not specified variable is a y coord
        :param var:
        :return: Boolean value
        """
        y_list = ['lat', 'latitude', 'LATITUDE', 'Latitude', 'y']
        if self.get_units(var) == 'degrees_north' or self.get_name(var) in y_list:
            return True
        else:
            return False

    def is_x(self, var):
        """
        Detect whether or not specified variable is an x coord
        :param var:
        :return: Boolean value
        """
        x_list = ['lon', 'longitude', 'LONGITUDE', 'Longitude', 'x']

        if self.get_units(var) == 'degrees_east':
            return True
        if self.get_name(var) in x_list:
            return True
        if self.get_description(var) in x_list:
            return True
        else:
            return False

    def has_time(self):
        time_list = ['t', 'TIME', 'time', 's', 'seconds', 'Seconds', ]
        for var in self.var_names:
            if self.get_units(var) in time_list:
                return True
            if self.get_name in time_list:
                return True
            if var in time_list:
                return True
            else:
                return False

    def get_time(self):
        time_list = ['t', 'TIME', 'time', 's', 'seconds', 'Seconds']
        time_dict = {}
        for var in self.var_names:
            if self.get_units(var) in time_list or self.get_name(var) in time_list:
                time_dict[var] = True
                if len(self.get_shape(var)) == 1:
                    time_var = var
                else:
                    return False
        return time_var

    def get_values(self, variable):
        """

        :param variable:
        :return: variable values as ndarray
        """
        x = self.dataset[variable].values
        y = np.where(np.isnan(x), None, x)

        return y

    def get_type(self, variable):
        """
        :param dset: NetCDF dataset object
        :param variable: Specified
        :return: var_type with digits stripped
        """
        try:
            var_type = str(self.dataset[variable].dtype)

            return re.sub(r'[0-9]+', '', var_type)

        except Exception as e:
            raise e

    def get_dimensions(self, variable):
        """
        Return dimension of specified variable.

        :param variable: Input variable
        :return: Tuple - Array dimension of specified variable
        """
        try:
            var_dimension = self.dataset[variable].dims
            return var_dimension
        except:
            print("Error Occurred: No Dimensions detected... Exiting. ")
            exit()

    def get_std_name(self, variable):
        """
        Return standard name of variable.

        :param variable: input variable
        :return: name
        """
        try:
            std_name = self.dataset[variable].name
            return std_name
        except:
            return None

    def get_description(self, variable):
        """

        :param variable: input variable
        :return: long_name
        """
        try:
            return self.dataset[variable].long_name
        except:
            return None

    def get_name(self, variable):
        """

        :param variable: input variable
        :return: name - string
        """
        try:
            return self.dataset[variable].name
        except:
            return None

    def get_units(self, variable):
        """
        Return units of specified variable.
        :param variable:
        :return: units
        """
        try:
            units = self.dataset[variable].units
            return units
        except:
            return None

    def get_metadata(self, variable):
        """
        Returns metadata for a specified variable.

        :param variable: Name of specified
        :return: dset[variable]
        """
        return self.dataset[variable]

    def get_var_group(self, variable):
        """
        Return group which specified variable belongs to.

        :param variable:
        :return: group as string
        :type string
        """
        return self.dataset[variable].group()

    def get_axis(self, variable):
        try:
            axis = self.dataset[variable].axis
            axis = list(map(str.lower, list(axis)))
            return axis
        except:
<<<<<<< HEAD
            print('Warning: Variable ' + str(variable) + ' has no axis attribute. ')
            pass
=======
            print("Error occured: Variable '%s' has no axis attribute" % (variable))
>>>>>>> 1cf81ed12227447eddf8904627cad7ad9c40873d
        try:
            axes_list = []
            axes_dict = self.get_axes()
            for dim in self.dataset[variable].dims:

                index = (list(axes_dict.keys())[
                         list(axes_dict.values()).index(dim)])

                axes_list.append(index)

            return axes_list
        except:
            print('Error in axes_dict')
    def get_dims(self, variable):
        try:
            dims = self.dataset[variable].dims
        except:
            print("Error Occurred: No Dimensions detected... Exiting. ")
            exit()

    def convert_time(self, t_variable):
        """
        Formats time objects to CovJSON compliant strings.

        :param t_variable: Time Variable
        :return: list of formatted datetime strings
        """
        date_list = []
        times = self.dataset[t_variable].values

        for time in times:
            time = pd.to_datetime(str(time))
            date_list.append(time.strftime('%Y-%m-%dT%H:%M:%SZ'))

        return date_list

    def extract_var_data(self, var_names):
        """
        Returns dictionary containing the values in each variable specified in the variable list.

        :type var_names: String
        :param var_names:
        :return variable_dict - Dictionary containing key-val pairs
        """
        variable_dict = {}  # Declaring dictionary used to store key-val pairs, var_name as key and the array as the value
        try:
            for var in var_names:
                variable_dict[var] = self.dataset[var].values
            return variable_dict
        except Exception as e:
            print("An Error occured:", e)
            raise e

    def get_axes(self):

        axes_dict = OrderedDict()
        x_list = ['lon', 'longitude', 'LONGITUDE', 'Longitude', 'x', 'X']
        y_list = ['lat', 'latitude', 'LATITUDE', 'Latitude', 'y', 'Y']
        t_list = ['time', 'TIME', 't', 'T']
        z_list = ['depth', 'DEPTH']
        for coord in self.dataset.coords:
            try:
                if self.dataset[coord].axis == 'T':
                    axes_dict['t'] = coord
                if self.dataset[coord].axis == 'Z':
                    axes_dict['z'] = coord
            except:
                pass

            try:
                if self.dataset[coord].units == 'degrees_north':
                    axes_dict['y'] = coord
                if self.dataset[coord].units == 'degrees_east':
                    axes_dict['x'] = coord
            except:
                pass

            try:
                if self.dataset[coord].name.lower() == 'x':
                    axes_dict['x'] = coord

                if self.dataset[coord].name.lower() == 'y':
                    axes_dict['y'] = coord

                if self.dataset[coord].name.lower() == 'z':
                    axes_dict['z'] = coord
            except:
                pass

            try:
                if self.dataset[coord].positive in ['up', 'down']:
                    axes_dict['z'] = coord
            except:
                pass

<<<<<<< HEAD
            # if coord in x_list or self.dataset[coord].standard_name in x_list: axes_dict['x'] = coord
            # if coord in y_list or self.dataset[coord].standard_name in y_list: axes_dict['y'] = coord
            try:
                if coord in t_list or self.dataset[coord].standard_name  in t_list:
                    axes_dict['t'] = coord
                if coord in z_list or self.dataset[coord].standard_name in z_list:
                    axes_dict['z'] = coord
            except:
                print("Error: DataArray does not include standard name.")
                pass

        if len(axes_dict) < 2:
            print('Error: File does not conform to CF Conventions')
            exit()
=======
            if coord in t_list or self.dataset[coord].name in t_list:
                axes_dict['t'] = coord
            if coord in z_list or self.dataset[coord].name in z_list:
                axes_dict['z'] = coord
>>>>>>> 1cf81ed12227447eddf8904627cad7ad9c40873d

        return axes_dict

    def get_x(self):
        for elem in self.dataset.coords:

            if elem in ['lon', 'longitude', 'LONGITUDE', 'Longitude', 'x', 'X']:
                return self.dataset[elem].values
            try:
                if self.dataset[elem].axis == 'X':
                    return self.dataset[elem].values
                if self.dataset[elem].name in ['lon', 'longitude', 'LONGITUDE', 'Longitude', 'x', 'X']:
                    return self.dataset[elem].values
                if self.dataset[elem].units == 'degrees_east':
                    return self.dataset[elem].values
            except AttributeError:
                pass

    def get_y(self):

        y_var = self.get_axes()['y']
        return self.dataset[y_var].values

    def get_t(self):
        axis_dict = self.get_axes()
        t_var = axis_dict['t']
        return self.convert_time(t_var)

    def get_z(self):

        for elem in self.dataset.coords:
            if type(self.dataset[elem]) in ['numpy.datetime64', 'numpy.datetime32', 'datetime.datetime']:
                return self.dataset[elem].values

            try:
                if self.dataset[elem].axis == 'Z':
                    return self.dataset[elem].values

                if self.dataset[elem].positive in ['down', 'up']:
                    return self.dataset[elem].values

            except:
                raise AttributeError

            if elem in ['z', 'Z', 'depth', 'DEPTH']:
                return self.dataset[elem].values
