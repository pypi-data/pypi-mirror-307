from attrs import define,asdict,field
from pprint import pformat
import numpy as np
import mayavi.core.scene
import mayavi.mlab as mlab

from gerg_plotting.data_classes.SpatialInstruments import SpatialInstrument


@define
class Plotter3D:
    '''Wrapper around Mayavi'''
    instrument: SpatialInstrument

    def init_figure(self,fig=None,figsize=(1920,1080)):
        if fig is None:
            fig = mlab.figure(size=figsize)
        elif isinstance(fig,mayavi.core.scene.Scene):
            fig = fig
        else:
            ValueError(f"fig must be either None or a mayavi.core.secne.Scene object")
        return fig
    
    def _has_var(self, key) -> bool:
        '''Check if object has var'''
        return key in asdict(self).keys()
    
    def _get_vars(self) -> list:
        '''Get list of object variables/attributes'''
        return list(asdict(self).keys())

    def __getitem__(self, key: str):
        '''
        Allow dictionary-style access to class attributes.
        
        Args:
            key (str): The attribute name to access.
        
        Returns:
            The value of the specified attribute.
        '''
        if self._has_var(key):
            return getattr(self, key)
        raise KeyError(f"Variable '{key}' not found. Must be one of {self._get_vars()}")  

    def __setitem__(self, key, value):
        """Allows setting standard and custom variables via indexing."""
        if self._has_var(key):
            setattr(self, key, value)
        else:
            raise KeyError(f"Variable '{key}' not found. Must be one of {self._get_vars()}")

    def __repr__(self):
        '''Return a pretty-printed string representation of the class attributes.'''
        return pformat(asdict(self),width=1)
    
    def convert_colormap(self,colormap,over_color=None,under_color=None) -> np.ndarray:
        # Create the colormap array
        colormap_array = np.array([colormap(i) for i in range(256)])
        # Scale the color values to 0-1 range
        colormap_array *= 255
        # Convert the dtype to uint8
        colormap_array = colormap_array.astype(np.uint8)
        if under_color is not None:
            colormap_array[0] = under_color
        if over_color is not None:
            colormap_array[-1] = over_color
        
        return colormap_array
    
    def format_colorbar(colorbar,frame_height=1080):
        fontsize = round(((frame_height/400)**1.8)+11)  # Scale text with window size
        fontcolor = (0, 0, 0)  # Black Text
        # Allow the font sizes to be changed
        colorbar.scalar_bar.unconstrained_font_size = True  # Allow the font size to change
        # Labels text
        colorbar.scalar_bar.label_text_property.font_size = fontsize
        colorbar.scalar_bar.label_text_property.color = fontcolor
        # Title text
        colorbar.title_text_property.font_size = fontsize
        colorbar.title_text_property.color = fontcolor
        colorbar.title_text_property.line_offset = -7
        colorbar.title_text_property.line_spacing = 10
        colorbar.title_text_property.vertical_justification = 'top'
        pos2 = colorbar.scalar_bar_representation.position2
        colorbar.scalar_bar_representation.position2 = [pos2[0]-0.02,pos2[1]-0.01]
    
    def add_colormap(self,points,cmap_title,cmap=None):
        if cmap is not None:
            points.module_manager.scalar_lut_manager.lut.table = self.convert_colormap(cmap)
        var_colorbar = mlab.colorbar(points, orientation='vertical',title=cmap_title,label_fmt='%0.1f',nb_labels=6)  # Add colorbar
        var_colorbar.scalar_bar_representation.proportional_resize=True
        self.format_colorbar(var_colorbar,frame_height=self.settings.figsize[1])
        pos2 = var_colorbar.scalar_bar_representation.position2
        var_colorbar.scalar_bar_representation.position2 = [pos2[0]-0.02,pos2[1]-0.01]
