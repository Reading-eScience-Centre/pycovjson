from pycovjson.read_netcdf import NetCDFReader as Reader
from pycovjson.write import Writer
from pycovjson.model import TileSet

def main(input_file, output_file, variable, tiled=False, tile_shape=[], axis=''):


    if output_file == None:
        output_file = 'coverage.json'


    def tile_by_axis(variable, axis):
        """

        :param variable:
        :param axis:
        :return: tile_shape
        """
        # Get shape of variable
        shape = Reader.get_shape(variable)
        # Set axis to slice by to 1
        TileSet.create_tileset()
        # Generate new tile shape
        return tile_shape
    if tiled:
        tile_shape = tile_by_axis(variable, axis)

    Writer(output_file, input_file, [variable], tiled=tiled, tile_shape=tile_shape).write()


if __name__ == '__main__':
    main()


