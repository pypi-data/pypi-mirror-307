from attrs import define,field,asdict
from pprint import pformat
from typing import Iterable
import cmocean
import copy
import pandas as pd

from gerg_plotting.data_classes.NonSpatialInstruments import Variable


@define(slots=False)
class SpatialInstrument:
    # Dims
    lat: Iterable|Variable|None = field(default=None)
    lon: Iterable|Variable|None = field(default=None)
    depth: Iterable|Variable|None = field(default=None)
    time: Iterable|Variable|None = field(default=None)
    
    # Custom variables dictionary to hold dynamically added variables
    custom_variables: dict = field(factory=dict)

    def __attrs_post_init__(self):
        self._init_dims()
        self._format_datetime()

    def copy(self):
        self_copy = copy.deepcopy(self)
        return self_copy
    
    def slice_var(self,var:str,slice:slice):
        return self[var].data[slice]

    def _has_var(self, key):
        return key in asdict(self).keys() or key in self.custom_variables
    
    def _get_vars(self):
        vars = list(asdict(self).keys()) + list(self.custom_variables.keys())
        vars = [var for var in vars if var!='custom_variables']
        return vars

    def __getitem__(self, key):
        """Allows accessing standard and custom variables via indexing."""
        if isinstance(key,slice):
            self_copy = self.copy()
            for var_name in self._get_vars():
                if isinstance(self_copy[var_name],Variable):
                    self_copy[var_name].data = self.slice_var(var=var_name,slice=key)
            return self_copy
        elif self._has_var(key):
            return getattr(self, key, self.custom_variables.get(key))
        raise KeyError(f"Variable '{key}' not found. Must be one of {self._get_vars()}")    

    def __setitem__(self, key, value):
        """Allows setting standard and custom variables via indexing."""
        if self._has_var(key):
            if key in asdict(self):
                setattr(self, key, value)
            else:
                self.custom_variables[key] = value
        else:
            raise KeyError(f"Variable '{key}' not found. Must be one of {self._get_vars()}")
            
    def __repr__(self):
        '''Pretty printing'''
        return pformat(asdict(self),width=1)
    
    def _init_dims(self):
        self._init_variable(var='lat', cmap=cmocean.cm.haline, units='°N', vmin=None, vmax=None)
        self._init_variable(var='lon', cmap=cmocean.cm.thermal, units='°E', vmin=None, vmax=None)
        self._init_variable(var='depth', cmap=cmocean.cm.deep, units='m', vmin=None, vmax=None)
        self._init_variable(var='time', cmap=cmocean.cm.thermal, units=None, vmin=None, vmax=None)

    def _init_variable(self, var: str, cmap, units, vmin, vmax):
        """Initializes standard variables if they are not None and of type np.ndarray."""
        if self._has_var(var):
            if not isinstance(self[var],Variable):
                if self[var] is not None:    
                    self[var] = Variable(
                        data=self[var],
                        name=var.capitalize(),
                        cmap=cmap,
                        units=units,
                        vmin=vmin,
                        vmax=vmax
                    )
        else:
            raise ValueError(f'{var.capitalize()} does not exist, try using the add_custom_variable method')
        
    def _format_datetime(self):
        if self.time is not None:
            if self.time.data is not None:
                self.time.data = self.time.data.astype('datetime64')

    def add_custom_variable(self, variable: Variable):
        """Adds a custom Variable object and makes it accessible via both dot and dict syntax."""
        if not isinstance(variable, Variable):
            raise TypeError(f"The provided object is not an instance of the Variable class.")
        
        if hasattr(self, variable.name):
            raise AttributeError(f"The variable '{variable.name}' already exists.")
        else:
            # Add to custom_variables and dynamically create the attribute
            self.custom_variables[variable.name] = variable
            setattr(self, variable.name, variable)

    def remove_custom_variable(self,variable_name):
        '''Removes a custom variable'''
        delattr(self,variable_name)

