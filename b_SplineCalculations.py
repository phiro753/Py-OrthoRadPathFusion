"""
Description: Calculation on splines

History:
> Created by Robert Phillips 2024-04
> Rewritten by Jaime Uy De Baron 2024-11
""" 

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
""" READ ME
    
    THIS FILE:
    # Processes the imported spline

"""
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Pre-written module import statements
import numpy as np

# Written module import statements - this will change quickly
import a_readscript
from b_solvingf import Fforpt2 # For function solving
from scipy.optimize import fsolve # Finds the roots of a system of non-linear equations

# Individual functions for calculating geometric maniupations - this should not be here
# from b_GeometricManipulations import GeometricEquClassConvex # Getting orientation of cutting planes on convex biseciton

class SplineClass:
    """ Actions:
        1. Stores spline and fiducial points into lists
        2. Converts these lists to tuples
    """
    def __init__(self):
        # Class attributes

        # Creating lists for spline sample points from json files
        self.xlist = []
        self.ylist = []
        self.zlist = []

        # Conversion of lists to list of tuples
        self.xtup = ()
        self.ytup = ()
        self.ztup = ()

        # Derivatives
        self.Xder = np.poly1d([])
        self.Yder = np.poly1d([])

    def readfunc(self, filename):
        """ Getting control points from JSON files - using seraliser """
        for f in a_readscript.extract_control_point_positions(filename):
            # Need to change list in list to tupples in list
            # S1.tuplelist.append((f[0],f[1],f[2]))
            self.xlist.append(f[0])
            self.ylist.append(f[1])
            self.zlist.append(f[2])
    
    def convLists2Tuple(self):
        """ Need to convert control points that define markups to tuples """
        self.xtup = tuple(self.xlist)
        self.ytup = tuple(self.ylist)
        self.ztup = tuple(self.zlist)

class SplineProcessingClass:
    """ Actions:
        1. Fits a 3rd order (cubic) polynomial to the points given by S1 and S2 files
        2. Differentiates these cubic functions for S1 and S2
        3. Iteratively obtains the coordinates/points on the spline using Newton-Raphson and the Euclidean matrix in dmatrix 
        4. Obtains the coordinates(?) for the tangent to the point at the chosen/solved for spline points


    """   
    def __init__(self, S1, S2, S3, Fiducial, useM3):
        # Class attributes
        if useM3:
            self.useM3 = True
        else:
            self.useM3 = False
        # Spline and fiducial attributes
        self.S1 = S1 
        self.S2 = S2 # Spline 1 and Spline 2 being classed as attributes
        if self.useM3:
            self.S3 = S3
        self.Fiducial = Fiducial # Fiducial marker stored for processing

        # Essential data for calculations
        self.S1.intersec = [] 
        self.S2.intersec = [] 
        if self.useM3:
            self.S3.intersec = [] # Intersection points (cut points) for each spline
        self.S1.midpoints = [] # Midpoints will just be stored in spline 1's data
        self.S1.n_VecA2B = [] # Intersection vectors will just be stored in spline 1's data

    def fitPoly(self):
        """ Fitting a third order polynomial to the points given by the json file """
        # Parametrising polynomial - with t but t = z
        # https://stackoverflow.com/questions/73069026/finding-an-equation-of-polynom-by-given-point-in-3d-python
        # Setting coefficients as instances of class
        # Future development might see this in its own class
        self.S1.coeffx = np.polyfit(self.S1.ztup, self.S1.xtup, 3) # Get the coefficients for a parametertised 3rd order polynomial as function Z
        self.S1.coeffy = np.polyfit(self.S1.ztup, self.S1.ytup, 3) # Get the coefficients for a parametertised 3rd order polynomial as function Z
        self.S2.coeffx = np.polyfit(self.S2.ztup, self.S2.xtup, 3) # Get the coefficients for a parametertised 3rd order polynomial as function Z
        self.S2.coeffy = np.polyfit(self.S2.ztup, self.S2.ytup, 3) # Get the coefficients for a parametertised 3rd order polynomial as function Z
        # For M3
        if self.useM3:
            self.S3.coeffx = np.polyfit(self.S3.ztup, self.S3.xtup, 3) # Get the coefficients for a parametertised 3rd order polynomial as function Z
            self.S3.coeffy = np.polyfit(self.S3.ztup, self.S3.ytup, 3) # Get the coefficients for a parametertised 3rd order polynomial as function Z

    def diffCurves(self):
        """ Differentiating curves """
        # https://www.geeksforgeeks.org/numpy-polyder-in-python/
        # https://www.khanacademy.org/math/multivariable-calculus/multivariable-derivatives
        self.S1.Xder = np.polyder(self.S1.XfromZequ)
        self.S1.Yder = np.polyder(self.S1.YfromZequ)

    def splineIntersecPoints(self, dmatrix):
        """ Finding point of intersection on curve using lab measurements
            Done using the Newton-Raphson method of iteratively obtaining the length between fiducial and spline point 
        """   
        S1intersec = []
        S2intersec = []
        # For M3
        S3intersec = []

        # Identifying z end of the specimen the fiducial marker was placed and which end the splines were started from...
        # S1Identifying z end of the specimen the fiducial marker was placed and which end the splines were started from...
        if abs(self.Fiducial[2] - self.S1.zlist[0]) > abs(self.Fiducial[2] - self.S1.zlist[-1]):
            # The start of the spline is furtherest from the fiducial (Spline[0] should be used to start intersection point finding) 
            self.S1.furtherstEnd = np.array([self.S1.xlist[0], self.S1.ylist[0], self.S1.zlist[0]])
        else:
            # The end of the spline is furtherest from the fiducial (Spline[-1] should be used to start intersection point finding) 
            self.S1.furtherstEnd = np.array([self.S1.xlist[-1], self.S1.ylist[-1], self.S1.zlist[-1]])
        
        # S2Identifying z end of the specimen the fiducial marker was placed and which end the splines were started from...
        if abs(self.Fiducial[2] - self.S2.zlist[0]) > abs(self.Fiducial[2] - self.S2.zlist[-1]):
            # The start of the spline is furtherest from the fiducial (Spline[0] should be used to start intersection point finding) 
            self.S2.furtherstEnd = np.array([self.S2.xlist[0], self.S2.ylist[0], self.S2.zlist[0]])
        else:
            # The end of the spline is furtherest from the fiducial (Spline[-1] should be used to start intersection point finding) 
            self.S2.furtherstEnd = np.array([self.S2.xlist[-1], self.S2.ylist[-1], self.S2.zlist[-1]])
        
        if self.useM3:
            # S3Identifying z end of the specimen the fiducial marker was placed and which end the splines were started from...
            if abs(self.Fiducial[2] - self.S3.zlist[0]) > abs(self.Fiducial[2] - self.S3.zlist[-1]):
                # The start of the spline is furtherest from the fiducial (Spline[0] should be used to start intersection point finding) 
                self.S3.furtherstEnd = np.array([self.S3.xlist[0], self.S3.ylist[0], self.S3.zlist[0]])
            else:
                # The end of the spline is furtherest from the fiducial (Spline[-1] should be used to start intersection point finding) 
                self.S3.furtherstEnd = np.array([self.S3.xlist[-1], self.S3.ylist[-1], self.S3.zlist[-1]])
        
        # Getting points of intersection of measurements
        """ Finding the coordinates of each spline point chosen using the Eculidean measurement 
            Actions:
            1. Initialize the function of spline 1 f1 using the Fforpt2 class defined in b_solfingf.py
            2. zsol1 is the coordinate of the z point, fsolve is a function from SciPy that finds this point based on Eculidean distances
            3. Once zsol1 is known, we can find xsol1 and ysol1 because they are in terms of z
            4. Then add it to the list defined above
        """
        for i in range(len(dmatrix)):
            # Initialize class for S1
            f1 = Fforpt2(self.S1.coeffx, self.S1.coeffy, dmatrix[i][0], self.Fiducial)

            # Calculate the z roots of f1
            zsol1 = fsolve(f1, self.S1.furtherstEnd[2])  # Initial guess: farthest point on spline

            # Find x and y coordinates that correspond to the z coordinate above
            xsol1 = Fforpt2.run_cubic(self.S1.coeffx[0], self.S1.coeffx[1], self.S1.coeffx[2], self.S1.coeffx[3], zsol1)
            ysol1 = Fforpt2.run_cubic(self.S1.coeffy[0], self.S1.coeffy[1], self.S1.coeffy[2], self.S1.coeffy[3], zsol1)

            # Create an array and append that to S1 intersec
            a = [np.array(xsol1)[0], np.array(ysol1)[0], np.array(zsol1)[0]]
            S1intersec.append(a)  # Add to list of intersections for S1

            # Process for S2 is the same as S1
            f2 = Fforpt2(self.S2.coeffx, self.S2.coeffy, dmatrix[i][1], self.Fiducial)

            zsol2 = fsolve(f2, self.S2.furtherstEnd[2])  # Initial guess: farthest point on spline

            xsol2 = Fforpt2.run_cubic(self.S2.coeffx[0], self.S2.coeffx[1], self.S2.coeffx[2], self.S2.coeffx[3], zsol2)
            ysol2 = Fforpt2.run_cubic(self.S2.coeffy[0], self.S2.coeffy[1], self.S2.coeffy[2], self.S2.coeffy[3], zsol2)

            b = [np.array(xsol2)[0], np.array(ysol2)[0], np.array(zsol2)[0]]
            S2intersec.append(b)

            if self.useM3:
                # For M3
                # Process for S3 is the same as S1
                f3 = Fforpt2(self.S3.coeffx, self.S3.coeffy, dmatrix[i][2], self.Fiducial)

                zsol3 = fsolve(f3, self.S3.furtherstEnd[2])  # Initial guess: farthest point on spline
    
                xsol3 = Fforpt2.run_cubic(self.S3.coeffx[0], self.S3.coeffx[1], self.S3.coeffx[2], self.S3.coeffx[3], zsol3)
                ysol3 = Fforpt2.run_cubic(self.S3.coeffy[0], self.S3.coeffy[1], self.S3.coeffy[2], self.S3.coeffy[3], zsol3)

                c = [np.array(xsol3)[0], np.array(ysol3)[0], np.array(zsol3)[0]]
                S3intersec.append(c)

        # Store intersection points in S1 and S2 class
        self.S1.intersec = np.array(S1intersec)
        self.S2.intersec = np.array(S2intersec)
        if self.useM3:
            # For M3
            self.S3.intersec = np.array(S3intersec)

        # Finding intersection points from parametrised equations in data array type
        """ GPT suggests that this code block creates a polynomial from the coefficients returned by the polyfit function,
            not sure what that means effectively but ok! 
        """
        self.S1.XfromZequ = np.poly1d(np.polyfit(self.S1.ztup, self.S1.xtup, 3)) # X axis and y axis of parameterisation, and order of desired polynomial
        self.S1.YfromZequ = np.poly1d(np.polyfit(self.S1.ztup, self.S1.ytup, 3)) # X axis and y axis of parameterisation, and order of desired polynomial
        self.S2.XfromZequ = np.poly1d(np.polyfit(self.S2.ztup, self.S2.xtup, 3)) # X axis and y axis of parameterisation, and order of desired polynomial
        self.S2.YfromZequ = np.poly1d(np.polyfit(self.S2.ztup, self.S2.ytup, 3)) # X axis and y axis of parameterisation, and order of desired polynomial
        if self.useM3:
            self.S3.XfromZequ = np.poly1d(np.polyfit(self.S3.ztup, self.S3.xtup, 3)) # X axis and y axis of parameterisation, and order of desired polynomial
            self.S3.YfromZequ = np.poly1d(np.polyfit(self.S3.ztup, self.S3.ytup, 3)) # X axis and y axis of parameterisation, and order of desired polynomial

    def midpoints(self):
        """ Finds the midpoints between each intersection point """
        # Performing midpoint average calculation
        midpoints = (self.S1.intersec + self.S2.intersec) / 2
        self.S1.midpoints = np.array(midpoints)

    def betweenSplines(self):
        """ Getting the vector between two spline points """
        # Assigning a list
        vecA2B = []

        # Calculating the vectors between corresponding intersection points
        for i in range(len(self.S1.intersec)):
            ptA = self.S2.intersec[i]
            ptB = self.S1.intersec[i]
            vecA2B.append([ptA - ptB for ptA, ptB in zip(ptA, ptB)])
        
        self.S1.n_vecA2B = vecA2B / np.linalg.norm(vecA2B) # Normalizing