"""
Description: Main script for visualization and output of histology cut planes into
 JSON for 3D slicer import
Hierachy: Main file

History:
> Written by Robert Phillips 2024-04
> Rewritten by Jamie Uy De Baron 2024-11

"""

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
""" READ ME

    THIS FILE:
    # Calls all other files to handle read input, process data, and produce output
    # Plots planes for visualization (Future development might see this in a different module)
    # Debug/test module using input data from 'DataStorage' (already in-file, no need to use the UI), (Future development will see this using M3)
    
    Details on file names and therefore types:
    # - files with prefix "a_" use seralisers and read functions for reading from .JSON markup files in a schema of markup object '.json' export from 3DSlicer
    # - files with prefix "b_" are called to execute computations 
    # - files with prefix "c_" use seralisers and write functions to write .jcon markup files in a schema for importing plane objects into 3DSlicer
    # - files with prefix "d_" are calculation methods that perform quantitative analysis on plane orientation and difference - usage is unnecessary
    # - files with prefix "e_" were one-off usage for report writing and visualization
    
    Methods for cut plane projection:
    # Method 1 (M1): Computed planes model dissection cuts during histology and prependicular to the average of the splines at the two intersection points  
    # Method 2 (M2): Utilizing the vector between the two spline intersection points and the vector from the previous spline cut point to the end of the spline on one side
    # Method 3 (M3): Involves a third spline and the two original ones, to reduce the 'assumptions' made during calculation

    
    WARNINGS
    # (Dont use .mrk.json exported from 3DSlicer. You'll need to change the a_JSONObjectRead.py if you want to do this...)

"""
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" RUNNING INSTRUCTIONS:

Change user flags to True/False as needed
> Sample specimens for testing are in b_Specimens.py file

 These are pre-made inputs for testing without having to use/go through full user GUI,
        Uncommenting must be changed in b_Specimens.py file if inputUI below is set to 
        false
"""

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Produces a simple User-Interface for 3DSlicer created spline and laboratory measurement inputs
inputUI = False  

# If user wants to turn off writing json planes to file for input to 3DSlicer
writeOn = False 

# If user wants to have quick visualisation of the planes they are plotting with their selected method
plotsimple = True

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Administrative setup """

# Pre-written module import statements
import numpy as np # For array calculations
import tkinter as tk

# Written module import statements
import a_importguis as GUIs # For user interface
from b_SplineCalculations import SplineClass, SplineProcessingClass # For spline processing
from b_GeometricManipulations import GeometricM1Class, GeometricM2Class, GeometricM3Class # For plane calculations
from c_writeScript import writeRunning
import matplotlib.pyplot as plt  # For simple plotting funcitonality

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" end-User Interface for data input """

# Method Selection
selector = GUIs.MethodSelector()
selected_method = selector.run()
if selected_method:
    print(f"Selected Method: M{selected_method}")
else:
    print("No method was selected.")

# Running GUIs
if inputUI:
    
    if selected_method == 1 or selected_method == 2:

        # File selection
        file_selector = GUIs.FileSelector()
        tk.messagebox.showinfo("Message", "Please select the .json file for your Spline 1.") 
        fileS1 = file_selector.select_file()
        print(f"Selected Spline 1: {fileS1}")

        tk.messagebox.showinfo("Message", "Now, please select the .json file for your Spline 2.")
        fileS2 = file_selector.select_file()
        print(f"Selected Spline 2: {fileS2}")

        tk.messagebox.showinfo("Message", "Again, please select the .json file for your reference feature.") # Show a message
        fileF1 = file_selector.select_file()
        print(f"Selected Reference Feature: {fileF1}")

        # Number table input
        dmatrix_gui = GUIs.NumberTableGUI()
        dmatrix = dmatrix_gui.run()
        print(f"Input dmatrix: {dmatrix}")

    elif selected_method == 3:

        # File selection
        file_selector = GUIs.FileSelector()
        tk.messagebox.showinfo("Message", "Please select the .json file for your Spline 1.") 
        fileS1 = file_selector.select_file()
        print(f"Selected Spline 1: {fileS1}")

        tk.messagebox.showinfo("Message", "Now, please select the .json file for your Spline 2.")
        fileS2 = file_selector.select_file()
        print(f"Selected Spline 2: {fileS2}")

        # For M3
        tk.messagebox.showinfo("Message", "Now, please select the .json file for your Spline 3.")
        fileS3 = file_selector.select_file()
        print(f"Selected Spline 3: {fileS3}")

        tk.messagebox.showinfo("Message", "Again, please select the .json file for your reference feature.")
        fileF1 = file_selector.select_file()
        print(f"Selected Reference Feature: {fileF1}")

        # Number table input
        dmatrix_gui = GUIs.NumberTableGUIM3()
        dmatrix = dmatrix_gui.run()
        print(f"Input dmatrix: {dmatrix}")

    # Offset inputs
    offset_gui = GUIs.OffsetInputs(len(dmatrix))
    offsets, sign = offset_gui.run()
    print(f"Offsets: {offsets}, Sign: {sign}")
else:
    from b_Specimens import name, dmatrix, offsets, sign, fileS1, fileS2, fileS3, fileF1, bisection # comment this in if using sample data

if selected_method == 3:
    useM3 = True
else:
    useM3 = False

if writeOn:
    # Output directory decision
    output_decision = GUIs.OutputDecision()
    output_dir = output_decision.run()

    if output_dir:

        print(f"Output Directory: {output_dir}")  # Now correctly prints the output directory
        bisection = GUIs.StringReturn().run()
        print(f"Bisection Suffix: {bisection}")
    else:
        print("No output directory selected.")
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Spline class setup """

# Defining splines with b_SplineCalculations and SpineClass
S1 = SplineClass() # Sets the spline markup points to a processable class
S1.readfunc(fileS1) # Creates lists of the coordinates of each sample point
S1.convLists2Tuple()

S2 = SplineClass()
S2.readfunc(fileS2)
S2.convLists2Tuple()

if useM3:
    # For M3
    S3 = SplineClass()
    S3.readfunc(fileS3)
    S3.convLists2Tuple()
else:
    S3 = SplineClass() # If not using M3, S3 is just an empty spline class

F1 = SplineClass()
F1.readfunc(fileF1)
F1.convLists2Tuple()
Fiducial = F1.xlist[0], F1.ylist[0], F1.zlist[0]

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Process splines data using SplineProcessingClass
splineData = SplineProcessingClass(S1, S2, S3, Fiducial, useM3)
splineData.fitPoly()
splineData.splineIntersecPoints(dmatrix)
splineData.diffCurves()
splineData.midpoints()
splineData.betweenSplines()
npmidpoints = S1.midpoints

# For method 3, reuse splineData for all processing (no need for separate splineDataM3)
# All necessary processing is already handled above based on useM3 flag

# Calculated intersection points
S1.intx = [item[0] for item in S1.intersec] # Extracting S1 intersection x values for all itersection points
S1.inty = [item[1] for item in S1.intersec] # Extracting S1 intersection y values for all itersection points
S1.intz = [item[2] for item in S1.intersec] # Extracting S1 intersection z values for all itersection points
S2.intx = [item[0] for item in S2.intersec] # Extracting S2 intersection x values for all itersection points
S2.inty = [item[1] for item in S2.intersec] # Extracting S2 intersection y values for all itersection points
S2.intz = [item[2] for item in S2.intersec] # Extracting S2 intersection z values for all itersection points
if selected_method == 3:
    S3.intx = [item[0] for item in S3.intersec] # Extracting S2 intersection x values for all itersection points
    S3.inty = [item[1] for item in S3.intersec] # Extracting S2 intersection y values for all itersection points
    S3.intz = [item[2] for item in S3.intersec] # Extracting S2 intersection z values for all itersection points

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Method 1 """

CalcM1 = GeometricM1Class(S1, S2)
CalcM1.geometricTangCalcs(S1, S2)
M1npPlnCoeff = CalcM1.planeCoeffs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Method 2 """

CalcM2 = GeometricM2Class(S1, S2, Fiducial)
CalcM2.endpoints()
CalcM2.calculate_normal_vectors()
CalcM2.CuttingPlane()
M2npPlnCoeff = CalcM2.planeCoefficients
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Method 3 """

if selected_method == 3:
    CalcM3 = GeometricM3Class(S1, S2, S3)
    CalcM3.vecCalcs()
    CalcM3.crossProd()
    CalcM3.cuttingPlane()
    M3npPlnCoeff = CalcM3.planeCoefficients
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Write to json module """

# Construct and define app_DirOut before entering try-except
if not fileS1:
    raise ValueError("fileS1 is undefined. Cannot construct output directory.")

# Ensure the directory exists before trying to write files
# os.makedirs(output_dir, exist_ok=True)

# Set which method outputs planes
if selected_method == 1:
    npPlnCoeffs = M1npPlnCoeff
if selected_method == 2:
    npPlnCoeffs = M2npPlnCoeff
if selected_method == 3:
    npPlnCoeffs = M3npPlnCoeff

# Now, handle the writing process
if writeOn:
    try:
        # Attempt to write to the specified output folder
        print(f"Writing planes to: {output_dir}")
        Writing = writeRunning(dmatrix, offsets, sign, S1, S2, npPlnCoeffs[:, :3]) 
        Writing.write_to_folder(output_dir, bisection)
    except Exception as e:
        # Log the error for debugging
        print(f"Error during writing: {e}")

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Plotting module """
if plotsimple == True:
    
    """ Plotting admin """
    # Creating plot
    fig = plt.figure(figsize = (12,12))
    ax = fig.add_subplot(projection='3d')

    # Creating array for plotting curves
    z_new1 = np.linspace(S1.ztup[0], S1.ztup[-1], 100)
    x_new1 = S1.XfromZequ(z_new1) # Creating x's from x's
    y_new1 = S1.YfromZequ(z_new1) # creating y's from z's


    z_new2 = np.linspace(S2.ztup[0], S2.ztup[-1], 100)
    x_new2 = S2.XfromZequ(z_new2)
    y_new2 = S2.YfromZequ(z_new2)

    # Plotting fiducial reference point and curves
    ax.scatter(F1.xlist,F1.ylist,F1.zlist, c="g") # Fiducial location from 3DSlicer
    ax.plot(x_new1, y_new1, z_new1, c="r", label="Curve Fit to File 1") # Polynomial fitted
    ax.plot(x_new2, y_new2, z_new2, c="k", label="Curve Fit to File 2") # Polynomial fitted

    # Plotting intersection points calculated on S1 and S2 (same between all methods)
    ax.scatter(S1.intx,S1.inty,S1.intz, label="Intersection Points Curve 1")
    ax.scatter(S2.intx,S2.inty,S2.intz, label="Intersection Points Curve 2")

    # Calculating planes for plotting
    size_plane = 4
    xx_arr = np.zeros((len(npPlnCoeffs), size_plane, size_plane))
    yy_arr = np.zeros((len(npPlnCoeffs), size_plane, size_plane))
    zz_arr = np.zeros((len(npPlnCoeffs), size_plane, size_plane))
    for i in range(len(npPlnCoeffs)):
        # Extract plane coefficients
        a_plot, b_plot, c_plot, d_plot = npPlnCoeffs[i]
        
        # Generate grid points
        x_vals = np.linspace(S2.intersec[i][0] - 15, S2.intersec[i][0] + 15, size_plane)
        y_vals = np.linspace(S2.intersec[i][1] - 15, S2.intersec[i][1] + 15, size_plane)
        xx, yy = np.meshgrid(x_vals, y_vals)
        
        # Compute z values with error handling for c_plot == 0
        if np.isclose(c_plot, 0):
            zz = np.full_like(xx, np.nan)  # Or handle as a constant plane
            print(f"Skipping plane {i}: c_plot is zero, parallel to xy-plane.")
        else:
            zz = (-a_plot * xx - b_plot * yy - d_plot) / c_plot

        # Append arrays for plotting
        xx_arr[i, :] = xx
        yy_arr[i, :] = yy
        zz_arr[i, :] = zz

    # Doing the plotting
    for p in range(len(npPlnCoeffs)):
        # Plot the surface
        surf_m2 = ax.plot_surface(
            xx_arr[p], yy_arr[p], zz_arr[p], 
            alpha=0.6, cmap=plt.cm.coolwarm, label=f"Plane {p+1}")

    plt.gca().set_aspect('equal') # can remove to squash graph, but sets axis aspect ratio equal for visualisation...
    plt.show()
	