from netCDF4 import Dataset, num2date

import datetime
import numpy
import re

class ReadNetCDF(object):
    ncdf_file = ''

    def __init__(self, ncdf_file):
        self.netcdf_file = ncdf_file
        self.dataset = Dataset(self.netcdf_file, 'r')
        self.var_names = self.get_var_names(self.dataset)
        print(self.netcdf_file)

    def get_var_names(self, dataset):
        try:
            variable_names = [var for var in dataset.variables]
            return variable_names
        except Exception as e:
            print("Failed", e)
            return None

    def get_shape(self,variable):
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

    def is_y(self,var):
        """
        Detect whether or not specified variable is a y coord
        :param var:
        :return: Boolean value
        """
        y_list = ['lat', 'latitude', 'LATITUDE', 'Latitude', 'y']
        if self.get_units(var) == 'degrees_north':
            return True
        elif self.get_name(var) in y_list:
            return True
        else:
            return False

    def is_x(self,var):
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
            if (self.get_units(var) in time_list): return True
            if (self.get_name in time_list): return True
            if (var in time_list):
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

    def get_type(self,variable):
        """
        :param dset: NetCDF dataset object
        :param variable: Specified
        :return: var_type with digits stripped
        """
        try:
            var_type = str(self.dataset.variables[variable].dtype)

            return re.sub(r'[0-9]+', '', var_type)

        except Exception as e:
            return None

    def get_dimensions(self,variable):
        """
        Return dimension of specified variable
        :param variable: Input variable
        :return: Tuple - Array dimension of specified variable
        """
        try:
            var_dimension = self.dataset.variables[variable].dimensions
            return var_dimension
        except:
            return None

    def get_std_name(self,variable):
        """

        :param variable: input variable
        :return: standard_name
        """
        try:
            std_name = self.dataset.variables[variable].standard_name
            return std_name
        except:
            return None

    def get_description(self,variable):
        """

        :param variable: input variable
        :return: long_name
        """
        try:
            return self.dataset.variables[variable].long_name
        except:
            return None

    def get_name(self,variable):
        """

        :param variable: input variable
        :return: name - string
        """
        try:
            return self.dataset.variables[variable].name
        except:
            return None

    def get_units(self,variable):
        """
        Return
        :param variable:
        :return: units
        """
        try:
            units = self.dataset.variables[variable].units
            return units
        except:
            return None

    def get_metadata(self,variable):
        """
        Returns metadata for a specified variable

        :param variable: Name of specified
        :return: dset.variables[variable]
        """
        return self.dataset.variables[variable]

    def get_var_group(self,variable):
        """

        :param variable:
        :return: Group that specifed variable belongs to
        """
        return self.dataset.variables[variable].group()

    def convert_time(self, t_variable):
        """
        Formats time objects to CovJSON compliant strings
        :param t_variable:
        :return: list of datetime strings
        """
        date_list = []
        times = self.dataset.variables[t_variable][:]
        units = self.dataset.variables[t_variable].units
        cal = self.dataset.variables[t_variable].calendar
        dates = (num2date(times[:], units=units, calendar=cal)).tolist()
        for date in dates:
            date_list.append(date.strftime('%Y-%m-%dT%H:%M:%SZ'))

        # date_list = [dates.stfrtime('%Y-%m-%dT:%H') for date in dates]
        return date_list

    def extract_var_data(self, var_names):

        """
        Returns dictionary containing the values in each variable specified in the variable list
        :type var_names: object
        :return variable_dict - Dictionary containing key-val pairs
        """
        variable_dict = {}  # Declaring dictionary used to store key-val pairs, var_name as key and the array as the value
        try:
            for var in var_names:
                variable_dict[var] = self.dataset.variables[var][:]
            return variable_dict
        except Exception as e:
            print("An Error occured:", e)
            raise e

    def group_vars(self, var_names):
        dim_list = []
        for var in var_names:
            dim_list.append(self.get_dimensions(var))
        return dim_list

    def get_attr_names(self, variable):
        try:
            return self.dataset[variable].ncattrs()
        except:
            return None



