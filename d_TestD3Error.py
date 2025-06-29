"""
Description: Supporting script to calculate sensitivity of plane calculations

History:
> Written by Jaime Uy De Baron 2024-12
"""

""" READ ME

    THIS FILE:
    # Calculates the error (lab measurements - python calculations) between the specimen slices and the calculated width using Python
"""
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" User debug/modularization interface
    Turn parts of the code on and off for usage (without the need to comment things out)
"""

# printIntersect = False # Make 'False' if want to turn off printing of intersection points
# printEuclideanComparison = False # Make 'False' if want to turn off printing of Euclidean points
printPlanes = False 
printErrorAverage = False # Make 'False' if want to turn off printing of average Euclidean error
printErrorAll = False # Make 'False' if want to turn off printing of all Euclidean error between planes
printAllMeasurements = True # Make 'False' if want to turn off printing of each of raw computed and physical measurements along splines S1,S2,S3 between planes
bladewidth = 0.6 # will need to abstract into inputUI at some point
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Administrative setup """

# Pre-written module import statements
import numpy as np # For array calculations
from Main import F1, M1npPlnCoeff, M2npPlnCoeff, M3npPlnCoeff, splineData, splineDataM3
from scipy.optimize import fsolve

# Written module import statements - this will change quickly
from b_SplineCalculations import SplineClass # For spline processing

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Specimen pull from b_Specimens.py """

from b_Specimens import name, fileS1, fileS2, fileS3, d1, d2, d3, bisection
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Setup """

# Setup the first spline
S1 = SplineClass()
S1.readfunc(fileS1)
S1.convLists2Tuple()

# Setup the second spline
S2 = SplineClass()
'''Have updated and pulled these from where specified in b_SplineCalculations rather than calculating coefficients again'''
S2.readfunc(fileS2)
S2.convLists2Tuple()

# Setup the third spline
'''Have updated and pulled these from where specified in b_SplineCalculations rather than calculating coefficients again'''
S3 = SplineClass()
S3.readfunc(fileS3)
S3.convLists2Tuple()

# Spline 3
'''May be good to keep this here as is only used here'''
S3x = np.array(S3.xlist)
S3y = np.array(S3.ylist)
S3z = np.array(S3.zlist)  
S3coeffX = np.polyfit(S3z, S3x, 3)  
S3coeffY = np.polyfit(S3z, S3y, 3)  
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Main body code """

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


def calcEuclidean(intersectionPoints):
    """ Calculates the Euclidean distance between each consecutive intersection point. """
    
    # Initialize the list to store Euclidean distances
    euclideanDistances = []

    # Loop through the intersection points to calculate the distance between consecutive points
    for i in range(1, len(intersectionPoints)):
        # Convert consecutive intersection points to NumPy arrays
        point1 = np.array(intersectionPoints[i-1])
        point2 = np.array(intersectionPoints[i])
        distance = np.linalg.norm(point1 - point2) - bladewidth # blade width
        euclideanDistances.append(distance)

    return euclideanDistances

# Calculate intersections and then calculate euclidean distances
S1M1intersections = splineData.S1.intersec
S1M2intersections = splineData.S1.intersec
S1M3intersections = splineData.S1.intersec

S1M1euclidean = calcEuclidean(S1M1intersections)
S1M2euclidean = calcEuclidean(S1M2intersections)
S1M3euclidean = calcEuclidean(S1M3intersections)

S2M1intersections = splineData.S2.intersec
S2M2intersections = splineData.S2.intersec
S2M3intersections = splineData.S2.intersec

S2M1euclidean = calcEuclidean(S2M1intersections)
S2M2euclidean = calcEuclidean(S2M2intersections)
S2M3euclidean = calcEuclidean(S2M3intersections)

# # Used for M1, M2 testing
S3M1intersections = findIntersectionPoints(S3coeffX, S3coeffY, M1npPlnCoeff)
S3M2intersections = findIntersectionPoints(S3coeffX, S3coeffY, M2npPlnCoeff)
S3M3intersections = splineDataM3.S3.intersec

S3M1euclidean = calcEuclidean(S3M1intersections)
S3M2euclidean = calcEuclidean(S3M2intersections)
S3M3euclidean = calcEuclidean(S3M3intersections)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

""" Print comparison UI """

S1M1error = (S1M1euclidean - d1)
S2M1error = (S2M1euclidean - d2)
S3M1error = (S3M1euclidean - d3)

S1M2error = (S1M2euclidean - d1)
S2M2error = (S2M2euclidean - d2)
S3M2error = (S3M2euclidean - d3)

S1M3error = (S1M3euclidean - d1)
S2M3error = (S2M3euclidean - d2)
S3M3error = (S3M3euclidean - d3)

if printPlanes:
    print(name)
    planebyplaneM1 = (S1M1error + S2M1error + S3M1error) / 3
    planebyplaneM2 = (S1M2error + S2M2error + S3M2error) / 3
    planebyplaneM3 = (S1M3error + S2M3error + S3M3error) / 3

    print("_" * 50)

    print("\nPlane-by-plane Width Error Comparison: (units in mm)\n")
    
    print(f"{'Plane Index':<15}{'Avg Error M1':<15}{'Avg Error M2':<15}{'Avg Error M3':<15}")
    for i in range(len(planebyplaneM1)):
        print(f"{i+1:<15}{planebyplaneM1[i]:<15.2f}{planebyplaneM2[i]:<15.2f}{planebyplaneM3[i]:<15.2f}")

    print("_" * 50)

    avgM1 = sum(planebyplaneM1) / len(planebyplaneM1)
    avgM2 = sum(planebyplaneM2) / len(planebyplaneM2)
    avgM3 = sum(planebyplaneM3) / len(planebyplaneM3)

    print(f"{'Averages':<15}{avgM1:<15.2f}{avgM2:<15.2f}{avgM3:<15.2f}\n")

# Print the error comparison in a structured format
if printErrorAverage:
    print(name)
    print("\nAverage Error Comparison: (units in mm)")
    print(f"{'Spline':<10}{'M1 Error':<15}{'M2 Error':<15}{'M3 Error':<15}")
    print("-" * 50)

    # Spline 1 Errors
    print(f"S1 {'':<5}{S1M1error.mean():<15.4f}{S1M2error.mean():<15.4f}{S1M3error.mean():<15.4f}")
    
    # Spline 2 Errors
    print(f"S2 {'':<5}{S2M1error.mean():<15.4f}{S2M2error.mean():<15.4f}{S2M3error.mean():<15.4f}")

    # Spline 3 Errors
    print(f"S3 {'':<5}{S3M1error.mean():<15.4f}{S3M2error.mean():<15.4f}{S3M3error.mean():<15.4f}")
    print(" ")

    # print("-" * 50)
    # print(f"{'Avg Error':<10}{np.mean(S1M1error):<15.4f}{np.mean(S1M2error):<15.4f}{np.mean(S1M3error):<15.4f}")

if printErrorAll:
    print(name)
    print(f"\nAll Error Comparison: (units in mm) ({bisection} bisection)")
    print(f"{'Spline':<8}{'Index':<7}{'M1 Error':<15}{'M2 Error':<15}{'M3 Error':<15}")
    print("-" * 50)

    # Loop through all the errors and print each index's error for all splines
    for i in range(len(S1M1error)):
        print(f"S1 {'':<5}{i:<7}: {S1M1error[i]:<15.4f}: {S1M2error[i]:<15.4f}: {S1M3error[i]:<15.4f}")
    
    # print("-" * 50)

    for i in range(len(S2M1error)):
        print(f"S2 {'':<5}{i:<7}: {(S2M1error[i]):<15.4f}: {(S2M2error[i]):<15.4f}: {(S2M3error[i]):<15.4f}")

    # print("-" * 50)

    for i in range(len(S3M1error)):
        print(f"S3 {'':<5}{i:<7}: {(S3M1error[i]):<15.4f}: {(S3M2error[i]):<15.4f}: {(S3M3error[i]):<15.4f}")
    
    print(" ")


if printAllMeasurements:
    print(f"\nIndividual Measurements: (units in mm) ({name})")
    # S1M1euclidean
    print(f"{'Spline':<8}{'Index':<7}{'M1 Measure':<15}{'M2 Measure':<15}{'M3 Measure':<15}")
    print("-" * 50)
    
    print("Computed measurements")
    # Loop through all the errors and print each index's error for all splines
    for i in range(len(S1M1euclidean)):
        print(f"S1 {'':<5}{i:<7}: {S1M1euclidean[i]:<15.4f}: {S1M2euclidean[i]:<15.4f}: {S1M3euclidean[i]:<15.4f}")
    for i in range(len(S2M1euclidean)):
        print(f"S2 {'':<5}{i:<7}: {S2M1euclidean[i]:<15.4f}: {S2M2euclidean[i]:<15.4f}: {S2M3euclidean[i]:<15.4f}")
    for i in range(len(S3M1euclidean)):
        print(f"S3 {'':<5}{i:<7}: {S3M1euclidean[i]:<15.4f}: {S3M2euclidean[i]:<15.4f}: {S3M3euclidean[i]:<15.4f}")
    
    print("-" * 50)
    
    print("Physical measurements")
    for i in range(len(d1)):
        print(f"d1 {'':<5}{i:<7}: {d1[i]:<15.4f}: {d1[i]:<15.4f}: {d1[i]:<15.4f}")
    for i in range(len(d2)):
        print(f"d2 {'':<5}{i:<7}: {d2[i]:<15.4f}: {d2[i]:<15.4f}: {d2[i]:<15.4f}")
    for i in range(len(d3)):
        print(f"d3 {'':<5}{i:<7}: {d3[i]:<15.4f}: {d3[i]:<15.4f}: {d3[i]:<15.4f}")
    
    print(" ")