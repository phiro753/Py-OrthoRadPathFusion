# Script to read curve .JSON and fiducial from Slicer
# Outputs planes (perpendicular to splines) for histology assignment
# Robert Phillips
# 2024-03/04


# The two validation (val) scripts in this repo are for performing solution validaiton as described in 

# Uses seralisers and read functions for reading from, and writing to .JSON 
# uses Polynomial.fit
# https://stackoverflow.com/questions/67728068/get-the-coefficients-of-a-polynomial-with-numpy

import matplotlib.pyplot as plt
import numpy as np
import a_readscript
from Val_CalculationClasses import ValintsCalcClass
from c_writeScript import writeFun # for writing to json files (contained in this is call to json plane file, etc)

# 02
## ...........................This is the validation script which specimen 02 didn't have any values for...........................

# 04
## For Specimen 04 Ant  # Did Ant and Post, not Lat and Med
fileS1 = "DataStorage/Specimen_04/SplineAnt_ma.json"
fileS2 = "DataStorage/Specimen_04/SplineAnt_mb.json"
fileF1 = "DataStorage/Specimen_04/F_Ant.json"
bisection = "A"
dmatrix = [[90.36,78.55],[73.85,72.83],[60.84,59.22],[53.70,53.10],[41.84,37.64],[32.12,24.80],[19.37,10.35]]
# DedicatedSplinesFor_Measurements 
# - spline_ma and spline_mb are only used to test sensitivity of spline assignment to different 3DSlicer user inputs... 
# - spline_mc is used as the measuring stick for both by comaprison against d2 labrotory measurements
# fileS1 = "DataStorage/Specimen_04/DedicatedMeasurespline/SplineAnt_ma.json"
# fileS2 = "DataStorage/Specimen_04/DedicatedMeasurespline/SplineAnt_mb.json"
fileSval = "DataStorage/Specimen_04/DedicatedMeasurespline/SplineAnt_mc.json" # Using this is both valudating with "DataStorage/Specimen_04/..." and "DataStorage/Specimen_04/DedicatedMeasurespline..."

## For Specimen 04 Post  # Did Ant and Post, not Lat and Med
# fileS1 = "DataStorage/Specimen_04/SplinePost_ma.json" 
# fileS2 = "DataStorage/Specimen_04r/SplinePost_mb.json" 
# fileF1 = "DataStorage/Specimen_04/F_Post.json" 
# bisection = "P"
# dmatrix = [[65.33,68.94],[54.30,54.05],[45.06,45.01],[33.00,33.23],[20.81,19.30]]
# DedicatedSplinesFor_Measurements 
# - spline_ma and spline_mb are only used to test sensitivity of spline assignment to different 3DSlicer user inputs... 
# - spline_mc is used as the measuring stick for both by comaprison against d2 labrotory measurements
# fileS1 = "DataStorage/Specimen_04/DedicatedMeasurespline/SplinePost_ma.json" 
# fileS2 = "DataStorage/Specimen_04/DedicatedMeasurespline/SplinePost_mb.json" 
# fileSval = "DataStorage/Specimen_04/DedicatedMeasurespline/SplinePost_mc.json" # Using this is both valudating with "DataStorage/Specimen_04/..." and "DataStorage/Specimen_04/DedicatedMeasurespline..."

# 05
# ## For Specimen 05 Lateral
# fileS1 = "DataStorage/Specimen_05/SplineLat_ma.json" 
# fileS2 = "DataStorage/Specimen_05/SplineLat_mb.json" 
# fileF1 = "DataStorage/Specimen_05/F_Lat.json" 
# bisection = "L"
# dmatrix = [[114.7,117.7],[95.43,98.23],[82.10,84.66],[69.54,72.47],[56.46,60.50],[44.97,49.33],[33.71,37.40],[20.74,25.52]]
# DedicatedSplinesFor_Measurements 
# - spline_ma and spline_mb are only used to test sensitivity of spline assignment to different 3DSlicer user inputs... 
# - spline_mc is used as the measuring stick for both by comaprison against d2 labrotory measurements
# fileS1 = "DataStorage/Specimen_05/DedicatedMeasurespline/SplineLat_ma.json" 
# fileS2 = "DataStorage/Specimen_05/DedicatedMeasurespline/SplineLat_mb.json" 
# fileSval = "DataStorage/Specimen_05/DedicatedMeasurespline/SplineLat_mc.json" # Using this is both valudating with "DataStorage/Specimen_04/..." and "DataStorage/Specimen_04/DedicatedMeasurespline..."

# ## For Specimen 05 Medial
# fileS1 = "DataStorage/Specimen_05/SplineMed_ma.json" 
# fileS2 = "DataStorage/Specimen_05/SplineMed_mb.json" 
# fileF1 = "DataStorage/Specimen_05/F_Med.json" 
# bisection = "M"
# dmatrix = [[120,122],[106,108],[93.1,95.5],[77.7,80.7],[66.6,69.5],[56.0,59.7],[43.3,47.3],[29.6,33.8]]
# DedicatedSplinesFor_Measurements 
# - spline_ma and spline_mb are only used to test sensitivity of spline assignment to different 3DSlicer user inputs... 
# - spline_mc is used as the measuring stick for both by comaprison against d2 labrotory measurements
# fileS1 = "DataStorage/Specimen_05/DedicatedMeasurespline/SplineMed_ma.json" 
# fileS2 = "DataStorage/Specimen_05/DedicatedMeasurespline/SplineMed_mb.json" 
# fileSval = "DataStorage/Specimen_05/DedicatedMeasurespline/SplineMed_mc.json"

# 06
## For Specimen 06 lateral
# fileS1 = "DataStorage/Specimen_06/SplineLat_ma.json" # Vet Tumour specimen 06
# fileS2 = "DataStorage/Specimen_06/SplineLat_mb.json" # Vet Tumour specimen 06
# fileF1 = "DataStorage/Specimen_06/F_Lat.json" # Vet Tumour specimen 06
# bisection = "L"
# dmatrix = [[148.9,152.4],[135.0,137.1],[119.3,124.3],[99.12,105.3],[85.45,80.25],[69.94,69.31],[53.66,54.12],[30.92,32.67],[20.87,22.99]]
# DedicatedSplinesFor_Measurements 
# - spline_ma and spline_mb are only used to test sensitivity of spline assignment to different 3DSlicer user inputs... 
# - spline_mc is used as the measuring stick for both by comaprison against d2 labrotory measurements
# fileS1 = "DataStorage/Specimen_06/DedicatedMeasurespline/SplineLat_ma.json" 
# fileS2 = "DataStorage/Specimen_06/DedicatedMeasurespline/SplineLat_mb.json" 
# fileSval = "DataStorage/Specimen_06/DedicatedMeasurespline/SplineLat_mc.json" ### just for validation

## For Specimen 06 Medial
# fileS1 = "DataStorage/Specimen_06/SplineMed_ma.json" # Vet Tumour specimen 06
# fileS2 = "DataStorage/Specimen_06/SplineMed_mb.json" # Vet Tumour specimen 06
# fileF1 = "DataStorage/Specimen_06/F_Med.json" 
# bisection = "M"
# dmatrix = [[150.8,160.0],[135.8,142.5],[117.8,121.8],[99.11,96.57],[79.43,78.39],[51.21,53.84],[44.93,44.75]]
# DedicatedSplinesFor_Measurements 
# - spline_ma and spline_mb are only used to test sensitivity of spline assignment to different 3DSlicer user inputs... 
# - spline_mc is used as the measuring stick for both by comaprison against d2 labrotory measurements
# fileS1 = "DataStorage/Specimen_05/DedicatedMeasurespline/SplineMed_ma.json" 
# fileS2 = "DataStorage/Specimen_05/DedicatedMeasurespline/SplineMed_mb.json" 
# fileSval = "DataStorage/Specimen_06/DedicatedMeasurespline/SplineMed_mc.json" ### just for validation


'''For user to input measurement distances from the lab - UNCOMMENT IF USE'''
# # Getting user input of lab measures
# dmatrix,Row,Column = getDist.getdistance([])

'''measurements from lab''' 
# 06
## dmatrix for specimen 6 - lateral
# dmatrix for specimen 6 - medial



## Defining classes and things
class ctrlpts:
    # Instance attribute
    def __init__(self):
        # Class instances
        # self.file = filename
        self.ylist = []
        self.xlist = []
        self.zlist = []
        # self.tuplelist = []
        self.xtup = ()
        self.ytup = ()
        self.ztup = ()
        # self.deravitive
        self.Xder = np.poly1d([])
        self.Yder = np.poly1d([])
        

    def readfunc(self, filename):
        """Getting control points from JSON files - using seraliser"""
        for f in a_readscript.extract_control_point_positions(filename):
            # Need to change list in list to tupples in list
            # S1.tuplelist.append((f[0],f[1],f[2]))
            self.xlist.append(f[0])
            self.ylist.append(f[1])
            self.zlist.append(f[2])
    
    def convLists2Tuple(self):
        """But need to convert them to tuples!"""
        self.xtup = tuple(self.xlist)
        self.ytup = tuple(self.ylist)
        self.ztup = tuple(self.zlist)

class dist():
    '''for creating plane'''
    def __init__(self):
        # Class attribtes
        self.distance = []                 # Instance attribute of 2xM matrix of distances


########## Reading control points into instances
S1 = ctrlpts()
S1.readfunc(fileS1)
S1.convLists2Tuple()

S2 = ctrlpts()
S2.readfunc(fileS2)
S2.convLists2Tuple()

F1 = ctrlpts()
F1.readfunc(fileF1)
F1.convLists2Tuple()
Fiducial = F1.xlist[0], F1.ylist[0], F1.zlist[0] # putting pt1 (aka fiducial) as tuple of (x,y,z)

### just for validation
SVal = ctrlpts()
SVal.readfunc(fileSval)
SVal.convLists2Tuple()


# Asking the user if the cut on this bisected specimen is more concave or convex
# flip = getCutCPolarity.getflip()
flip = 'convex'   #### -------------for testing

# If it is concave ask the user what the full distance from the fiducial to the end would be. 
# Necessary for computing correct biseciton plane (as will not be perpendicular to each point...)
if flip == 'concave':
    # LengthFromF = getCutCPolarity.disToEnd()
    LengthFromF = [80,80]   ## -------------for testing
    
    # Inputting the full length of fiducial to specimen end because cutting planes will be perpendicular to cutting point n-1...
    dmatrix = np.insert(dmatrix,0,LengthFromF,axis=0) 

    # # # Need to work on the concave case...
    # Make sure control points of splines are specified at each end

else:

    
    CalcVal = ValintsCalcClass(S1, S2, SVal, Fiducial)
    CalcVal.FittingPoly() # running class function to find polynimal coefficients
    CalcVal.IntersectionPointConvex(dmatrix) 
    CalcVal.diffCurves()
    ptXZ1, ptXZ2, ptYZ1, ptYZ2, npTang2Splines, npNorm2Spline, npNorm2Cut, npvecAB, npPlnCoeff, npmidpoints = CalcVal.geometricTangCalc(dmatrix)


# - calculated intersection points - get restructred into np array
S1.intx = [item[0] for item in S1.intersec] # extracting S1 intersection x values for all itersection points
S1.inty = [item[1] for item in S1.intersec] # extracting S1 intersection y values for all itersection points
S1.intz = [item[2] for item in S1.intersec] # extracting S1 intersection z values for all itersection points
S2.intx = [item[0] for item in S2.intersec] # extracting S2 intersection x values for all itersection points
S2.inty = [item[1] for item in S2.intersec] # extracting S2 intersection y values for all itersection points
S2.intz = [item[2] for item in S2.intersec] # extracting S2 intersection z values for all itersection points


# #--##
# # Writing JSON planes
# outputsuffix = fileS1.split("/", -1)[0] + "/" + fileS1.split("/", -1)[1] + "/" + "pyOutputPlanes"
# # Using the plane normals
# NormalsArray = npNorm2Cut
# # Origin or plane
# Plxorigins = np.mean([S1.intx, S2.intx], axis = 0)
# Plyorigins = np.mean([S1.inty, S2.inty], axis = 0)
# Plzorigins = np.mean([S1.intz, S2.intz], axis = 0)
# CentresArray = np.zeros((len(dmatrix), 3))
# for i in range(len(dmatrix)):
#     CentresArray[i,:] = [Plxorigins[i], Plyorigins[i], Plzorigins[i]] #     Structuring origin points into readable np array (x, y, z)
#     writefile = outputsuffix + "/" + "P_{}".format(i+1) + bisection + ".json"
#     Writ = writeFun(writefile, CentresArray[i], NormalsArray[i])
#     baseToNode = Writ.CalcBase2Node()
#     # Iteratively calling writing seraliser 
#     Writ.writeFun(baseToNode.flatten().tolist())

## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Plotting

## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------



# For visualising planes in python
size_plane = 4 # how many points will there be to define the planes?
xx_arr = np.zeros((len(dmatrix), size_plane, size_plane))
yy_arr = np.zeros((len(dmatrix), size_plane, size_plane))
zz_arr = np.zeros((len(dmatrix), size_plane, size_plane))
SVal.intersec = np.zeros((len(dmatrix), 3))

for i in range(len(dmatrix)):
    # Plotting plane
    # Define the plane equation coefficients for each plane (a, b, c, d)
    apl, bpl, cpl, dpl = npPlnCoeff[i][0], npPlnCoeff[i][1], npPlnCoeff[i][2], npPlnCoeff[i][3]  # Replace with your coefficients

    # Generate a array of grid of points
    x_vals = np.linspace(S1.intersec[i][0] - 10, S1.intersec[i][0] + 10, size_plane)
    y_vals = np.linspace(S1.intersec[i][1] - 10, S1.intersec[i][1] + 10, size_plane)
    xx, yy = np.meshgrid(x_vals, y_vals)

    # Calculate z values for each point on the grid using the plane equation
    zz = (-apl * xx - bpl * yy - dpl) / cpl

    # Appending np plane array
    xx_arr[i,:] = xx
    yy_arr[i,:] = yy
    zz_arr[i,:] = zz

    ### ------------------for validation------------------
    # try:
        
    intersect_mc = CalcVal.find_intersection_points(apl, bpl, cpl, dpl)
    SVal.intersec[i] = intersect_mc

SVal.intx = [item[0] for item in SVal.intersec] # extracting S1 intersection x values for all itersection points
SVal.inty = [item[1] for item in SVal.intersec] # extracting S1 intersection y values for all itersection points
SVal.intz = [item[2] for item in SVal.intersec] # extracting S1 intersection z values for all itersection points

'''Creating planes for plotting'''
# (for building) Creating array for plotting curves
z_new1 = np.linspace(S1.ztup[0], S1.ztup[-1], 100)
x_new1 = S1.XfromZequ(z_new1) # Creating x's from x's
y_new1 = S1.YfromZequ(z_new1) # creating y's from z's

z_new2 = np.linspace(S2.ztup[0], S2.ztup[-1], 100)
x_new2 = S2.XfromZequ(z_new2)
y_new2 = S2.YfromZequ(z_new2)

'''creating plot'''
fig = plt.figure(figsize = (12,12))
ax = fig.add_subplot(projection='3d')

'''Plotting fiducial reference points and curves'''
# ax.scatter(S1.xtup, S1.ytup, S1.ztup, label="ctrl pts File 1") # Control points from 3DSlicer
# ax.scatter(S2.xtup, S2.ytup, S2.ztup, label="ctrl pts File 2") # Control points from 3DSlicer
ax.scatter(F1.xtup,F1.ytup,F1.ztup) # Fiducial location from 3DSlicer
ax.plot(x_new1, y_new1, z_new1, c="r",label="Curve Fit to File 1") # Polynomial fitted
ax.plot(x_new2, y_new2, z_new2, c="k", label="Curve Fit to File 2") # Polynomial fitted

'''plotting intersection points calculated '''
ax.scatter(S1.intx,S1.inty,S1.intz, label="Intersection Points Curve 1")
ax.scatter(S2.intx,S2.inty,S2.intz, label="Intersection Points Curve 2")
ax.scatter(SVal.intx,SVal.inty,SVal.intz, label="Intersection Points Curve 2")




# Plotting simple gradient - NOT NEEDED
'''plotting surface of cuts'''
for p in range(len(dmatrix)):

    # plot the surface
    surf = ax.plot_surface(xx_arr[p], yy_arr[p], zz_arr[p], cmap = plt.cm.cividis)

# '''Plotting vectors - between points, normals and tangents'''
# ax.quiver(npmidpoints[:,0], npmidpoints[:,1], npmidpoints[:,2], npNorm2Spline[:,0], npNorm2Spline[:,1], npNorm2Spline[:,2], length = 2, color='r', label="norm to spline @ intersections")
# ax.quiver(npmidpoints[:,0], npmidpoints[:,1], npmidpoints[:,2], npNorm2Cut[:,0], npNorm2Cut[:,1], npNorm2Cut[:,2], length = 2, color='g', label="norm to cutting plane @ intersections")
# ax.scatter(npmidpoints[:,0], npmidpoints[:,1], npmidpoints[:,2], label = "midpoints")

# # tangent vector to the splines in 3D
# ax.quiver(npmidpoints[:,0], npmidpoints[:,1], npmidpoints[:,2], npTang2Splines[:,0], npTang2Splines[:,1], npTang2Splines[:,2], length = 2, color='m', label="avg tangent to spline @ intersections")
# # # vector between points in 3D
# ax.quiver(npmidpoints[:,0], npmidpoints[:,1], npmidpoints[:,2], npvecAB[:,0], npvecAB[:,1], npvecAB[:,2], length = 2, color='c', label="vector between spline @ intersections")

# Axis labels
# ax.set_xlabel('X-axis label')
# ax.set_ylabel('Y-axis label')
# ax.set_zlabel('Z-axis label')
ax.set_title('Anterior bisection and assigned cutting planes')

plt.axis('off')
plt.legend()
plt.gca().set_aspect('equal') # can remove to squash graph, but sets axis aspect ratio equal for visualisation...
# '''for testing by plotting paramertised tangent to curve at given intersectionpoints'''
# ax.plot([ptXZ1[0],ptXZ2[0]],[ptXZ1[1],ptXZ2[1]],[ptXZ1[2],ptXZ2[2]], label='parametertised tang in XZ')
# ax.plot([ptYZ1[0],ptYZ2[0]],[ptYZ1[1],ptYZ2[1]],[ptYZ1[2],ptYZ2[2]], label='parametertised tang in YZ')
plt.show()






# validation

bladewidth = 0.6 # blade width in mm
maDArr = np.zeros(len(dmatrix)-1)  # computed distances along spline 1 (aka Spline_ma) which should match d1 measurements from lab
for i in range(len(dmatrix)-1):
    p1S1 = np.array([S1.intx[i], S1.inty[i], S1.intz[i]])
    # print(p1S1)
    p2S1 = np.array([S1.intx[i+1], S1.inty[i+1], S1.intz[i+1]])
    squared_dist = np.sum((p1S1 - p2S1) ** 2, axis=0)
    dist = np.sqrt(squared_dist)
    maDArr[i] = dist - bladewidth

# print(S1dArr)
mbDArr = np.zeros(len(dmatrix)-1)  # computed distances along spline 1 (aka Spline_ma) which should match d1 measurements from lab
for i in range(len(dmatrix)-1):
    p1S2 = np.array([S2.intx[i], S2.inty[i], S2.intz[i]])
    p2S2 = np.array([S2.intx[i+1], S2.inty[i+1], S2.intz[i+1]])
    squared_dist = np.sum((p1S2 - p2S2) ** 2, axis=0)
    dist = np.sqrt(squared_dist)
    mbDArr[i] = dist - bladewidth

mcDArr = np.zeros(len(dmatrix)-1)  # computed distances along spline 1 (aka Spline_ma) which should match d1 measurements from lab
for i in range(len(dmatrix)-1):
    p1S2 = np.array([SVal.intx[i], SVal.inty[i], SVal.intz[i]])
    p2S2 = np.array([SVal.intx[i+1], SVal.inty[i+1], SVal.intz[i+1]])
    squared_dist = np.sum((p1S2 - p2S2) ** 2, axis=0)
    dist = np.sqrt(squared_dist)
    mcDArr[i] = dist - bladewidth

# print(f'The distances between intersection points on spline_ma were {maDArr}')
# print(f'The distances between intersection points on spline_mc were {mcDArr}')
# print(f'The distances between intersection points on spline_mb were {mbDArr}')
print(maDArr)
print(mcDArr)
print(mbDArr)