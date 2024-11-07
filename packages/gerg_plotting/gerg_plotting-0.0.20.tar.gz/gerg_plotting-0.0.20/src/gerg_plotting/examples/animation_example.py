from gerg_plotting import Data,Variable,Histogram,Animator
from gerg_plotting.utils import calculate_range
import numpy as np

n_points = 10000

data = Data(temperature=np.random.normal(28,size=n_points),salinity=np.random.normal(35.25,scale=0.25,size=n_points))
pH = Variable(data=np.random.normal(7.7,scale=0.25,size=n_points),name='pH')
data.add_custom_variable(pH)

temp_range=calculate_range(data['temperature'].data)

def make_hists(sample,data=data):
    '''Plot Histogram based on sample size'''
    data_sample = data[:10*sample+1]  # Slice data
    hist = Histogram(data_sample)  # Init histogram plotter
    hist.plot('temperature',color='g',bins=30,range=(25,31))  # Plot 1-d histogram
    hist.ax.set_ybound(upper=80)  # Set the ybounds maximum to 80 for a clearer plot
    return hist.fig

Animator().animate(plotting_function=make_hists,iterable=range(90),iteration_param='sample',gif_filename='hist.gif')


