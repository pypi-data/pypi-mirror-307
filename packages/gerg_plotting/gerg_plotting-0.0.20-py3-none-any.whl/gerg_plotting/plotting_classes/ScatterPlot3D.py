from attrs import define,field
import mayavi.core
import mayavi.core.scene
import mayavi.modules
import mayavi.modules.axes
import numpy as np
import mayavi.mlab as mlab
import mayavi
from functools import partial

from gerg_plotting.plotting_classes.Plotter3D import Plotter3D

@define
class ScatterPlot3D(Plotter3D):

    fig:mayavi.core.scene.Scene = field(default=None)
    figsize:tuple = field(default=(1920,1080))

    def show(self):
        mlab.show()

    def _check_var(self,var):
        if var is not None:
            if not self.data._has_var(var):
                raise ValueError(f'Instrument does not have {var}')

    def _scatter(self,var,point_size,fig):
        if var is None:
            points = mlab.points3d(self.data.lon.data,self.data.lat.data,self.data.depth.data,
                        mode='sphere',resolution=8,scale_factor=point_size,figure=fig)
        elif isinstance(var,str):
            points = mlab.points3d(self.data.lon.data,self.data.lat.data,self.data.depth.data,self.data[var].data,
                        mode='sphere',resolution=8,scale_factor=point_size,vmax=self.data[var].vmax,vmin=self.data[var].vmin,figure=self.fig)
            points.glyph.scale_mode = 'scale_by_vector'
        else:
            raise ValueError(f'var must be either None or one of {self.data}')


    def plot(self,var:str|None=None,point_size:int|float=0.05,fig=None,show:bool=True):
        self.fig = self.init_figure(fig=fig)

        self._check_var(var)
            
        self._scatter(var,point_size,fig)
            

        
        if show:
            self.show()
    


