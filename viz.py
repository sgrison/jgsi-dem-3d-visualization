import pyvista as pv

# Load the STL file
mesh = pv.read('data/model.stl')

# Plot the mesh
plotter = pv.Plotter()
plotter.add_mesh(mesh, show_edges=True)
plotter.show()