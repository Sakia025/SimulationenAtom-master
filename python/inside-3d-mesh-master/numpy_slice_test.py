#plt.imshow(origin = 'lower')
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.image import NonUniformImage
from matplotlib.patches import Rectangle

Dosis_Werte = np.array([0.2, 0.7, 0.5, 0.3])
cogs = np.array([[0,0,6],[0,1,6], [1,0,6],[1,1,6]])

z_true_indices = np.where(cogs[:,2]==6)         #hier später vlt ein in range angeben falls sonst durch nicht würfel am Rande des Auges Probleme auftreten
cogs = cogs[z_true_indices]
Dosis_Werte = Dosis_Werte[z_true_indices]

cmap = plt.cm.rainbow
norm = colors.Normalize(vmin=Dosis_Werte.min(), vmax=Dosis_Werte.max())

fig, ax = plt.subplots()
x = cogs[ : , 0]
y = cogs[ : , 1]
plt.scatter(x,y,c = cmap(norm(Dosis_Werte)))

width = 0.1 #Breite der Detektorwürfel
height = 0.1

for i in range(0, len(x)):
    ax.add_patch(Rectangle(xy=(x[i]-width/2, y[i]-height/2) ,width=width, height=height, linewidth=1, color=cmap(norm(Dosis_Werte[i])), fill=False))
ax.axis('equal')

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
fig.colorbar(sm)
plt.show()
