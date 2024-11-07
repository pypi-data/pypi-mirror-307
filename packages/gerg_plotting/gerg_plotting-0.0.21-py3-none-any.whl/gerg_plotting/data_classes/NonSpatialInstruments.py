from attrs import define,field,validators,asdict
from matplotlib.colors import Colormap
from typing import Iterable

from gerg_plotting.utils import lat_min_smaller_than_max,lon_min_smaller_than_max,is_flat_numpy_array,to_numpy_array
from gerg_plotting.data_classes.NonSpatialInstrument import NonSpatialInstrument

@define
class Variable(NonSpatialInstrument):
    data:Iterable = field(converter=to_numpy_array,validator=is_flat_numpy_array)
    name:str
    cmap:Colormap = field(default=None)
    units:str = field(default=None)  # Turn off units by passing/assigning to None
    vmin:float = field(default=None)
    vmax:float = field(default=None)
    label:str = field(default=None)  # Set label to be used on figure and axes, use if desired


    def get_attrs(self):
        return list(asdict(self).keys())

    def get_label(self):
        '''Assign the label if it was not passed'''
        if self.label is None:
            # Define the units that are added to the label
            # if the units are defined, we will use them, else it will be an empty string
            unit = f" ({self.units})" if self.units is not None else ''
            # The label is created from the name of the variable with the units
            self.label = f"{self.name}{unit}"
        return self.label

@define
class Bounds(NonSpatialInstrument):
    '''
    depth_bottom: positive depth example: 1000
    depth_top:positive depth example for surface: 0
    '''
    lat_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lat_min_smaller_than_max])
    lat_max:float|int|None = field(default=None)
    
    lon_min:float|int|None = field(default=None,validator=[validators.instance_of(float|int|None),lon_min_smaller_than_max])
    lon_max:float|int|None = field(default=None)

    depth_bottom:float|int|None = field(default=None)
    depth_top:float|int|None = field(default=None)