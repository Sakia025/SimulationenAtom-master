#mesh
from stl import mesh

#listdir
from os import listdir
from os.path import isfile, join

#go
import plotly.graph_objects as go

#numpy
import numpy as np
mypath = '/Users/smller/Simulationen/python/test/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


# Load the STL files and add the vectors to the plot
i = 0
for file in onlyfiles:
    your_mesh = mesh.Mesh.from_file(mypath + file)

X, Y, Z = np.mgrid[-8:8:40j, -8:8:40j, -8:8:40j]
values = np.sin(X)

#X, Y, Z = np.mgrid[-8:8:40j, -8:8:40j, -8:8:40j]
#X = your_mesh.x
#Y = your_mesh.y
#Z = your_mesh.z
c = np.random.rand(len(X))

#values = c
print(c)
fig = go.Figure(data=go.Volume(
    x=X.flatten(),
    y=Y.flatten(),
    z=Z.flatten(),
    value=values.flatten(),
    isomin= values.min(),
    isomax= values.max(),
    opacity=0.1, # needs to be small to see through all surfaces
    surface_count=17, # needs to be a large number for good volume rendering
    ))
print(values.flatten())
fig.show()
