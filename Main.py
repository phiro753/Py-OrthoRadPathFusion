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
# If making false, turn to commenting/uncommenting secitons in b_Specimens.py file for guiding DataStorage searching
if inputUI == False:
    selected_method = 3 # Manually change this method between 1, 2, and 3 for M1, M2 and M3

# If user wants to turn off writing json planes to file for input to 3DSlicer
writeOn = False 

# Make true if you want to plot the planes
plot = True # If true, plot function is on
plotCommon = True # Plot the common intersection points of the two splines
plotAllS3intersect = False # Plot all intersection points of S3 with S1 and S2
plotM1 = True # Plot the M1 plane
plotM2 = False # Plot the M2 plane
plotM3 = False # Plot the M3 plane

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
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" end-User Interface for data input """
if inputUI:
    
    # Method Selection
    selector = GUIs.MethodSelector()
    selected_method = selector.run()
    
    if selected_method:
        print(f"Selected Method: M{selected_method}")
    else:
        print("No method was selected.")
    
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

# For M3
S3 = SplineClass()
S3.readfunc(fileS3)
S3.convLists2Tuple()

F1 = SplineClass()
F1.readfunc(fileF1)
F1.convLists2Tuple()
Fiducial = F1.xlist[0], F1.ylist[0], F1.zlist[0]

if selected_method == 3:
    useM3 = True
else:
    useM3 = False

# Notes - the problem with modularising it this much is that the third spline needs to always be measured even if using M1 or M2

# Processing splines data with b_SplineCalculations and SplineProcessingClass
splineData = SplineProcessingClass(S1, S2, S3, Fiducial, useM3) # Processes the spline sample points
splineData.fitPoly() # Fits a polynomial to the spline points
splineData.splineIntersecPoints(dmatrix) # Finds the coordinates of each intersection point using the fiducial measurement
splineData.diffCurves() # Differentiates the polynomial for the use of tangent calculations
splineData.midpoints() # Calculates the midpoint of each corresponding intersection point set
splineData.betweenSplines() # Calculates the vector between each corresponding intersection point set
npmidpoints = S1.midpoints

if selected_method == 3:
    # Processing splines data with b_SplineCalculations and SplineProcessingClassM3
    splineDataM3 = SplineProcessingClass(S1, S2, S3, Fiducial, useM3) # Processes the spline sample points
    splineDataM3.fitPoly() # Fits a polynomial to the spline points
    splineDataM3.splineIntersecPoints(dmatrix) # Finds the coordinates of each intersection point using the fiducial measurement
    splineDataM3.midpoints()
    splineData.betweenSplines()

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
from b_Plot import plot_planes
from scipy.optimize import fsolve
import numpy as np

def findIntersectionPoints(coeffX, coeffY, planeCoefficients):
    """
    Is called to find the intersection points of S3 cubic polynomial curve with planes for M1 and M2.

    Parameters:
    coeffX (numpy array): Coefficients of the cubic polynomial for the x-axis.
    coeffY (numpy array): Coefficients of the cubic polynomial for the y-axis.
    planeCoefficients (numpy array): A 2D array where each row represents the coefficients [a, b, c, d] of a plane.

    Returns:
    intersectionPoints (list): A list of lists or arrays, each containing the intersection points (x, y, z) for each plane.
    """
    
    intersectionPoints = []

    # Loop over all the rows of plane coefficients
    for plane in planeCoefficients:
        a, b, c, d = plane  # Extract plane coefficients

        # Define the function to represent the plane equation with the parametric equations substituted
        def planeIntersection(t): #t=z
            # Parametric equations of the curve (x(t), y(t), z(t)) using the fitted coefficients
            x = np.polyval(coeffX, t)
            y = np.polyval(coeffY, t)
            #z = np.polyval(coeffZ, t)

            # Plane equation a*x + b*y + c*z + d = 0
            return a * x + b * y + c * t + d

        # Use fsolve to find the roots of the equation (i.e., solve for z)
        initialGuess = np.mean(S3.zlist) # Initial guess for t. Start by guessing in the middle of the spline (z axis)
        zSolution = fsolve(planeIntersection, initialGuess)

        # Calculate the intersection points (x(t), y(t), z(t)) at the found t values
        planeIntersections = []
        # for z in zSolution:
        x_intersection = np.polyval(coeffX, zSolution)
        y_intersection = np.polyval(coeffY, zSolution)
        z_intersection = zSolution
        
        planeIntersections.append((x_intersection, y_intersection, z_intersection))

        # Append the intersection points for the current plane
        intersectionPoints.append(planeIntersections)

    return intersectionPoints

S3x = np.array(S3.xlist)
S3y = np.array(S3.ylist)
S3z = np.array(S3.zlist) 

S3coeffX = np.polyfit(S3z, S3x, 3)  
S3coeffY = np.polyfit(S3z, S3y, 3)  

S3M1intersections = findIntersectionPoints(S3coeffX, S3coeffY, M1npPlnCoeff)
S3M2intersections = findIntersectionPoints(S3coeffX, S3coeffY, M2npPlnCoeff)
S3M3intersections = splineDataM3.S3.intersec

# Call the plot_planes function with the appropriate parameters

if plot:
    plot_planes(
        plotCommon,
        plotAllS3intersect,
        plotM1,
        plotM2,
        plotM3,
        S1,
        S2,
        S3,
        F1,
        dmatrix,
        bisection,
        M1npPlnCoeff,
        M2npPlnCoeff,
        M3npPlnCoeff,
        CalcM2,
        S3M1intersections,
        S3M2intersections,
        S3M3intersections,
    )
