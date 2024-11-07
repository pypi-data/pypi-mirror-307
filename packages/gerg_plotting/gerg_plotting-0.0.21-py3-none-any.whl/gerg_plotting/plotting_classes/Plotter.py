import matplotlib
import matplotlib.axes
import matplotlib.cm
import matplotlib.colorbar
import matplotlib.figure
import matplotlib.pyplot
from matplotlib.colors import Colormap
import matplotlib.dates as mdates
from attrs import define, field, asdict
from pprint import pformat
import cartopy.crs as ccrs

from gerg_plotting.data_classes.NonSpatialInstruments import NonSpatialInstrument, Variable
from gerg_plotting.data_classes.SpatialInstrument import SpatialInstrument
from gerg_plotting.data_classes.NonSpatialInstruments import Bounds
from gerg_plotting.utils import calculate_range, calculate_pad, colorbar

@define
class Plotter:
    '''
    Base class for creating plots of data.
    
    Attributes:
        data (SpatialInstrument): The instrument holding spatial data (lat, lon, etc.).
        bounds (Bounds, optional): Geographic boundaries of the data.
        bounds_padding (float): Padding to be applied to the detected bounds.
        fig (matplotlib.figure.Figure, optional): Matplotlib figure object.
        ax (matplotlib.axes.Axes, optional): Matplotlib axes object.
        nrows (int): Number of rows in the figure.
        cbar (matplotlib.colorbar.Colorbar, optional): Colorbar object.
        cbar_nbins (int): Number of bins for colorbar tick marks.
        cbar_kwargs (dict): Keyword arguments for colorbar customization.
    '''
    
    data: SpatialInstrument
    bounds: Bounds | None = field(default=None)
    bounds_padding: float = field(default=0)

    fig: matplotlib.figure.Figure = field(default=None)
    ax: matplotlib.axes.Axes = field(default=None)

    nrows: int = field(default=1)

    cbar: matplotlib.colorbar.Colorbar = field(init=False)
    cbar_nbins: int = field(default=5)
    cbar_kwargs: dict = field(default={})

    def __attrs_post_init__(self):
        '''Post-initialization step to automatically detect bounds after the object is created.'''
        self.detect_bounds()

    def init_figure(self, fig=None, ax=None, three_d=False, geography=False) -> None:
        '''
        Initialize the figure and axes if they are not provided.
        
        Args:
            fig (matplotlib.figure.Figure, optional): Pre-existing figure.
            ax (matplotlib.axes.Axes, optional): Pre-existing axes.
            three_d (bool, optional): Flag to initialize a 3D plot.
            geography (bool, optional): Flag to initialize a map projection (Cartopy).
        
        Raises:
            ValueError: If both 'three_d' and 'geography' are set to True.
        '''
        
        # Guard clause: Ensure three_d and geography are not both True
        if three_d and geography:
            raise ValueError("Cannot set both 'three_d' and 'geography' to True. Choose one.")

        if fig is None and ax is None:
            # Create a new figure and axes
            if geography:
                # Initialize a figure with Cartopy's PlateCarree projection for geographic plots
                self.fig, self.ax = matplotlib.pyplot.subplots(
                    figsize=(6.4, 4.8),
                    subplot_kw={'projection': ccrs.PlateCarree()}
                )
            elif three_d:
                # Initialize a 3D figure
                self.fig, self.ax = matplotlib.pyplot.subplots(
                    figsize=(6.4, 4.8),
                    subplot_kw={'projection': '3d'}
                )
            else:
                # Standard 2D Matplotlib figure with no projection
                self.fig, self.ax = matplotlib.pyplot.subplots(figsize=(6.4, 4.8))
        elif fig is not None and ax is not None:
            # Use existing figure and axes
            self.fig = fig
            self.ax = ax
            self.nrows = len(self.fig.axes)  # Update the number of rows based on existing axes

            if three_d:
                # If it's a 3D plot, re-initialize the axes as a 3D plot
                index = [idx for idx, ax in enumerate(self.fig.axes) if ax is self.ax][0] + 1
                self.ax.remove()  # Remove existing 2D axis
                gs = self.ax.get_gridspec()  # Get grid specification
                self.ax = fig.add_subplot(gs.nrows, gs.ncols, index, projection='3d')

    def detect_bounds(self) -> None:
        '''
        Detect the geographic bounds of the instrument data, applying padding if specified.
        
        Raises:
            ValueError: If the instrument is not of type SpatialInstrument.
        '''
        if isinstance(self.data, SpatialInstrument):
            if self.bounds is None:
                # Detect and calculate the lat/lon bounds with padding
                if isinstance(self.data.lat, Variable) and isinstance(self.data.lon, Variable):
                    if self.data.lat is not None:
                        lat_min, lat_max = calculate_pad(self.data.lat.data, pad=self.bounds_padding)
                    else:
                        lat_min, lat_max = None, None
                    if self.data.lon is not None:
                        lon_min, lon_max = calculate_pad(self.data.lon.data, pad=self.bounds_padding)
                    else:
                        lon_min, lon_max = None, None
                    # Set the bounds
                    self.bounds = Bounds(
                        lat_min=lat_min,
                        lat_max=lat_max,
                        lon_min=lon_min,
                        lon_max=lon_max,
                        depth_bottom=None,
                        depth_top=None
                    )
        else:
            raise ValueError(f'Must pass an instrument of type SpatialInstrument, you passed {type(self.data) = }')

    def get_cmap(self, color_var: str) -> Colormap:
        '''
        Retrieve the colormap for a specified variable.
        
        Args:
            color_var (str): The name of the variable for which to retrieve the colormap.
        
        Returns:
            Colormap: The colormap for the variable, or 'viridis' if none is assigned.
        '''
        # Return the variable's assigned colormap, or the default 'viridis' if none exists
        if self.data[color_var].cmap is not None:
            cmap = self.data[color_var].cmap
        else:
            cmap = matplotlib.pyplot.get_cmap('viridis')
        return cmap
    
    def add_colorbar(self, mappable: matplotlib.axes.Axes, var: str | None, divider=None, total_cbars: int = 2) -> None:
        '''
        Add a colorbar to the plot.
        
        Args:
            mappable (matplotlib.axes.Axes): The mappable object (e.g., scatter plot) to associate with the colorbar.
            var (str | None): The variable for which the colorbar is created.
            divider (optional): Axes divider for better colorbar positioning.
            total_cbars (int): The total number of colorbars in the plot.
        
        Returns:
            matplotlib.colorbar.Colorbar: The created colorbar.
        '''
        if var is not None:
            # Get the label for the colorbar
            cbar_label = self.data[var].get_label()
            if divider is not None:
                # Create a colorbar using the custom 'colorbar' function with divider
                self.cbar = colorbar(self.fig, divider, mappable, cbar_label, nrows=self.nrows, total_cbars=total_cbars)
            else:
                # Create a standard colorbar
                self.cbar = self.fig.colorbar(mappable, label=cbar_label)

            # Adjust the number of ticks on the colorbar
            self.cbar.ax.locator_params(nbins=self.cbar_nbins)

            # Format the colorbar for time-based variables
            if var == 'time':
                self.cbar.ax.yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

            return self.cbar
        
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
