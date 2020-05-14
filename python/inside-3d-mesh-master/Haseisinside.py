from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot
from os import listdir
from os.path import isfile, join
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from matplotlib.patches import Rectangle
from matplotlib.colors import Normalize
import numpy as np
import pandas as pd
from is_inside_mesh import is_inside_turbo as is_inside
import matplotlib as mpl

def makeArray(text):
    return np.fromstring(text,sep=',')


def main():

    mypath = '/Users/smller/Simulationen/ccb-plaque/models/'
    onlyfiles = [f for f in listdir(mypath) if f.endswith('.stl')]

    data_path = '/Users/smller/Simulationen/ccb-plaque-build/Daten/daten_0_copy.txt'
    cog_path = '/Users/smller/Simulationen/python/COG_Fusion/COG.txt'
    #replace(cog_path)
    cog_df = pd.read_csv(cog_path, sep = ';', names = ['Filename', 'cog'], skiprows = 1)
    cog_df = cog_df.set_index('Filename')
    cog_df['cog'] = cog_df['cog'].apply(makeArray)
    #Simulationsdaten einlesen
    #replace(data_path)
    Simulationsdaten = pd.read_csv(data_path, names = ['Text' , 'Filename' , 'Dose'  , 'Unit'])
    Simulationsdaten = Simulationsdaten.set_index('Filename')
    Simulationsdaten = Simulationsdaten.head(n=len(onlyfiles))  # fliegt später raus, aktuell speichert event Action aber jeden Detector zweimal ab, beim zweiten Mal mit 0Dosis
    #print(Simulationsdaten['Dose'])

    DosisUndCog = pd.concat([cog_df, Simulationsdaten],axis = 1)
    #print(DosisUndCog['Dose'])
    #print(DosisUndCog)
    #STLObjektDaten = Simulationsdaten.loc['Sclera:1_23.stl']
    #Dosis = STLObjektDaten['Dose']
    #Einheit = STLObjektDaten['Unit']
    #ende

    # Load the STL files and add the vectors to the plot
    Dosis_Werte = np.zeros(len(onlyfiles))

    #dummy Eintrag, damit vstack genutzt werden kann, wird später weggeschnitten
    cogs = np.array([0,1,2])
    i = 0
    for file in onlyfiles:
        file = file[:-4] #to remove the .stl in the string

        STLObjektDaten = DosisUndCog.loc[file]
        Dosis = STLObjektDaten['Dose']

        Einheit = STLObjektDaten['Unit']
        COG = STLObjektDaten['cog']

        Dosis_Werte[i] = Dosis
        cogs = np.vstack((cogs,np.array(COG)))

        i = i+1

    cogs = cogs[1:] #muss sein da der erste eintrag von cogs nur ein dumy war, damit vstack geutzt werden kann
    fig, ax = plt.subplots()
    cmap = plt.cm.rainbow
    norm = mpl.colors.Normalize(vmin=Dosis_Werte.min(), vmax=Dosis_Werte.max())

    #print((cogs[:,2].max()-cogs[:,2].min())/2)
    wanted_zStepSize = 0.1
    zNumberOfSteps = int((cogs[:,2].max()-cogs[:,2].min())/wanted_zStepSize)
    real_zStepSize = (cogs[:,2].max()-cogs[:,2].min())/zNumberOfSteps

    speichernummer = 0
    for z in np.linspace(cogs[:,2].min(),cogs[:,2].max(), zNumberOfSteps):
        speichernummer = speichernummer +1
        z_true_indices = np.where((cogs[:,2]>=z) & (cogs[:,2]<= z + real_zStepSize))         #hier später vlt ein in range angeben falls sonst durch nicht würfel am Rande des Auges Probleme auftreten
        cogs_z = cogs[z_true_indices]
        Dosis_Werte_z = Dosis_Werte[z_true_indices]


        x = cogs_z[ : , 0]
        y = cogs_z[ : , 1]
        plt.scatter(x,y,c = cmap(norm(Dosis_Werte_z)), marker = 's')

        width = 0.1 #Breite der Detektorwürfel
        height = 0.1
        #print(len(x))
        #Rechtecke, brauchen ewig, besser scatter marker = 's'
        #for i in range(0, len(x)):
        #    ax.add_patch(Rectangle(xy=(x[i]-width/2, y[i]-height/2) ,width=width, height=height, linewidth=1, color=cmap(norm(Dosis_Werte[i])), fill=False))
        #    ax.axis('equal')

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        plt.colorbar(sm)
        plt.xlim(-1.3, 1.3)
        plt.ylim(-1.3, 1.3)
        #plt.title("Initial_windows_MA_plot")
        #plt.xlabel("log10 base mean")
        #plt.ylabel("log2 fold-change")
        #plt.show()

        plt.savefig("Ergebnisse/Plots/Auge_z_" + str(speichernummer) +".png")
        plt.clf()
    #wird von Snakemake in Simulationen aufgerufen, desshalb landet es dort, wenn ich es in Python aufrufe dann anderer pfad



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
    #data = data.replace(' ,', ';')
    data = data.replace('[', '')
    data = data.replace(']', '')

    #close the input file
    fin.close()
    #open the input file in write mode
    fin = open(file, "wt")
    #overrite the input file with the resulting data
    fin.write(data)
    #close the file
    fin.close()

main()
