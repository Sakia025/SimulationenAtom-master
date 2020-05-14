import numpy as np
import pandas as pd


#----main---------------------------------------------------------------------------

def main():
    cog_path = '/Users/smller/Simulationen/python/COG_Fusion/COG.txt'
    SavePossibleFilenames_path = "/Users/smller/Simulationen/python/Plot/FilenamesGridpointsPossible.txt"

    FilenamesUndCog = ReadFilenamesAndCOG(cog_path)
    GridPoints = create3DGridPoints(min = -4, max = 4, NumberOfPoints = 10)

    names = FilenamesUndCog.index
    cogs = FilenamesUndCog['cog'].values

    GridPossibleVolumes, GridPointsInVolumes = WriteGridPointsPossibleVolumesTXT(cogs, names, GridPoints, CubeLength = 0.1)

    fmt = "%5s" #weil dtype=object
    np.savetxt(SavePossibleFilenames_path, np.column_stack((GridPointsInVolumes, GridPossibleVolumes)), fmt = fmt)

    #outfile = open(SavePossibleFilenames_path, "w")
    #outfile.write("\n".join(str(i) for i in GridPossibleVolumes))
    #outfile.close()
    return

#----Einlesen der Daten---------------------------------------------------------------------------

def makeArray(text):
    return np.fromstring(text,sep=',')

def FindStlFiles(StlPath):
    filenames = [f for f in listdir(StlPath) if f.endswith('.stl')]
    return filenames

def removeStlEnding(filename):
    newFilename = filename.replace(".stl", "")
    return newFilename

def ReadFilenamesAndCOG(cog_path):
    cog_df = pd.read_csv(cog_path, sep = ';', names = ['Filename', 'cog'], skiprows = 1)
    cog_df = cog_df.set_index('Filename')
    cog_df['cog'] = cog_df['cog'].apply(makeArray)
    return cog_df

#----erzeugen des 3D Grids---------------------------------------------------------------------------

def create3DGridPoints(min, max, NumberOfPoints):
    #3D Pointgrid (symmetric)
    x = np.linspace(min,max,NumberOfPoints)
    y = x
    z = x

    #https://stackoverflow.com/questions/18253210/creating-a-numpy-array-of-3d-coordinates-from-three-1d-arrays
    GridPoints = np.vstack(np.meshgrid(x,y,z)).reshape(3,-1).T
    return GridPoints

#----Vorsortierung, ob Punkt in bestimmter Stlfile sein kann---------------------------------------------------------------------------

def AreXYZinCube(grid, cog, CubeLength):
    AreInside = IsXYZinCube(grid[:,0], cog[0], CubeLength) & IsXYZinCube(grid[:,1], cog[1], CubeLength) &IsXYZinCube(grid[:,2], cog[2], CubeLength)
    return AreInside

def IsXYZinCube(x, cog_x, CubeLength):
    xmin = cog_x - CubeLength
    xmax = cog_x + CubeLength
    IsInside = (x >= xmin) & (x <= xmax)
    return IsInside

def WriteGridPointsPossibleVolumesTXT(cogs, names, GridPoints, CubeLength):
    GridPossibleVolumes = np.empty(np.shape(GridPoints[:,0]), dtype = object)
    for index in range(len(names)):
        cog = cogs[index]
        name = names[index]

        Gridindices = np.where(AreXYZinCube(GridPoints, cog, CubeLength))
        Gridindices = np.asarray([Gridindices[0]]).flatten()

        for i in Gridindices:
            GridPossibleVolumes[i] = np.append(GridPossibleVolumes[i],name)

    GPV = []
    Grid = []
    for entry_nr in range(len(GridPossibleVolumes)):
        entry = GridPossibleVolumes[entry_nr]
        if entry is not None:
            GPV.append(entry[1:])
            for i in range(len(entry[1:])):
                Grid.append(GridPoints[entry_nr])

    GPV = np.asarray(GPV).flatten()
    Grid = np.asarray(Grid)
    return GPV, Grid

#----main-----------------------------------------------------------------------

main()
