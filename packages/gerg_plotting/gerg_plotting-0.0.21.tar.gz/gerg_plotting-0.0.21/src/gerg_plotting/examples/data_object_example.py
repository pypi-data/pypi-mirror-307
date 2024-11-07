from gerg_plotting import Data,Variable,Bounds
from gerg_plotting.utils import generate_random_point

import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import cmocean

# We will create a few Data objects below using various methods

# Let's read in the example data
df = pd.read_csv('example_data/sample_glider_data.csv',parse_dates=['time'])
n_points = len(df)

lats = df['latitude']
lons = df['longitude']
depth = df['pressure']
time = df['time']
salinity = df['salinity']
temperature = df['temperature']
density = df['density']



# Method 1: Using Iterables

# Here is the initialization of the Data object used for plotting using pandas.Series objects as the inputs
# To use this method you must use one of the default variables, there is another method for adding non-default/custom variables
data = Data(lat=df['latitude'],lon=df['longitude'],depth=df['pressure'],time=df['time'],
            salinity=df['salinity'],temperature=df['temperature'],density=df['density'])
# Here is an example using numpy arrays:
data = Data(lat=lats,lon=lons,depth=depth,time=time,salinity=salinity,temperature=temperature,density=density)



# Method 2: Using Variable Objects

# There is a bit more to do before we can initialize the Data object
# This way we can be clear with our variable creation

# Let's initialize the Variable objects
lat_var = Variable(data = lats,name='lat', cmap=cmocean.cm.haline, units='°N', vmin=None, vmax=None)
lon_var = Variable(data = lons,name='lon', cmap=cmocean.cm.thermal, units='°W', vmin=None, vmax=None)
depth_var = Variable(data = depth,name='depth', cmap=cmocean.cm.deep, units='m', vmin=None, vmax=None)
time_var = Variable(data = time,name='time', cmap=cmocean.cm.thermal, units=None, vmin=None, vmax=None)

temperature_var = Variable(data = temperature,name='temperature', cmap=cmocean.cm.thermal, units='°C', vmin=-10, vmax=40)
salinity_var = Variable(data = salinity,name='salinity', cmap=cmocean.cm.haline, units=None, vmin=28, vmax=40)
density_var = Variable(data = density,name='density', cmap=cmocean.cm.dense, units="kg/m\u00B3", vmin=1020, vmax=1035)

# Now that we have our Variables we can initialize the Data object just like before
data = Data(lat=lat_var,lon=lon_var,depth=depth_var,time=time_var,
            temperature=temperature_var,salinity=salinity_var,density=density_var)


# You can see that there are a few attributes in the Variable object
print(data['lat'].get_attrs())
# To change any attribute of any variable just reassign after the init like this:
data['lat'].vmin = 27
data['depth'].units = 'km'
# or like this:
data.lat.vmin = 27
data.depth.units = 'km'
# You can even reassign an entire variable like this:
data['lat'] = Variable(data = lats, name='lat', cmap=cmocean.cm.haline, units='°N', vmin=27, vmax=28.5)


# Assigning a variable that is a non-default/custom variable is simple:
# First we must initialize the variable
# Init speed_of_sound Variable object
speed_of_sound = Variable(data=df['speed_of_sound'],name='speed_of_sound',cmap=cmocean.cm.thermal,units='m/s',label='Speed of Sound (m/s)')
# Add the speed_of_sound Variable object to the Data object
data.add_custom_variable(speed_of_sound)

# We need to remove the old custom variable first before reassignment using the add_custom_variable method, otherwise we can use the base assignment methods
data.remove_custom_variable('speed_of_sound')
# We can also add custom variables in one line:
data.add_custom_variable(Variable(data=df['speed_of_sound'],name='speed_of_sound',cmap=cmocean.cm.thermal,units='m/s',label='Speed of Sound (m/s)'))

print(data)