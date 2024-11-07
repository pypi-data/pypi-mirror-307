# glider_class.py

from attrs import define,field
import numpy as np
import pandas as pd
import xarray as xr
import mayavi.mlab as mlab 
from tvtk.tools import visual
import cmocean
import matplotlib.pyplot as plt
from datetime import datetime
import glob
from Scripts.Utils.utils import img2mov,generate_unique_filename,add_keys,format_colorbar,get_map_bounds,get_bathy,set_ssh_bounds,get_ssh # type: ignore


@define
class Glider:
    settings:None = field(default=None)

    df:pd.DataFrame = field(default=None)

    glider_tracker:dict = field(init=False)

    glider_dfs:dict = field(init=False)

    ds_ssh:xr.Dataset = field(init=False)

    scene = field(default=None)

    num_iterations:int = field(default=None)


    def __attrs_post_init__(self) -> None:
        # Check required values
        if self.settings is None:
            raise ValueError('Must Pass settings')
        if self.df is None:
            raise ValueError("Must pass df parameter")
        if self.settings.var is None:
            raise ValueError("Must pass var parameter")
        # Scale the vertical dimension
        # self.df['pressure'] = self.df.pressure/self.settings.vertical_scaler
        self.num_iterations = len(self.settings.date_range)
        self.ds_ssh = xr.open_dataset('../Data/processed_data/ssh.nc')
        self.ds_ssh = set_ssh_bounds(self.ds_ssh,self.settings.map_bounds)
        self.ds_ssh['sla'] = self.ds_ssh['sla']/self.settings.ssh_vertical_scaler

    
    def add_bathymetry(self) -> None:
        # Get bathymetry data
        x_bathy,y_bathy,z_bathy = get_bathy(get_map_bounds(depth_min=self.settings.map_bounds['depth_min'],depth_max=self.settings.map_bounds['depth_max'],
                                                           lon_min=self.settings.map_bounds['lon_min'],lon_max=self.settings.map_bounds['lon_max'],
                                                           lat_min=self.settings.map_bounds['lat_min'],lat_max=self.settings.map_bounds['lat_max']))
        # Rescale depth
        if self.settings.vertical_scaler is not None:
            z_bathy = z_bathy/self.settings.vertical_scaler
        # Plot Bathymetry data
        bathy = mlab.mesh(x_bathy,y_bathy,z_bathy,vmax=0)
        # Change colormap   
        land_color = [231,194,139,255]
        bathy_cmap = plt.get_cmap('Blues_r')
        bathy_cmap = cmocean.tools.crop_by_percent(bathy_cmap,25,'max')
        bathy_cmap = cmocean.tools.crop_by_percent(bathy_cmap,18,'min')
        bathy.module_manager.scalar_lut_manager.lut.table = get_colormap(bathy_cmap,over_color=land_color)  #type:ignore
        # Add and format colorbar
        bathy_colorbar = mlab.colorbar(bathy, orientation='vertical',title=f'Bathymetry {self.settings.bathy_unit}',label_fmt='%0.1f',nb_labels=6)  # Add colorbar
        bathy_colorbar.scalar_bar_representation.position = [0.89, 0.15]  # Adjust position as needed
        format_colorbar(bathy_colorbar,frame_height=self.settings.figsize[1])
        pos1 = bathy_colorbar.scalar_bar_representation.position
        pos2 = bathy_colorbar.scalar_bar_representation.position2
        bathy_colorbar.scalar_bar_representation.position = [pos1[0]+0.04,pos1[1]]
        bathy_colorbar.scalar_bar_representation.position2 = [pos2[0]-0.02,pos2[1]-0.01]

    def add_var(self) -> None:
        # Check 
        if self.settings.point_size is None:
            self.settings.point_size = 0.05
        if self.settings.evolve_time:
            initial_df = self.df[:self.settings.date_range[1]]
            points = mlab.points3d(initial_df.longitude,initial_df.latitude,initial_df.pressure,initial_df[self.settings.var],
                                mode='sphere',resolution=8,line_width=0,scale_factor=self.settings.point_size,vmax=self.settings.vmax,vmin=self.settings.vmin)   
        else:
            # Create all glider points
            points = mlab.points3d(self.df.longitude,self.df.latitude,self.df.pressure,self.df[self.settings.var],
                                mode='sphere',resolution=8,line_width=0,scale_factor=self.settings.point_size,vmax=self.settings.vmax,vmin=self.settings.vmin)
        # Change only the color by temperature
        points.glyph.scale_mode = 'scale_by_vector'
        # Change colormap
        if self.settings.cmap is not None:
            points.module_manager.scalar_lut_manager.lut.table = get_colormap(self.settings.cmap)  #type:ignore
        var_colorbar = mlab.colorbar(points, orientation='vertical',title=f'{self.settings.var.capitalize()} {self.settings.var_units}',label_fmt='%0.1f',nb_labels=6)  # Add colorbar
        var_colorbar.scalar_bar_representation.proportional_resize=True
        format_colorbar(var_colorbar,frame_height=self.settings.figsize[1])
        pos2 = var_colorbar.scalar_bar_representation.position2
        var_colorbar.scalar_bar_representation.position2 = [pos2[0]-0.02,pos2[1]-0.01]

        if self.settings.evolve_time:
            return points
        
    def add_ssh(self):
        start_date = self.settings.date_range[0].date()
        ds_ssh_init = self.ds_ssh.sel(time = slice(start_date,start_date))
        # Get SSH data
        x_ssh, y_ssh, z_ssh = get_ssh(ds_ssh_init)
        # Plot SSH data
        ssh = mlab.mesh(x_ssh,y_ssh,z_ssh,opacity=self.settings.ssh_surface_opacity,vmin=self.settings.ssh_vmin,vmax=self.settings.ssh_vmax)
        # Change colormap   
        ssh_cmap = cmocean.cm.balance
        ssh.module_manager.scalar_lut_manager.lut.table = get_colormap(ssh_cmap)  #type:ignore
        # Add and format colorbar
        ssh_colorbar = mlab.colorbar(ssh, orientation='horizontal',title=f'SSH {self.settings.ssh_unit}',label_fmt='%0.1f',nb_labels=6)  # Add colorbar
        # format_colorbar(ssh_colorbar)
        pos1 = ssh_colorbar.scalar_bar_representation.position
        pos2 = ssh_colorbar.scalar_bar_representation.position2
        format_colorbar(ssh_colorbar,frame_height=self.settings.figsize[1])

        ssh_colorbar.scalar_bar_representation.position = [pos1[0]+0.05,pos1[1]]
        ssh_colorbar.scalar_bar_representation.position2 = [pos2[0]-0.1,pos2[1]-0.08]
        if self.settings.evolve_time:
            return ssh

    def update_ssh(self,ssh_plot,current_date):
        ds = self.ds_ssh.sel(time = current_date,method='nearest')
        x,y,z = get_ssh(ds,just_sla=False)
        ssh_plot.mlab_source.reset(x=x,y=y,z=z,scalars=z)


    def add_glider_tracker(self) -> dict:
        if self.settings.point_size is None:
            self.settings.point_size = 0.05
        
        ds_glider_locs = xr.open_dataset('../Data/processed_data/glider_locs.nc')
        # self.settings.glider_ids = np.unique(ds_glider_locs.glider_id.values)

        # Filter out any gliders that are not specified in the glider_name_ids
        self.settings.glider_ids = list(self.settings.glider_name_ids.keys())

        glider_tracker = {glider_id:None for glider_id in self.settings.glider_ids}
        self.glider_dfs = {glider_id:None for glider_id in self.settings.glider_ids}

        for glider_id in self.settings.glider_ids:
            # Filter out any gliders that are not specified in the glider_name_ids
            da = ds_glider_locs.sel(glider_id=glider_id)
            df = da.to_dataframe()
            df = df.reset_index()
            df = df.set_index('time')
            
            self.glider_dfs[glider_id] = df.dropna()

            initial_df = df[:self.settings.date_range[0]]
            glider_tracker[glider_id] = mlab.points3d(initial_df.longitude,initial_df.latitude,
                                        initial_df.pressure,
                                        color=self.settings.glider_colors[glider_id],scale_factor=self.settings.tracker_point_size)
            
        return glider_tracker
        
    def update_glider_tracker(self,i):
        ''''''
        if self.settings.track_gliders:
            for glider_id in self.settings.glider_ids:
                df_frame = self.glider_dfs[glider_id][self.settings.date_range[i-1]:self.settings.date_range[i]]
                if len(df_frame) == 0:
                    pass
                else:
                    newx = df_frame['longitude']
                    newy = df_frame['latitude']
                    # newz = df_frame['pressure']
                    self.glider_tracker[glider_id].mlab_source.reset(x=[newx[-1]], y=[newy[-1]], z=np.zeros_like([newy[-1]]))
                # Check if the current frame's datetime is later than the glider's last datetime. This will remove the glider tracker from the map when it is retrieved
                if self.settings.time_window is not None:
                    if self.settings.date_range[i-self.settings.time_window] > self.glider_dfs[glider_id].index[-1]:
                        self.glider_tracker[glider_id].mlab_source.reset(x=[0], y=[0], z=[0])
                else:
                    if self.settings.date_range[i] > self.glider_dfs[glider_id].index[-1]:
                        self.glider_tracker[glider_id].mlab_source.reset(x=[0], y=[0], z=[0])                   

    def time_window(self,i,df_frame):
        if self.settings.time_window is None:
            newx = df_frame['longitude']
            newy = df_frame['latitude']
            newz = df_frame['pressure']
            newvar = df_frame[self.settings.var]  

        else:
            if i <= self.settings.time_window:
                df_frame = self.df[:self.settings.date_range[i]]
                newx = df_frame['longitude']
                newy = df_frame['latitude']
                newz = df_frame['pressure']
                newvar = df_frame[self.settings.var]
            else: 
                if i < self.num_iterations:
                    df_frame = self.df[self.settings.date_range[i-self.settings.time_window]:self.settings.date_range[i]]
                    newx = df_frame['longitude']
                    newy = df_frame['latitude']
                    newz = df_frame['pressure']
                    newvar = df_frame[self.settings.var]
                else:
                    newx = df_frame['longitude']
                    newy = df_frame['latitude']
                    newz = df_frame['pressure']
                    newvar = df_frame[self.settings.var] 

        return newx,newy,newz,newvar

    def set_camera(self) -> None:
        # Move the camera
        cam = self.scene.camera
        if self.settings.cam.start_loc.zoom is not None:
            cam.zoom(self.settings.cam.start_loc.zoom)
        cam.focal_point = self.settings.cam.start_loc.focalpoint.to_tuple()
        if self.settings.image_camera_loc is not None:
            mlab.view(azimuth=self.settings.image_camera_loc['azimuth'],
                      elevation=self.settings.image_camera_loc['elevation'],
                      distance=self.settings.image_camera_loc['distance'],
                      focalpoint = self.settings.cam.start_loc.focalpoint.to_tuple())

    def update_timestamp(self,fig,t,i):
        try:
            time_point = f"{self.settings.date_range[i]:%m-%d-%Y %H}:00"
            if fig._is_running:
                t.text = time_point
        except IndexError:
            pass

    def plot(self) -> None:
        if self.settings.figsize is not None:
            fig = mlab.figure(size=self.settings.figsize)
        else:
            fig = mlab.figure()
        self.scene = mlab.gcf().scene
        visual.set_viewer(fig)
        # cam = fig.scene.camera
        
        # Add Bathymetry
        self.add_bathymetry()
        # Add variable
        points = self.add_var()
        # Add glider tracker 
        if self.settings.track_gliders:
            self.glider_tracker = self.add_glider_tracker()
        # Add SSH
        ssh_plot = self.add_ssh()
        # Set starting camera position
        self.set_camera()

        @mlab.animate(delay=100,ui=False)
        def make_frame():
            # self.num_iterations = len(self.settings.date_range)

            time_start = f"{self.df.index[0]:%m-%d-%y %H}:00"
            time_text = mlab.text(*(0.89,0.019),time_start,color=(0, 0, 0),width=0.09)

            for i in range(self.num_iterations):
                df_frame = self.df[:self.settings.date_range[i]]

                if self.settings.evolve_time:                        

                    newx,newy,newz,newvar = self.time_window(i,df_frame)
                        
                    self.update_timestamp(fig,time_text,i)

                    self.update_glider_tracker(i)

                    self.update_ssh(ssh_plot,current_date=self.settings.date_range[i].date())
                    
                    points.mlab_source.reset(x=newx,y=newy,z=newz,scalars=newvar)

                    if self.settings.finalize_whole:
                        if i == self.num_iterations-1:
                            points.mlab_source.reset(x=self.df.longitude,y=self.df.latitude,z=self.df.pressure,scalars=self.df[self.settings.var])

                
                if self.settings.move_it:
                    azimuth = self.settings.cam.movement.azimuth[i]
                    elevation = self.settings.cam.movement.elevation[i]
                    distance = self.settings.cam.movement.distance[i]
                    focalpoint = self.settings.cam.movement.focalpoint[i].to_tuple()
                    mlab.view(azimuth=azimuth,elevation=elevation,distance=distance,focalpoint=focalpoint)

                if self.settings.save==True:
                    image_filename = f'../Plots/images/{self.settings.var}{i:04}.png'
                    self.scene.save(image_filename, size=self.settings.figsize)
                    # Add key for gliders
                    if self.settings.track_gliders:
                        add_keys(image_file=image_filename,figsize=self.settings.figsize,
                            glider_colors=self.settings.key_glider_colors,glider_name_ids=self.settings.glider_name_ids)
                    if i == self.num_iterations-1:
                        mlab.close()
                yield

        if self.settings.animate_it:
            ani = make_frame()
        else:
            # Not animating, plotting all data then saving as png
            if self.settings.save:
                if self.settings.image_camera_loc is not None:
                    mlab.view(azimuth=self.settings.image_camera_loc['azimuth'],elevation=self.settings.image_camera_loc['elevation'],distance=self.settings.image_camera_loc['distance'],focalpoint = self.settings.cam.start_loc.focalpoint.to_tuple())                  
                file_path = generate_unique_filename(directory='Plots/Glider/stills',filename=f'{self.settings.var}.png')
                self.scene.save(file_path, size=self.settings.figsize)
        mlab.show()

        if self.settings.save and self.settings.animate_it:
            image_path='Plots/Glider/animations/images'

            images = [image for image in glob.glob(f"{image_path}/{self.settings.var}*.png")]
            img2mov(images,self.settings.var,self.settings.frame_rate)



