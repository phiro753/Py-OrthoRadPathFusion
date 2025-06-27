# Script to read markup curves/spline .JSON and fiducial .JSON from Slicer
# Robert Phillips
# Created 2024-03/04 (working edits)

# Details on script excecution:
# - files with prefex "a_" use seralisers and read functions for reading from .JSON markup files in a schema of markup object '.json' export from 3DSlicer
# - files with prefex "b_" are called to execute computations 
# - files with prefex "c_" use seralisers and write functions to write .jcon markup files in a schema for importing plane objects into 3DSlicer
# Computed planes model dissection cuts during histology and prependicular to the average of the splines at the two intersection points  
# (Warnings)
# (Dont use .mrk.json exported from 3DSlicer. You'll need to change the a_JSONObjectRead.py if you want to do this...)

# Things to import
import matplotlib.pyplot as plt
import numpy as np
import a_readscript
from b_CalculationClasses import CalcClasses
from c_writeScript import writeRunning
from c_writeScript import writeFunschema # for writing to 3DSlicer schema (contained in this is a call to json plane file, etc)


# required for gui input by user of labrotory measurements 
import os
import a_importguis as GUIs
import tkinter as tk

## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 ###For testing with provided .json files (offset measurements are in dmatrix variable below) ###
## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 06
## For Specimen 06 Lateral bisection
dmatrix = [[148.9,152.4],[135.0,137.1],[119.3,124.3],[99.12,105.3],[85.45,80.25],[69.94,69.31],[53.66,54.12],[30.92,32.67],[20.87,22.99]]
offset = [910,1970,1265,0,0,0,0,0,0]  # um, offset of histology from cut face (due to thickness*number of microtomb slices).
sign = -1 # should the offset numbers be subtracted (shifted back towards fid_ref) dissection blockface or added to? (subtracted from in this testcase... it depends on which side of dissection sections were processed in histology)
fileS1 = "DataStorage/Specimen_06/SplineLat_ma.json" # Vet Tumour specimen 06
fileS2 = "DataStorage/Specimen_06/SplineLat_mb.json" # Vet Tumour specimen 06
fileF1 = "DataStorage/Specimen_06/F_Lat.json" # Vet Tumour specimen 06
bisection = "L"

## For Specimen 06 Medial bisection
# dmatrix = [[150.8,160.0],[135.8,142.5],[117.8,121.8],[99.11,96.57],[79.43,78.39],[51.21,53.84],[44.93,44.75]]
# offset = [0,0,0,0,0,0,0]  # um, offset of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Specimen_06/SplineMed_ma.json" # Vet Tumour specimen 06
# fileS2 = "DataStorage/Specimen_06/SplineMed_mb.json" # Vet Tumour specimen 06
# fileF1 = "DataStorage/Specimen_06/F_Med.json" 
# bisection = "M"

## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Uncomment sections below for full user input (will require commenting out sections above)
## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# '''Asking User: Opening file explorer and asking user to select the .json's that are needed'''
# file_selector = GUIs.FileSelector()
# ## Selecting Spline 1 (i.e. Spline_ma)
# tk.messagebox.showinfo("Message", "Welcome! Please select the .json file for your Spline 1.") # Show a message
# fileS1 = file_selector.select_file() # Select a file
# ## Selecting Spline 2 (i.e. Spline_mb)
# tk.messagebox.showinfo("Message", "Now, please select the .json file for your Spline 2.") # Show a message
# fileS2 = file_selector.select_file()
# ## Selecting Reference feature (i.e. Fid_Med)
# tk.messagebox.showinfo("Message", "Again, please select the .json file for your reference feature.") # Show a message
# fileF1 = file_selector.select_file()
# # Seems when uncomment this it buggers up the GUI for getting output filepath

# '''Asking User: Check if want .json exported and where to export them'''
# app_DirOut = GUIs.OutputDecision()
# app_DirOut = app_DirOut.run()
# if not app_DirOut == None:
#     '''Asking User: Chosing which bisection'''
#     WhichBisection = GUIs.StringReturn()
#     bisection = WhichBisection.run()

# print(fileF1)
# '''User input dmatrix (lab measurements): comment out if dmatrix is being specified in script...'''
# app_matrix = GUIs.NumberTableGUI()
# # Calling for user input
# dmatrix = app_matrix.table

# '''Asking the user if want to input microtomb offsets'''
# offset_selector = GUIs.OffsetInputs(len(dmatrix)) 
# offset, sign = offset_selector.get_offsets() # calling gui to 1) ask if offsets were recoreded 2) what they were and what polarity
# print(sign)
## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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
        """But need to convert control points that define markups to tuples!"""
        self.xtup = tuple(self.xlist)
        self.ytup = tuple(self.ylist)
        self.ztup = tuple(self.zlist)

class dist():
    '''for creating plane'''
    def __init__(self):
        # Class attribtes
        self.distance = []      # Instance attribute of 2xM matrix of distances/measurements


########## Reading markups into class instances which were created previous 
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

# Assuming planes are perpendicular to cut face 
CalcConvex = CalcClasses(S1,S2,Fiducial)
CalcConvex.FittingPoly()                    # running class function to find polynimal coefficients
CalcConvex.IntersectionPointConvex(dmatrix) # finding intersection points of all measruements with each spline
CalcConvex.diffCurves()                     # Differentiating spline polynomials at each intersection point and recording these

# Doing geometric calculations to find points, vectors and assigned plane coefficients
try:
    ptXZ1, ptXZ2, ptYZ1, ptYZ2, npTang2Splines, npNorm2Spline, npNorm2Cut, npvecAB, npPlnCoeff, npmidpoints = CalcConvex.geometricTangCalc(dmatrix)
except:
    print('Calculations are failing. Have you entered in any labrotory offsets?')

# - calculated intersection points - get restructred into np array
S1.intx = [item[0] for item in S1.intersec] # extracting S1 intersection x values for all itersection points
S1.inty = [item[1] for item in S1.intersec] # extracting S1 intersection y values for all itersection points
S1.intz = [item[2] for item in S1.intersec] # extracting S1 intersection z values for all itersection points
S2.intx = [item[0] for item in S2.intersec] # extracting S2 intersection x values for all itersection points
S2.inty = [item[1] for item in S2.intersec] # extracting S2 intersection y values for all itersection points
S2.intz = [item[2] for item in S2.intersec] # extracting S2 intersection z values for all itersection points


# Attempting to write planes in files (writing to .json in schema for import to 3DSlicer)
try:
    Writing = writeRunning(dmatrix, offset, sign, S1, S2, npNorm2Cut)
    Writing.write_to_folder(app_DirOut, bisection)
except Exception as e:
    app_DirOut = fileS1.split("/", -1)[0] + "/" + fileS1.split("/", -1)[1] + "/" + "pyOutputPlanes"
    print(f'Currently you are not getting any files out, I will put them in {app_DirOut}')
    Writing.write_to_folder(app_DirOut, bisection)









## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Plotting
# not necessary for export of .json in scheme for import into 3DSlicer but is good to visualise

## ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# For plotting planes in python - note this is just biseciton planes, it DOES NOT have a microtomb offset
size_plane = 4 # how many points will there be to define the planes?
xx_arr = np.zeros((len(dmatrix), size_plane, size_plane))
yy_arr = np.zeros((len(dmatrix), size_plane, size_plane))
zz_arr = np.zeros((len(dmatrix), size_plane, size_plane))

for i in range(len(dmatrix)):
    # Plotting plane
    # Define the plane equation coefficients for each plane (a, b, c, d)
    apl, bpl, cpl, dpl = npPlnCoeff[i][0], npPlnCoeff[i][1], npPlnCoeff[i][2], npPlnCoeff[i][3]  # Replace with your coefficients

    # Generate a array of grid of points
    x_vals = np.linspace(S1.intersec[i][0] - 15, S1.intersec[i][0] + 15, size_plane)
    y_vals = np.linspace(S1.intersec[i][1] - 15, S1.intersec[i][1] + 15, size_plane)
    xx, yy = np.meshgrid(x_vals, y_vals)

    # Calculate z values for each point on the grid using the plane equation
    zz = (-apl * xx - bpl * yy - dpl) / cpl

    # Appending np plane array
    xx_arr[i,:] = xx
    yy_arr[i,:] = yy
    zz_arr[i,:] = zz

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
# fig.patch.set_facecolor('none')
ax = fig.add_subplot(projection='3d')

'''Plotting fiducial reference points and curves'''
ax.scatter(F1.xtup,F1.ytup,F1.ztup) # Fiducial location from 3DSlicer
ax.plot(x_new1, y_new1, z_new1, c="r",label="Curve Fit to File 1") # Polynomial fitted
ax.plot(x_new2, y_new2, z_new2, c="k", label="Curve Fit to File 2") # Polynomial fitted


'''plotting intersection points calculated '''
ax.scatter(S1.intx,S1.inty,S1.intz, label="Intersection Points Curve 1")
ax.scatter(S2.intx,S2.inty,S2.intz, label="Intersection Points Curve 2")

# Plotting simple gradient - NOT NEEDED
'''plotting surface of cuts'''
for p in range(len(dmatrix)):

    # plot the surface
    surf = ax.plot_surface(xx_arr[p], yy_arr[p], zz_arr[p], cmap = plt.cm.cividis)

# '''Plotting vectors - between points, normals and tangents'''
ax.quiver(npmidpoints[:,0], npmidpoints[:,1], npmidpoints[:,2], npNorm2Spline[:,0], npNorm2Spline[:,1], npNorm2Spline[:,2], length = 2, color='r', label="norm to spline @ intersections")
ax.quiver(npmidpoints[:,0], npmidpoints[:,1], npmidpoints[:,2], npNorm2Cut[:,0], npNorm2Cut[:,1], npNorm2Cut[:,2], length = 2, color='g', label="norm to cutting plane @ intersections")
ax.scatter(npmidpoints[:,0], npmidpoints[:,1], npmidpoints[:,2], label = "midpoints")

# # tangent vector to the splines in 3D
ax.quiver(npmidpoints[:,0], npmidpoints[:,1], npmidpoints[:,2], npTang2Splines[:,0], npTang2Splines[:,1], npTang2Splines[:,2], length = 2, color='m', label="avg tangent to spline @ intersections")
# # vector between points in 3D
ax.quiver(npmidpoints[:,0], npmidpoints[:,1], npmidpoints[:,2], npvecAB[:,0], npvecAB[:,1], npvecAB[:,2], length = 2, color='c', label="vector between spline @ intersections")

'''for testing by plotting paramertised tangent to curve at given intersectionpoints'''
ax.plot([ptXZ1[0],ptXZ2[0]],[ptXZ1[1],ptXZ2[1]],[ptXZ1[2],ptXZ2[2]], label='parametertised tang in XZ')
ax.plot([ptYZ1[0],ptYZ2[0]],[ptYZ1[1],ptYZ2[1]],[ptYZ1[2],ptYZ2[2]], label='parametertised tang in YZ')

# Axis labels
ax.set_xlabel('X-axis label')
ax.set_ylabel('Y-axis label')
ax.set_zlabel('Z-axis label')
for labeli in plt.gca().axes.get_xticklabels():
    labeli.set_visible(False)
for labeli in plt.gca().axes.get_yticklabels():
    labeli.set_visible(False)
for labeli in plt.gca().axes.get_zticklabels():
    labeli.set_visible(False)
ax.grid(False)
ax.set_axis_off()
try:
    ax.set_title('Histology Assignment Planes From {} Bisection'.format(bisection))
except Exception as e:
    ax.set_title('Histology Assignment Planes')
    print('Ok we are not writing anything to file, hope you\'re ok with that')

# plt.legend()
plt.gca().set_aspect('equal') # can remove to squash graph, but sets axis aspect ratio equal for visualisation...
plt.show()
