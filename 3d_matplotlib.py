# https://blogs.igalia.com/itoral/2016/10/13/opengl-terrain-renderer-rendering-the-terrain-mesh/
from osgeo import gdal
import rasterio
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Path to the GeoTIFF file
elevation_file = "data/5339-35.geotiff"

# Open the GeoTIFF file for reading
with rasterio.open(elevation_file) as src:
    # Read the elevation data as a NumPy array
    elevation_data = src.read(1)  # Assuming elevation data is in the first band (band index 1)

    # Get the geographic extent of the data
    extent = src.bounds

# Create a 3D figure
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Create a grid of x and y values based on the extent
x = np.linspace(extent.left, extent.right, elevation_data.shape[1])
y = np.linspace(extent.bottom, extent.top, elevation_data.shape[0])
X, Y = np.meshgrid(x, y)

# Plot the elevation data as a 3D surface
ax.plot_surface(X, Y, elevation_data, cmap='terrain')

# Set axis labels and a title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Elevation (meters)')
ax.set_title('3D Elevation Map')

# Show the plot
plt.show()