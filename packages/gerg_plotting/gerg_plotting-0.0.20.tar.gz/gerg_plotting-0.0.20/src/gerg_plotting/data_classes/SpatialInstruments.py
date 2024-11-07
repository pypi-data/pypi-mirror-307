import matplotlib.figure
import numpy as np
import pandas as pd
from attrs import define,field,asdict
import matplotlib
import matplotlib.axes
import matplotlib.pyplot
import matplotlib.colorbar
from matplotlib.colors import Colormap
import xarray as xr
from pathlib import Path
import cmocean
from typing import Iterable

from gerg_plotting.utils import get_center_of_mass,colorbar
from gerg_plotting.data_classes.SpatialInstrument import SpatialInstrument
from gerg_plotting.data_classes.NonSpatialInstruments import Bounds, Variable

@define(repr=False)
class Bathy(SpatialInstrument):
    # Vars
    bounds:Bounds = field(default=None)
    resolution_level:float|int|None = field(default=5)
    contour_levels:int = field(default=50)
    land_color:list = field(default=[231/255,194/255,139/255,1])
    vmin:int|float = field(default=0)
    cmap:Colormap = field(default=matplotlib.colormaps.get_cmap('Blues'))
    cbar_show:bool = field(default=True)
    cbar:matplotlib.colorbar.Colorbar = field(init=False)
    cbar_nbins:int = field(default=5)
    cbar_kwargs:dict = field(default={})
    vertical_scaler:int|float = field(default=None)
    vertical_units:str = field(default='')
    center_of_mass:tuple = field(init=False)

    def __attrs_post_init__(self):
        self.get_bathy()
        if self.vertical_scaler is not None:
            self.depth = self.depth*self.vertical_scaler
        self.center_of_mass = get_center_of_mass(self.lon,self.lat,self.depth)
        self.adjust_cmap()
        
    def adjust_cmap(self):
        # Remove the white most but of the colormap
        self.cmap = cmocean.tools.crop_by_percent(self.cmap,20,'min')
        # Add land color to the colormap
        self.cmap.set_under(self.land_color)

    def get_bathy(self):
        '''
        bounds (Bounds): contains attributes of lat_min,lon_min,lat_max,lon_max,depth_max,depth_min
        resolution_level (float|int): how much to coarsen the dataset by in units of degrees
        '''
        self_path = Path(__file__).parent
        seafloor_path = self_path.parent.joinpath('seafloor_data/gebco_2023_n31.0_s7.0_w-100.0_e-66.5.nc')
        ds = xr.open_dataset(seafloor_path) #read in seafloor data

        ds = ds.sel(lat=slice(self.bounds["lat_min"],self.bounds["lat_max"])).sel(lon=slice(self.bounds["lon_min"],self.bounds["lon_max"])) #slice to the focus area

        if self.resolution_level is not None:
            ds = ds.coarsen(lat=self.resolution_level,boundary='trim').mean().coarsen(lon=self.resolution_level,boundary='trim').mean() #coarsen the seafloor data (speed up figure drawing) #type:ignore

        self.depth = ds['elevation'].values*-1 #extract the depth values and flip them
    
        if self.bounds["depth_top"] is not None:
            self.depth = np.where(self.depth>self.bounds["depth_top"],self.depth,self.bounds["depth_top"]) #set all depth values less than the depth_top to the same value as depth_top for visuals
        if self.bounds["depth_bottom"] is not None:
            self.depth = np.where(self.depth<self.bounds["depth_bottom"],self.depth,self.bounds["depth_bottom"]) #set all depth values less than the depth_bottom to the same value as depth_bottom for visuals

        self.lon = ds.coords['lat'].values #extract the latitude values
        self.lat = ds.coords['lon'].values #extract the longitude values
        self.lon, self.lat = np.meshgrid(self.lat, self.lon) #create meshgrid for plotting
    
    def add_colorbar(self,fig:matplotlib.figure.Figure,divider,mappable:matplotlib.axes.Axes,nrows:int) -> None:
        if self.cbar_show:
            label = 'Bathymetry (m)'
            self.cbar = colorbar(fig,divider,mappable,label,nrows=nrows)
            self.cbar.ax.locator_params(nbins=self.cbar_nbins)
            self.cbar.ax.invert_yaxis()
            return self.cbar


@define(slots=False,repr=False)
class Data(SpatialInstrument):
    # Vars
    temperature: Iterable|Variable|None = field(default=None)
    salinity: Iterable|Variable|None = field(default=None)
    density: Iterable|Variable|None = field(default=None)
    u: Iterable|Variable|None = field(default=None)
    v: Iterable|Variable|None = field(default=None)
    speed: Iterable|Variable|None = field(default=None)

    def __attrs_post_init__(self):
        super().__attrs_post_init__()
        self._init_variables()  # Init variables

    def _init_variables(self):
        '''Default Variable initialization.
        If you would like a new variable to be included in the default init, contact the repo manager'''
        self._init_variable(var='temperature', cmap=cmocean.cm.thermal, units='°C', vmin=-10, vmax=40)
        self._init_variable(var='salinity', cmap=cmocean.cm.haline, units=None, vmin=28, vmax=40)
        self._init_variable(var='density', cmap=cmocean.cm.dense, units="kg/m\u00B3", vmin=1020, vmax=1035)
        self._init_variable(var='u', cmap=cmocean.cm.balance, units="m/s", vmin=-5, vmax=5)
        self._init_variable(var='v', cmap=cmocean.cm.balance, units="m/s", vmin=-5, vmax=5)
        self._init_variable(var='speed', cmap=cmocean.cm.speed, units="m/s", vmin=0, vmax=5)

