import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt
from skimage import measure
from scipy.ndimage import morphology
from stl import mesh 

# Load GeoTIFF DEM
dem_file = "data/5339-35.geotiff"
dataset = gdal.Open(dem_file)
band = dataset.GetRasterBand(1)
elevation_array = band.ReadAsArray()
elevation_array = np.where(np.isnan(elevation_array), np.nanmean(elevation_array), elevation_array)
min_val = elevation_array.min()
max_val = elevation_array.max()
rescaled_elevation_array = ((elevation_array - min_val) / (max_val - min_val)) * 1000

# Create 3D point cloud
transform = dataset.GetGeoTransform()
projection = dataset.GetProjection()
cols = dataset.RasterXSize
rows = dataset.RasterYSize
points = []
for row in range(rows):
    for col in range(cols):
        x = transform[0] + col * transform[1] + row * transform[2]
        y = transform[3] + col * transform[4] + row * transform[5]
        z = rescaled_elevation_array[row, col]
        points.append((x, y, z))
x_coords, y_coords, z_coords = zip(*points)

# Create voxels
x_coords = np.array(x_coords)
y_coords = np.array(y_coords)
z_coords = np.array(z_coords)
range_x = x_coords.max() - x_coords.min()
range_y = y_coords.max() - y_coords.min()
range_z = z_coords.max() - z_coords.min()
voxel_size_x = range_x / 100
voxel_size_y = range_y / 100  
voxel_size_z = range_z / 100 
x_voxels = np.floor((x_coords - x_coords.min()) / voxel_size_x).astype(int)
y_voxels = np.floor((y_coords - y_coords.min()) / voxel_size_y).astype(int)
z_voxels = np.floor((z_coords - z_coords.min()) / voxel_size_z).astype(int)
grid_dimensions = (x_voxels.max() + 1, y_voxels.max() + 1, z_voxels.max() + 1)
voxel_grid = np.zeros(grid_dimensions, dtype=bool)
for x, y, z in zip(x_voxels, y_voxels, z_voxels):
    voxel_grid[x, y, z] = True


# Plot point cloud
# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_subplot(111, projection='3d')
# scatter = ax.scatter(x_coords, y_coords, z_coords, c=z_coords, cmap='viridis', marker='.')
# ax.set_title('3D Point Cloud')
# ax.set_xlabel('X Coordinate')
# ax.set_ylabel('Y Coordinate')
# ax.set_zlabel('Elevation')
# plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=5) # Optional: color bar for elevation
# plt.show()

# Point voxel
# fig = plt.figure(figsize=(10, 7))
# ax = fig.add_subplot(111, projection='3d')
# ax.voxels(voxel_grid, facecolors='blue', edgecolor='k')
# ax.set_title('3D Voxel Representation')
# ax.set_xlabel('X Voxel')
# ax.set_ylabel('Y Voxel')
# ax.set_zlabel('Z Voxel')
# plt.show()
    
voxel_data = voxel_grid
X, Y, Z = voxel_data.shape

# Create a mesh using Marching Cubes algorithm
verts, faces, normals, values = measure.marching_cubes(voxel_data, level=0)

# Create an STL mesh object from the vertices and faces
stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        stl_mesh.vectors[i][j] = verts[f[j], :]

# Save the mesh as an OBJ file
stl_mesh.save('output.obj')