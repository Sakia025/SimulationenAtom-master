from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from os import listdir
from os.path import isfile, join
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np

import plotly.plotly as py
import plotly.figure_factory as FF
import plotly.graph_objs as go
from scipy.spatial import Delaunay
#mypath = '/Users/smller/Simulationen/ccb-plaque/models/'
mypath = '/Users/smller/Simulationen/python/test/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
name_color_map = 'seismic';

# Create a new plot
#figure = pyplot.figure()
#axes = mplot3d.Axes3D(figure)


cogs = np.zeros(len(onlyfiles))
# Load the STL files and add the vectors to the plot
i = 0
for file in onlyfiles:
    your_mesh = mesh.Mesh.from_file(mypath + file)
    volume, cog, inertia = your_mesh.get_mass_properties()
    x = your_mesh.x
    c = np.random.rand(len(x))
    x = your_mesh.x.flatten()
    y = your_mesh.y.flatten()
    z = your_mesh.z.flatten()

print(x)
print(y)
print(z)
print(c)

triangles = mtri.Triangulation(x, y).triangles


fig = plt.figure()
ax = fig.gca(projection='3d')
triang = mtri.Triangulation(x, y, triangles);
surf = ax.plot_trisurf(triang, z, cmap = name_color_map, shade=False, linewidth=0.2)
surf.set_array(c)
surf.autoscale()


#Add a color bar with a title to explain which variable is represented by the color.
cbar = fig.colorbar(surf, shrink=0.5, aspect=5)
#cbar.ax.get_yaxis().labelpad = 15; cbar.ax.set_ylabel(list_name_variables[index_c], rotation = 270)

# Add titles to the axes and a title in the figure.
#ax.set_xlabel(list_name_variables[index_x]); ax.set_ylabel(list_name_variables[index_y])
#ax.set_zlabel(list_name_variables[index_z])
#plt.title('%s in function of %s, %s and %s' % (list_name_variables[index_c], list_name_variables[index_x], list_name_variables[index_y], list_name_variables[index_z]) );

plt.show()

    #your_mesh = your_mesh[your_mesh.z == 0]
    #face_color = (141 / 255, 184 / 255, 226 / 255)
    #edge_color = (50 / 255, 50 / 255, 50 / 255)
    #your_Poly3DMesh = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
    #your_Poly3DMesh.set_edgecolor(edge_color)
    #your_Poly3DMesh.set_facecolor(face_color)
    #axes.add_collection3d(your_Poly3DMesh)
    #surf = axes.plot_surface(your_mesh.x, your_mesh.y, your_mesh.z, rstride=1, cstride=1, cmap=cm.viridis,
    #                       linewidth=0, antialiased=False)
#figure.colorbar(surf, shrink=0.5, aspect=5)

#print(your_mesh.x)
#print(your_mesh.vectors[0][2][2])
# Auto scale to the mesh size
#scale = your_mesh.points.flatten(-1)
#axes.auto_scale_xyz(scale, scale, scale)

axes.set_xlim3d(-15, 15)
axes.set_ylim3d(-15, 15)
axes.set_zlim3d(-15, 15)
# axes.axis('equal') #funktioniert auch nicht gut, jedenfalls bisher

# figure.tight_layout(), nicht kompatibel->warning
# Show the plot to the screen
pyplot.show()
#pyplot.savefig("Auge_Dosis.png")
