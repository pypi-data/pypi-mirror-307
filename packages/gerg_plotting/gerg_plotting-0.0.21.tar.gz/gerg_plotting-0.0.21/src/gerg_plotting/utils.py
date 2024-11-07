import cartopy.mpl.geoaxes
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
import matplotlib.axes as maxes
import numpy as np
import pandas as pd
import xarray as xr
import gsw
import datetime
import random
import cartopy
from typing import Iterable

def lat_min_smaller_than_max(instance, attribute, value):
    if value is not None:
        if value >= instance.lat_max:
            raise ValueError("'lat_min' must to be smaller than 'lat_max'")
    
def lon_min_smaller_than_max(instance, attribute, value):
    if value is not None:
        if value >= instance.lon_max:
            raise ValueError("'lon_min' must to be smaller than 'lon_max'")
        
def validate_array_lengths(instance,attribute,value):
    lengths = {attr.name:len(getattr(instance,attr.name)) for attr in instance.__attrs_attrs__ if isinstance(getattr(instance,attr.name),np.ndarray)}
    if len(set(lengths.values()))>1:
        raise ValueError(f'All Dims and Vars must be the same length, got lengths of {lengths}')

def to_numpy_array(values:Iterable):
    # Convert iterable types (list, tuple, pandas.Series, etc.) to NumPy array
    if not isinstance(values, np.ndarray):
        array = pd.Series(values).to_numpy()
        return array
    elif isinstance(values, np.ndarray):
        return values
    elif values is None:
        return None
    else:
        raise ValueError(f"Cannot convert {type(value)} to a NumPy array")

def is_flat_numpy_array(instance, attribute, value):
    # Validate that the value is now a NumPy array
    if not isinstance(value, np.ndarray):
        raise ValueError(f"{attribute.name} must be a NumPy array or a list convertible to a NumPy array")
    
    # Ensure the array is flat (1-dimensional)
    if value.ndim != 1:
        raise ValueError(f"{attribute.name} must be a flat array")
    
def generate_random_point(lat_min,lat_max,lon_min,lon_max):
    lat = random.uniform(lat_min, lat_max)
    lon = random.uniform(lon_min, lon_max)
    return [lat, lon]
        
def get_center_of_mass(lon,lat,pressure) -> tuple:
    centroid = tuple([np.nanmean(lon), np.nanmean(lat), np.nanmean(pressure)])
    return centroid

def interp_glider_lat_lon(ds) -> xr.Dataset:
    # Convert time and m_time to float64 for interpolation
    new_time_values = ds['time'].values.astype('datetime64[s]').astype('float64')
    new_mtime_values = ds['m_time'].values.astype('datetime64[s]').astype('float64')

    # Create masks of non-NaN values for both latitude and longitude
    valid_latitude = ~np.isnan(ds['latitude'])
    valid_longitude = ~np.isnan(ds['longitude'])

    # Interpolate latitude based on valid latitude and m_time values
    ds['latitude'] = xr.DataArray(
        np.interp(new_time_values, new_mtime_values[valid_latitude], ds['latitude'].values[valid_latitude]),
        [('time', ds['time'].values)]
    )

    # Interpolate longitude based on valid longitude and m_time values
    ds['longitude'] = xr.DataArray(
        np.interp(new_time_values, new_mtime_values[valid_longitude], ds['longitude'].values[valid_longitude]),
        [('time', ds['time'].values)]
    )

    ds = ds.drop_vars('m_time')

    return ds

def load_example_data():
    df = pd.read_csv('example_data/sample_glider_data.csv',parse_dates=['time'])
    return df

def filter_var(var:pd.Series,min_value,max_value):
    var = var.where(var>min_value)
    var = var.where(var<max_value)
    return var

def calculate_range(var:np.ndarray):
    return [np.nanmin(var),np.nanmax(var)]

def calculate_pad(var:np.ndarray,pad=0.0):
    start, stop = calculate_range(var)
    difference = stop - start
    pad = difference*pad
    start = start-pad
    stop = stop+pad
    start = float(start)
    stop = float(stop)
    return start,stop

def colorbar(fig,divider,mappable,label:str,nrows:int=1,total_cbars:int=2):
    last_axes = plt.gca()
    base_pad = 0.1
    num_colorbars = (len(fig.axes)-nrows)%total_cbars
    pad = base_pad + num_colorbars * 0.6
    cax = divider.append_axes("right", size="4%", pad=pad,axes_class=maxes.Axes)
    cbar = fig.colorbar(mappable, cax=cax,label=label)
    plt.sca(last_axes)
    return cbar

def get_sigma_theta(salinity:np.ndarray,temperature:np.ndarray,cnt:bool=False):
    # Subsample the data
    num_points = len(temperature)
    if num_points>50_000 and num_points<300_000:
        salinity = salinity[::100]
        temperature = temperature[::100]    
    elif num_points>300_000 and num_points<1_000_000:
        salinity = salinity[::250]
        temperature = temperature[::250]
    elif num_points>=1_000_000:
        salinity = salinity[::1000]
        temperature = temperature[::1000]        

    # Remove nan values
    salinity = salinity[~np.isnan(salinity.astype('float64'))]
    temperature = temperature[~np.isnan(temperature.astype('float64'))]

    mint=np.min(temperature)
    maxt=np.max(temperature)

    mins=np.min(salinity)
    maxs=np.max(salinity)

    num_points = len(temperature)

    tempL=np.linspace(mint-1,maxt+1,num_points)

    salL=np.linspace(mins-1,maxs+1,num_points)

    Tg, Sg = np.meshgrid(tempL,salL)
    sigma_theta = gsw.sigma0(Sg, Tg)

    if cnt:
        num_points = len(temperature)
        cnt = np.linspace(sigma_theta.min(), sigma_theta.max(),num_points)
        return Sg, Tg, sigma_theta, cnt
    else:
        return Sg, Tg, sigma_theta


def get_density(salinity,temperature):
    return gsw.sigma0(salinity, temperature)

def print_time(value: int = None, intervals: list = [10,50,100,500,1000]):
    """
    Prints the current time if the value matches any of the intervals specified.

    Args:
    - value (int): The value value.
    - intervals (list): A list of integers representing intervals.

    Returns:
    - None
    """

    current_time = datetime.datetime.now().strftime("%H:%M:%S")

    if value is None:
        print(current_time)
        return

    # Check if intervals is at least 2 values long
    if not len(intervals) >= 2:
        raise ValueError(f'Not enough intervals, need at least 2 values, you passed {len(intervals)}')


    if value <= intervals[0]:
        print(f'{value = }, {current_time}')
        return
    elif value <= intervals[-2]:
        for idx,interval in enumerate(intervals[0:-1]):
            if value >= interval:
                if value < intervals[idx+1]:
                    if value % interval==0:
                        print(f'{value = }, {current_time}')
                        return
                    break
    elif value >= intervals[-1]:
        if value % intervals[-1]==0:
            print(f'{value = }, {current_time}')
            return