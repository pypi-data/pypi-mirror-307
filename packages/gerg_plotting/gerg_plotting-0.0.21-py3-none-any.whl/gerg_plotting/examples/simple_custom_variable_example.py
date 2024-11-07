from gerg_plotting import Data,Variable
from gerg_plotting import Histogram
import numpy as np

# Init Data object
data = Data()
# Init pH Variable object
pH = Variable(data=np.random.normal(7.7,scale=0.25,size=1000),name='pH')
# Add the pH Variable object to the Data object
data.add_custom_variable(pH)
# Test by plotting a histogram
Histogram(data).plot('pH')
