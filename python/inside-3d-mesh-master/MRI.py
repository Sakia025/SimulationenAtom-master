#from stl import mesh
#from mpl_toolkits import mplot3d
from matplotlib import pyplot
from os import listdir
#from os.path import isfile, join
from matplotlib import cm
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
#import matplotlib.tri as mtri
#from matplotlib.patches import Rectangle
from matplotlib.colors import Normalize
import numpy as np
import pandas as pd
#from is_inside_mesh import is_inside_turbo as is_inside
import matplotlib as mpl
from scipy.interpolate import griddata
#import stlparser
#import sys
#import json
import seaborn as sns


#def create3DGridPoints(min, max, NumberOfPoints):
##3D Pointgrid (symmetric)
#    x = np.linspace(min,max,NumberOfPoints)
#    y = x
#    z = x
#
#    #https://stackoverflow.com/questions/18253210/creating-a-numpy-array-of-3d-coordinates-from-three-1d-arrays
#    GridPoints = np.vstack(np.meshgrid(x,y,z)).reshape(3,-1).T
#    return GridPoints

#def ReadStl(StlFile):
## Load the input mesh as a list of triplets (ie. triangles) of 3d vertices, from demo-naive.py from is inside
#    try:
#        triangles = np.array([X for X, N in stlparser.load(StlFile)])
#    except stlparser.ParseError as e:
#        sys.stderr.write(f'{e}\n')
#        sys.exit(0)
#    finally:
#        StlFile.close()
#    #print('done')
#    return triangles


#def ():
#    return



#def BoolPointsInsideVolumes(StlPath, Grid):#StlVolumes, StlDosisTable, Points):
#    filenames = np.asarray(FindStlFiles(StlPath))
##!!!zu testzewcken nur drei Volumen
##
#    #filenames = filenames[:3]
#    #print('hey, hier noch auf alle Volumen erweitern und Grid zu longdouble ')
#    Volumes = [np.vstack(ReadStl(open(StlPath + file))) for file in filenames]
#
#    #Grid = Grid.astype('longdouble')
#
#    IsPointInside = np.asarray([np.vstack(is_inside(volume, Grid)) for volume in Volumes])
#    IsPointInside = np.swapaxes(IsPointInside, 0,1)
#    return IsPointInside, filenames


#def filenameForGridPoint(filenames, IsPointInside):
#    filename = filenames[IsPointInside]
#    if filename.size == 0:
#        filename = np.array(["PointIsInNoGivenVolume"])
#    if filename.size > 1:
#        print('Punkt ist in mehreren Volumina, wird erstmal auf das erste Volumen gesetzt')
#        filename = filename[0]
#
#    return filename


#def DoseValuesForGridPoints(StlPath, Grid, DosisUndCog):
#
#    IsPointInside, filenames = BoolPointsInsideVolumes(StlPath, Grid)
#    print(filenames)
#    #filenames = filenames[IsPointInside[0]]
#    #print('Aus Testzwecken wird hier noch der zweite Wert auf True gesetzt,')
#    print('exception einbauen falls Punkt in mehr als einem Volumen liegt')
#    #IsPointInside[:,2]= True
#    #the filenames of the STL Volumes in which the Grid Points lie. So Grid[0] is in STL Volume Filenames[0]
#    #filenames = np.asarray([np.hstack(filenames[IsPointInside[i].flatten()]) for i in range(0, len(Grid))]).flatten()
#    filenames = np.asarray([np.hstack(filenameForGridPoint(filenames, IsPointInside[i].flatten())) for i in range(0, len(Grid))]).flatten()
#    filenames = filenames.apply(convertToString)
#    print(filenames)
#    GridPointDose, cogs = DoseAndCogsAsArray(DosisUndCog, filenames)
#    return GridPointDose, Grid

# Python program to convert a list
# of character
#def convertToString(s):
#    new = ""
#    for x in s:
#        new += x
#    # return string
#    return new




#def DoseAndCogsAsArray(DosisUndCog, files):
#    Dosis_Werte = np.zeros(len(files))
#
#    #dummy Eintrag, damit vstack genutzt werden kann, wird spaeter weggeschnitten
#    cogs = np.array([0,1,2])
#    i = 0
#    for file in files:
#        #if convertToString(file) == "PointIsInNoGivenVolume":
#        #    Dosis_Werte[i] = 0
#        #    cogs = np.array([0,0,0])
#        #else:
#        file = file[:-4] #to remove the .stl in the string
#
#        STLObjektDaten = DosisUndCog.loc[file]
#        Dosis = STLObjektDaten['Dose']
#
#        Einheit = STLObjektDaten['Unit']
#        COG = STLObjektDaten['cog']
#
#        Dosis_Werte[i] = Dosis
#        cogs = np.vstack((cogs,np.array(COG)))
#
#        i = i+1
#
#    cogs = cogs[1:] #muss sein da der erste eintrag von cogs nur ein dumy war, damit vstack geutzt werden kann
#    return Dosis_Werte, cogs

#-------------------------------------------------------------------------------
def makeArray(text):
    return np.fromstring(text,sep=',')


def FindStlFiles(StlPath):
    filenames = [f for f in listdir(StlPath) if f.endswith('.stl')]
    return filenames

def removeStlEnding(filename):
    newFilename = filename.replace(".stl", "")
    return newFilename

def ExtrahiereDosisUndCog(stl_path,cog_path, dosis_path):
    onlyfiles = FindStlFiles(stl_path)
    #replace(cog_path)
    cog_df = pd.read_csv(cog_path, sep = ';', names = ['Filename', 'cog'], skiprows = 1)
    cog_df = cog_df.set_index('Filename')
    cog_df['cog'] = cog_df['cog'].apply(makeArray)
    print(cog_df)
    #Simulationsdaten einlesen
    #replace(data_path)
    Simulationsdaten = pd.read_csv(dosis_path, names = ['Text' , 'Filename' , 'Dose'  , 'Unit'])
    Simulationsdaten['Filename'] = Simulationsdaten['Filename'].apply(removeStlEnding)
    Simulationsdaten = Simulationsdaten.set_index('Filename')
    print(Simulationsdaten)
    #print(Simulationsdaten.index)
    #nicht mehr noetig in der main von der Simulation war zweimal runbeam 100
    #Simulationsdaten = Simulationsdaten.head(n=len(onlyfiles))  # fliegt spaeter raus, aktuell speichert event Action aber jeden Detector zweimal ab, beim zweiten Mal mit 0Dosis

    DosisUndCog = pd.concat([cog_df, Simulationsdaten],axis = 1)

    return DosisUndCog
#-------------------------------------------------------------------------------

#def WerteInAbhaenigkeitVonXYZ(cogs, Dosis_Werte, Koordinate, min_xyz, max_xyz):
#    xyz = KoordinateToArrayPos(Koordinate)
#
#    xyz_true_indices = np.where((cogs[:,xyz]>=min_xyz) & (cogs[:,xyz]<= max_xyz))         #hier spaeter vlt ein in range angeben falls sonst durch nicht wuerfel am Rande des Auges Probleme auftreten
#    cogs_xyz = cogs[xyz_true_indices]
#    Dosis_Werte_xyz = Dosis_Werte[xyz_true_indices]
#
#    k1 = cogs_xyz[ : , 0]   #je nachdem was Koordinate war sind k1 und k2 entweder x und y oder eine andere Kombination
#    k2 = cogs_xyz[ : , 1]
#
#    return k1, k2, Dosis_Werte_xyz


#def SliceDaten(cogs, Dosis_Werte, Koordinate, AnzahlSlices):
#    xyz = KoordinateToArrayPos(Koordinate)
#
#    all_k1 = []
#    all_k2 = []
#    all_Dosis_Werte = []#dummys fuer vstack werden wieder entfernt
#
#    Slice_Koordinaten = np.linspace(cogs[:,xyz].min(),cogs[:,xyz].max(), AnzahlSlices+1)
#    for i in range(0,len(Slice_Koordinaten)-1):
#        k1,k2, Dosis_Werte_xyz = WerteInAbhaenigkeitVonXYZ(cogs, Dosis_Werte, Koordinate, min_xyz = Slice_Koordinaten[i], max_xyz = Slice_Koordinaten[i+1])
#
#        all_k1.append(k1)
#        all_k2.append(k2)
#        all_Dosis_Werte.append(Dosis_Werte_xyz)
#
#    return np.asarray(all_k1), np.asarray(all_k2), np.asarray(all_Dosis_Werte)

def KoordinateToArrayPos(Koordinate):
    if Koordinate == 'x':
        xyz = 0
    elif Koordinate =='y':
        xyz = 1
    elif Koordinate == 'z':
        xyz = 2
    return xyz



def main():
    stl_path = '/Users/smller/Simulationen/ccb-plaque/models/'
    dosis_path = '/Users/smller/Simulationen/ccb-plaque-build/Daten/daten_0.txt'
    cog_path = '/Users/smller/Simulationen/python/COG_Fusion/COG.txt'
    SaveGridpoints_path = "/Users/smller/Simulationen/python/Plot/Gridpoints.txt"
    SaveGridpointsPossibleFilenames_path = "/Users/smller/Simulationen/python/Plot/GridpointsPossibleFilenames.txt"


    GridFilenames_path = "/Users/smller/Simulationen/python/Plot/FilenameGridpoints.txt"
    GridFilenames_severalVolumina_path = "/Users/smller/Simulationen/python/Plot/FilenameGridpoints_mehrereVolumen.txt"
    Gridpoints_noVolumina_path = "/Users/smller/Simulationen/python/Plot/FilenameGridpoints_inkeinemVolumen.txt"
    koordinate = 'z'
    #AnzahlSlices = 15
    #Dosis_Werte, cogs, DosisUndCog = ExtrahiereDosisUndCog(stl_path,cog_path, dosis_path)
    DosisUndCog = ExtrahiereDosisUndCog(stl_path,cog_path, dosis_path)

#0o0o0o00o0o00o0o0o0o0o0o0o0o00o00o0o00o0o0o0o0o00o00o0o0o0o00o0o0o0o0o0o0o0o0o0
#Zum einlesen von echten Fusion Punkte
    ##Punkte, die eindeutig in einem Volumen liegen
    #Filenames_Gridpoints1 = pd.read_csv(GridFilenames_path, sep = ',', names = ['Filename', 'x', 'y', 'z'], skiprows = 1, encoding = 'utf-8')
    #Filenames_Gridpoints1['Filename'] = Filenames_Gridpoints1['Filename'] + ".stl"
    #array = pd.Series(DosisUndCog['Dose'].loc[Filenames_Gridpoints1['Filename']])
    #Filenames_Gridpoints1 = Filenames_Gridpoints1.set_index('Filename')
    #xyz_OneDose_df = pd.concat([Filenames_Gridpoints1, array],axis = 1)

    ##Punkte, die auf der Oberflaeche mehrerer Volumina liegen
    #Filenames_Gridpoints2 = pd.read_csv(GridFilenames_severalVolumina_path, sep = ',', names = ['Filename', 'x', 'y', 'z'], skiprows = 2, encoding = 'utf-8')
    #Filenames_Gridpoints2['Filename'] = Filenames_Gridpoints2['Filename'] + ".stl"
    #array2 = pd.Series(DosisUndCog['Dose'].loc[Filenames_Gridpoints2['Filename']])
    #Filenames_Gridpoints2 = Filenames_Gridpoints2.set_index('Filename')
    #xyz_severalDoses_df = pd.concat([Filenames_Gridpoints2, array2],axis = 1)
    #xyz_severalDoses_df = xyz_severalDoses_df.sort_values(['x', 'y', 'z'])
    ##mitteln der Punkten die auf der Oberfläche mehrerer Volumina sitzen
    #xyz_severalDoses_df = xyz_severalDoses_df.groupby(['x', 'y', 'z'], as_index=False)['Dose'].mean()
    ##Zwischenergebnis der Punkte die irgendwie in Volumen liegen
    #xyz_OneDose_df = xyz_OneDose_df.append(xyz_severalDoses_df)

    ##Punkte, die außerhalb aller Volumina liegen und somit 0 als Dosis haben
    #NoFilenames_Gridpoints3 = pd.read_csv(Gridpoints_noVolumina_path, sep = ',', names = ['x', 'y', 'z', 'Dose'], skiprows = 2, encoding = 'utf-8')
    #resultGridDose_df = xyz_OneDose_df.append(NoFilenames_Gridpoints3)

    #resultGridDose_df = resultGridDose_df.reset_index()
    #resultGridDose_df = resultGridDose_df.drop(resultGridDose_df.columns[[0]], axis=1)
    ##print(resultGridDose_df)
    ##test zeigt, es gibt keine Duplikate mehr :D
    ##test = xyz_OneDose_df[xyz_OneDose_df.duplicated(['x', 'y', 'z'])]
    ##print(test)
#0o0o0o00o0o00o0o0o0o0o0o0o0o00o00o0o00o0o0o0o0o00o00o0o0o0o00o0o0o0o0o0o0o0o0o0
#----
#----
#!!!!!!!!!!!!!!wird gebraucht
    #cmap = plt.cm.rainbow
    #norm = mpl.colors.Normalize(vmin=resultGridDose_df['Dose'].min(), vmax=resultGridDose_df['Dose'].max())

    #PlotTables, SliceCoordiates = SliceDaten_2(GridDosisDaten = resultGridDose_df, SliceKoordinate = 'z', k1 = 'x', k2 = 'y', Dose = 'Dose')

#scr#ollbarer Scatterplot
    #fig, ax = plt.subplots(1, 1)
    #tracker = IndexTracker(ax, PlotTables, len(SliceCoordiates)) #norm(resultGridDose_df['Dose'].values()),
    #fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    #plt.show()
#!!!!!!!!!!!!wird gebracut

#0o0o0o00o0o00o0o0o0o0o0o0o0o00o00o0o00o0o0o0o0o00o00o0o0o0o00o0o0o0o0o0o0o0o0o0
    zDose_mean = TDK(DosisUndCog)
    TDKplot(zDose_mean)


#0o0o0o00o0o00o0o0o0o0o0o0o0o00o00o0o00o0o0o0o0o00o00o0o0o0o00o0o0o0o0o0o0o0o0o0
    return

def TDKplot(zDose_mean):
    z = zDose_mean['z'].values()
    Dosis = zDose_mean['Dose'].values()
    fig, ax = plt.subplots()
    ax.plot(z, Dosis)

    ax.set(xlabel='z/mm', ylabel='Dosis/Gry',
       title='TDK')
    ax.grid()

    fig.savefig("TDK.png")
    plt.show()
    return

def TDK(DosisUndCog):
    zDose_mean = DosisUndCog.groupby(['z'], as_index=False)['Dose'].mean()
    return zDose_mean



def SliceDaten_2(GridDosisDaten, SliceKoordinate, k1, k2, Dose):
    SliceCoordiates = GridDosisDaten[SliceKoordinate].drop_duplicates()
    SliceCoordiates = SliceCoordiates.sort_values()
    tables = []
    for k in SliceCoordiates:
        GridDosisDaten_k = GridDosisDaten.loc[GridDosisDaten[SliceKoordinate] == k]
        table = GridDosisDaten_k.pivot(k1, k2, Dose)
        tables.append(table)
    return tables, np.asarray(SliceCoordiates)



    #GridDose_z = resultGridDose_df.loc[resultGridDose_df['z'] == -1.0]
    #table = GridDose_z.pivot('y', 'x', 'Dose')
    #ax = sns.heatmap(table)
    #ax.invert_yaxis()
    #plt.show()




#    cmap = plt.cm.rainbow
#    norm = mpl.colors.Normalize(vmin=Dosis_Werte.min(), vmax=Dosis_Werte.max())
#
#    all_k1, all_k2, all_Dosis_Werte = SliceDaten(cogs, Dosis_Werte, Koordinate = koordinate, AnzahlSlices = AnzahlSlices)
#
##scrollbarer Scatterplot
#    fig, ax = plt.subplots(1, 1)
#    tracker = IndexTracker(ax, all_k1, all_k2, all_Dosis_Werte, norm(all_Dosis_Werte), AnzahlSlices)
#    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    #plt.show()



def replace(file):
    #EventAction saves / as : so i undo this here
    #input file
    fin = open(file, "rt")

    data = fin.read()
    #replace all occurrences of the required string
    #das muss noch in Event Action angepasst werden
    #data = data.replace('Dose in ', 'Dose in ,')
    #data = data.replace(' : ', ', ')
    #data = data.replace(' nano', ', nano')
    #data = data.replace(' pico', ', pico')
    #data = data.replace('.stl', '')
    data = data.replace(' ,', ';')
    #data = data.replace('[', '')
    #data = data.replace(']', '')

    #close the input file
    fin.close()
    #open the input file in write mode
    fin = open(file, "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()

class IndexTracker(object):

    def __init__(self, ax, PlotTables, AnzahlSlices): #,normDose
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.table = PlotTables
        self.slices = AnzahlSlices
        #self.normDose = normDose
        print(self.table)
        #cmap = plt.cm.rainbow
        self.ind = self.slices-1
        self.im = plt.contourf(self.table[self.ind])
        #self.im.invert_yaxis() nur bei sns.heatmap
        self.contour_axis = plt.gca()
        #plt.xlim(np.asarray(self.table).min(), np.asarray(self.table).max())
        #plt.ylim(np.asarray(self.table).min(), np.asarray(self.table).max())
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        #self.im.cla()
        self.contour_axis.clear()
        #plt.xlim(np.asarray(self.table).min(), np.asarray(self.table).max())
        #plt.ylim(np.asarray(self.table).min(), np.asarray(self.table).max())
        self.update()

    def update(self):
        #cmap = plt.cm.rainbow
        #self.im = plt.contour(self.table[self.ind])
        self.contour_axis.contourf(self.table[self.ind])
        #self.im.invert_yaxis() nur bei sns.heatmap

        #self.im.invert_yaxis() nur bei heatmap

        self.ax.set_ylabel('slice %s' % self.slices)
        plt.draw()
        #self.im.canvas.draw()
        #self.im.axes.figure.canvas.draw()

#class IndexTracker(object):
#
#    def __init__(self, ax, X, Y, Dose, normDose, AnzahlSlices):
#        self.ax = ax
#        ax.set_title('use scroll wheel to navigate images')
#
#        self.X = X
#        self.Y = Y
#        self.Dose = Dose
#        self.slices = AnzahlSlices
#        self.normDose = normDose
#        #rows, cols, self.slices = X.shape
#        #self.ind = self.slices//2
#        cmap = plt.cm.rainbow
#        self.ind = self.slices-1
#        print(self.ind)
#        self.im = self.ax.scatter(self.X[self.ind][:],self.Y[self.ind][:],c = cmap(self.normDose[self.ind]), marker = 's')
#        #self.im = ax.imshow(self.X[:, :, self.ind])
#        #sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
#        #plt.colorbar(sm)
#        plt.xlim(-1.3, 1.3)
#        plt.ylim(-1.3, 1.3)
#        self.update()
#
#    def onscroll(self, event):
#        print("%s %s" % (event.button, event.step))
#        if event.button == 'up':
#            self.ind = (self.ind + 1) % self.slices
#        else:
#            self.ind = (self.ind - 1) % self.slices
#        #print(self.ind)
#        self.ax.cla()
#        plt.xlim(-1.3, 1.3)
#        plt.ylim(-1.3, 1.3)
#        self.update()
#
#    def update(self):
#        #self.im.set_data(self.X[:, :, self.ind])
#        cmap = plt.cm.rainbow
#        self.im = self.ax.scatter(self.X[self.ind][:],self.Y[self.ind][:],c = cmap(self.normDose[self.ind]), marker = 's')
#
#        #self.im.set_data(self.X[self.slices][:],self.Y[self.slices][:])
#        self.ax.set_ylabel('slice %s' % self.slices)
#        self.im.axes.figure.canvas.draw()

main()
