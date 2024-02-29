import pyvista as pv
import numpy as np

# Load STL file
mesh = pv.read('data/model.stl')

# Initialize a scalar array with zeros
scalars = np.zeros(mesh.n_points)

# Get z-coordinates of all points
z_coords = mesh.points[:, 2]

# Set scalar values based on the z-coordinate condition
scalars[(z_coords > 0) & (z_coords < 6)] = 1  # Between 0 and 6

# Add Colors
mesh['Colors'] = scalars

# index 0 is green, index 1 will be blue
cmap = ['green', 'blue']

# Plot the mesh with the specified colormap
plotter = pv.Plotter()
plotter.add_mesh(mesh, scalars='Colors', cmap=cmap, show_edges=True)
plotter.show()
