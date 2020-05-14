#from matplotlib import pyplot
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from os import listdir
from os.path import isfile, join

import numpy as np


def main():
    Dosis_Werte =
    x, y, z = #SliceDaten(cogs, Dosis_Werte, Koordinate = koordinate, AnzahlSlices = AnzahlSlices)

    cmap = plt.cm.rainbow
    norm = mpl.colors.Normalize(vmin=Dosis_Werte.min(), vmax=Dosis_Werte.max())


#scrollbarer Scatterplot
    fig, ax = plt.subplots(1, 1)
    tracker = IndexTracker(ax, x, y, Dosis_Werte, norm(Dosis_Werte), z.size())
    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    #plt.show()





class IndexTracker(object):

    def __init__(self, ax, X, Y, Dose, normDose, AnzahlSlices):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        self.Y = Y
        self.Dose = Dose
        self.slices = AnzahlSlices
        self.normDose = normDose
        #rows, cols, self.slices = X.shape
        #self.ind = self.slices//2
        cmap = plt.cm.rainbow
        self.ind = self.slices-1
        print(self.ind)
        self.im = self.ax.scatter(self.X[self.ind][:],self.Y[self.ind][:],c = cmap(self.normDose[self.ind]), marker = 's')
        #self.im = ax.imshow(self.X[:, :, self.ind])
        #sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        #plt.colorbar(sm)
        plt.xlim(-1.3, 1.3)
        plt.ylim(-1.3, 1.3)
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        #print(self.ind)
        self.ax.cla()
        plt.xlim(-1.3, 1.3)
        plt.ylim(-1.3, 1.3)
        self.update()

    def update(self):
        #self.im.set_data(self.X[:, :, self.ind])
        cmap = plt.cm.rainbow
        self.im = self.ax.scatter(self.X[self.ind][:],self.Y[self.ind][:],c = cmap(self.normDose[self.ind]), marker = 's')

        #self.im.set_data(self.X[self.slices][:],self.Y[self.slices][:])
        self.ax.set_ylabel('slice %s' % self.slices)
        self.im.axes.figure.canvas.draw()

main()
