from attrs import define, field
from typing import Callable
import io
import os
from pathlib import Path
import imageio.v3 as iio
import imageio
from PIL import Image, ImageFile
import numpy as np
import matplotlib.pyplot as plt

@define
class Animator:
    """
    A class for creating animations (GIFs) from a sequence of images generated 
    by a user-defined plotting function.
    """
    
    # Fields
    plotting_function: Callable = field(init=False)  # Function used to generate frames
    iterable: np.ndarray | list = field(init=False)  # Values over which to iterate (e.g., angles, time)
    duration: int | float = field(init=False)  # Duration of each frame in the GIF (in ms)
    iteration_param: str = field(init=False)  # The parameter name for the iteration (e.g., azimuth)
    frames: list = field(factory=list)  # List to store generated frames in memory
    image_dpi: int = field(default=300)  # DPI (resolution) for saved images

    # Paths and file names for image and GIF handling
    gif_filename: Path = field(init=False)  # Path to save the generated GIF
    images_path: Path = field(init=False)  # Directory for storing temporary images on disk
    image_files: list = field(init=False)  # List of image file paths generated on disk
    function_kwargs: dict = field(init=False)  # Additional arguments for the plotting function

    def fig2img(self, fig) -> ImageFile:
        """
        Convert a Matplotlib figure to a PIL Image.

        Parameters:
        fig: The Matplotlib figure to convert.

        Returns:
        ImageFile: The figure converted to a PIL Image.
        """
        # Create an in-memory buffer to store the image data
        buf = io.BytesIO()
        # Save the figure into the buffer with the specified DPI
        fig.savefig(buf, dpi=self.image_dpi)
        # Reset the buffer pointer to the beginning
        buf.seek(0)
        # Open the buffer as a PIL Image and return it
        img = Image.open(buf)
        return img

    def delete_images(self) -> None:
        """
        Delete image files from disk.
        """
        # Loop through each file path in image_files and remove the file
        for file in self.image_files:
            os.remove(file)

    def generate_frames_in_memory(self) -> None:
        """
        Generate frames for the animation and store them in memory.
        """
        # Loop over each value in the iterable
        for _, iter_value in enumerate(self.iterable):
            # Call the plotting function with the current iteration value and additional kwargs
            fig = self.plotting_function(**{self.iteration_param: iter_value}, **self.function_kwargs)
            # If the figure is successfully created, convert it to an image
            if fig:
                img = self.fig2img(fig)
                # Append the image to the frames list
                self.frames.append(img)
                # Close the figure to free memory
                plt.close(fig)

    def generate_frames_on_disk(self) -> None:
        """
        Generate frames for the animation and store them on disk.
        """
        # Calculate the number of digits needed for zero-padding file names
        num_padding = len(str(len(self.iterable)))
        # Loop over each value in the iterable
        for idx, iter_value in enumerate(self.iterable):
            # Create a file name with zero-padded index
            image_filename = self.images_path / f"{idx:0{num_padding}}.png"
            # Call the plotting function with the current iteration value and additional kwargs
            fig = self.plotting_function(**{self.iteration_param: iter_value}, **self.function_kwargs)
            # If the figure is successfully created, save it as a PNG on disk
            if fig:
                fig.savefig(image_filename, dpi=self.image_dpi, format='png')
                # Close the figure to free memory
                plt.close(fig)

    def save_gif_from_memory(self) -> None:
        """
        Save the GIF from frames stored in memory.
        """
        # Use the first frame as the starting point and append the rest of the frames
        self.frames[0].save(
            self.gif_filename,
            save_all=True,
            append_images=self.frames[1:],
            optimize=True,
            duration=self.duration,  # Set the duration of each frame
            loop=0  # Set the GIF to loop infinitely
        )

    def save_gif_from_disk(self) -> None:
        """
        Save the GIF from frames stored on disk.
        """
        # Get a sorted list of all PNG files in the images_path
        self.image_files = sorted(self.images_path.glob('*.png'))
        images = []
        # Load each image file and append it to the images list
        for file in self.image_files:
            images.append(imageio.imread(file))
        # Save all loaded images as a GIF
        imageio.mimsave(self.gif_filename, images)

    def animate(self, plotting_function, iterable, iteration_param, gif_filename: str, fps=24, **kwargs) -> None:
        """
        Create and save a GIF using the provided plotting function and iterable.

        Parameters:
        plotting_function (Callable): The function used to plot each frame.
        iterable (list or np.ndarray): Values over which the plotting function will iterate.
        iteration_param (str): The name of the parameter used for iteration (e.g., 'elev' or 'azim').
        gif_filename (str): The file name (and path) for saving the generated GIF.
        fps (int | float): Frames per second for the GIF (default is 24).
        kwargs: Additional keyword arguments passed to the plotting function.
        """
        # Assign the provided arguments to the corresponding attributes
        self.plotting_function = plotting_function
        self.iterable = iterable
        self.iteration_param = iteration_param
        self.duration = 1000 / fps  # Calculate frame duration in milliseconds
        num_iterations = len(self.iterable)
        self.gif_filename = Path(gif_filename)
        self.function_kwargs = kwargs

        # Decide whether to store frames in memory or on disk based on the number of iterations
        if num_iterations < 100:
            print(f'Saving figures to memory, n_iterations: {num_iterations}')
            self.generate_frames_in_memory()  # Store frames in memory
            self.save_gif_from_memory()  # Save GIF from memory
        else:
            print(f'Saving figures to storage, n_iterations: {num_iterations}')
            # Create a directory for storing images if it doesn't exist
            self.images_path = Path(__file__).parent.joinpath('images')
            self.images_path.mkdir(parents=True, exist_ok=True)
            self.generate_frames_on_disk()  # Store frames on disk
            self.save_gif_from_disk()  # Save GIF from disk
            self.delete_images()  # Delete temporary image files from disk
