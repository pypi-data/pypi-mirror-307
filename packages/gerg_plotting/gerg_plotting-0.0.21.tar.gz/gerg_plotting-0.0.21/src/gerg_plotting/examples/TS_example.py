from gerg_plotting import Data,ScatterPlot
import pandas as pd

# Let's read in the example data
df = pd.read_csv('example_data/sample_glider_data.csv')

data = Data(lat=df['latitude'],lon=df['longitude'],depth=df['pressure'],time=df['time'],
            salinity=df['salinity'],temperature=df['temperature'],density=df['density'])

ScatterPlot(data).TS(contours=True)
