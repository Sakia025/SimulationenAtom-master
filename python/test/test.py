import numpy as np

def create3DGridPoints(min, max, NumberOfPoints):
#3D Pointgrid (symmetric)
    x = np.linspace(min,max,NumberOfPoints)
    y = x
    z = x

    #https://stackoverflow.com/questions/18253210/creating-a-numpy-array-of-3d-coordinates-from-three-1d-arrays
    GridPoints = np.vstack(np.meshgrid(x,y,z)).reshape(3,-1).T
    return GridPoints

def AreXYZinCube(grid, cog, CubeLength):
    AreInside = IsXYZinCube(grid[:,0], cog[0], CubeLength) & IsXYZinCube(grid[:,1], cog[1], CubeLength) &IsXYZinCube(grid[:,2], cog[2], CubeLength)
    return AreInside

def IsXYZinCube(x, cog_x, CubeLength):
    xmin = cog_x - CubeLength
    xmax = cog_x + CubeLength
    IsInside = (x >= xmin) & (x <= xmax)
    return IsInside

GridPoints = create3DGridPoints(min = 0, max = 1, NumberOfPoints = 2)
GridPossibleVolumes = np.empty(np.shape(GridPoints[:,0]), dtype = object)
cogs = np.array([[0,1,1],[0,0.8,0.9],[0,0.98,0.93],[1.1,1,0.9]])
names = np.array(['drin', 'nicht', 'im selben', 'woanders'])
GridPossibleVolumes = WriteGridPointsPossibleVolumesTXT(cogs, names, GridPoints, CubeLength = 0.1)

def WriteGridPointsPossibleVolumesTXT(cogs, names, GridPoints, CubeLength):
    for index in range(len(names)):
        cog = cogs[index]
        name = names[index]

        Gridindices = np.where(AreXYZinCube(GridPoints, cog, CubeLength))
        Gridindices = np.asarray([Gridindices[0]]).flatten()

        for i in Gridindices:
            GridPossibleVolumes[i] = np.append(GridPossibleVolumes[i],name)

    #print(GridPossibleVolumes)
    return GridPossibleVolumes
