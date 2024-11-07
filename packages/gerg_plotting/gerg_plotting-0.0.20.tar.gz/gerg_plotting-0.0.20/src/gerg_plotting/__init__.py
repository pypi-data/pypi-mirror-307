'''
Thin wrapper around matplotlib for standarized plotting at GERG
'''

from .plotting_classes.Histogram import Histogram
from .plotting_classes.Animator import Animator
from .data_classes.NonSpatialInstruments import Bounds,Variable
from .data_classes.SpatialInstruments import Bathy,Data
from .plotting_classes.MapPlot import MapPlot
from .plotting_classes.ScatterPlot import ScatterPlot
from .plotting_classes.ScatterPlot3D import ScatterPlot3D
from .data_classes.utils import data_from_df,data_from_csv