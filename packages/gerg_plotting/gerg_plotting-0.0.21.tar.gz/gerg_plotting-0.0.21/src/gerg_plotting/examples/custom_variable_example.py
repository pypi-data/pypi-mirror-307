from gerg_plotting import Data,MapPlot,Bounds,ScatterPlot,Histogram,Variable
import pandas as pd
import cmocean

# Let's read in the example data
df = pd.read_csv('example_data/sample_glider_data.csv')

# Let's initilize the data object
data = Data(lat=df['latitude'],lon=df['longitude'],depth=df['pressure'],time=df['time'],
            salinity=df['salinity'],temperature=df['temperature'],density=df['density'])


# Init speed_of_sound Variable object
speed_of_sound = Variable(data=df['speed_of_sound'],name='speed_of_sound',cmap=cmocean.cm.thermal,units='m/s',label='Speed of Sound (m/s)')
# Add the speed_of_sound Variable object to the Data object
data.add_custom_variable(speed_of_sound)
# Test by plotting a histogram
Histogram(data).plot(var='speed_of_sound')
# Plot hovmoller 
ScatterPlot(data).hovmoller(var='speed_of_sound')
