from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from os import listdir
from os.path import isfile, join
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.colors import Normalize
import numpy as np
import pandas as pd

mypath = '/Users/smller/Simulationen/python/test/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
name_color_map = 'Oranges';

data_path = '/Users/smller/Simulationen/ccb-plaque-build/Daten/daten_0.txt'
pandas = pd.read_csv(data_path, names = ['Text' , 'Filename' , 'Dose'  , 'Unit'])
#print(pandas['Filename'])
#pandas.loc(pandas['Filename'] == 'Sclera:1_23.stl')

# Create a new plot
figure = pyplot.figure()
axes = mplot3d.Axes3D(figure)

#c_list = np.zeros(2)
#c_list = np.random.rand(1)
#print(c_list)
# Load the STL files and add the vectors to the plot
color=iter(cm.rainbow(np.linspace(0,1,len(onlyfiles))))
i = 0
for file in onlyfiles:
    your_mesh = mesh.Mesh.from_file(mypath + file)
    c=next(color)
    face_color = c
    #c_list[i] = c
    i = i+1
    #edge_color = (50 / 255, 50 / 255, 50 / 255)
    your_Poly3DMesh = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
    #your_Poly3DMesh.set_edgecolor(edge_color)
    your_Poly3DMesh.set_facecolor(face_color)
    axes.add_collection3d(your_Poly3DMesh)
    #df = pd.DataFrame(data=your_Poly3DMesh)
    #print(df)
    print(your_Poly3DMesh)





im = axes.imshow(np.array([[0,1]]), cmap=name_color_map)
im.set_visible(False)
#figure.colorbar(im, cax=cax, orientation='horizontal')
pyplot.colorbar(im)
axes.set_xlim3d(-15, 15)
axes.set_ylim3d(-15, 15)
axes.set_zlim3d(-15, 15)

#norm = Normalize(vmin=-20, vmax=10)
#cbar = figure.colorbar(bla, axes = axes)#bla, shrink=0.5, aspect=5)

#pyplot.show()
pyplot.savefig("Ergebnisse/Plots/Hase.png")
#wird von Snakemake in Simulationen aufgerufen, desshalb landet es dort, wenn ich es in Python aufrufe dann anderer pfad
