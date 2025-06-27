# Cutting plane classes
# Robert Phillips
# 2024-03/04

import matplotlib.pyplot as plt
import numpy as np
import b_GuessCoeff3D
import a_readscript


# For funciton solving
from b_solvingf import Fforpt2
# from b_solvingf import simpcubic
from scipy.optimize import fsolve

# Individual functions for calculating geometric maniupations
from b_GeometricManipulations import GeometricEquClassConvex # getting orientation of cutting planes on convex biseciton


class CalcClasses:
    def __init__(self, S1, S2, Fiducial):
        # Class attributes
        self.S1 = S1
        self.S2 = S2
        self.Fiducial = Fiducial

    def FittingPoly(self):
        '''Fitting polynomial'''
        # Paramertising polynomial - with t but t = z
        # https://stackoverflow.com/questions/73069026/finding-an-equation-of-polynom-by-given-point-in-3d-python
        # Setting coefficients as instances of class
        # ---may put this in its own class method in future...?
        self.S1.coeffx = np.polyfit(self.S1.ztup, self.S1.xtup, 3) # Get the coefficients for a parametertised 3rd order polynomial as function Z
        self.S1.coeffy = np.polyfit(self.S1.ztup, self.S1.ytup, 3) # Get the coefficients for a parametertised 3rd order polynomial as function Z
        self.S2.coeffx = np.polyfit(self.S2.ztup, self.S2.xtup, 3) # Get the coefficients for a parametertised 3rd order polynomial as function Z
        self.S2.coeffy = np.polyfit(self.S2.ztup, self.S2.ytup, 3) # Get the coefficients for a parametertised 3rd order polynomial as function Z

    def diffCurves(self):
        ''' DIfferentiating curves - developing'''
        # https://www.geeksforgeeks.org/numpy-polyder-in-python/
        # https://www.khanacademy.org/math/multivariable-calculus/multivariable-derivatives
        self.S1.Xder = np.polyder(self.S1.XfromZequ)
        self.S1.Yder = np.polyder(self.S1.YfromZequ)

    def IntersectionPointConvex(self, dmatrix):
        '''Finding point of intersection on curve using lab measurements...'''
        # ---may want to put in loop or other class later...    
        S1intersec = []
        
        S2intersec = []

        # Identifying which end of the specimen the fiducial marker was placed and which end the splines were started from...
        if abs(self.Fiducial[2] - self.S1.zlist[0]) > abs(self.Fiducial[2] - self.S1.zlist[-1]):
            whichEndS1 = 0 # The start of the spline is furtherest from the fiducial (Spline[0] should be used to start intersection point finding) 
        else:
            whichEndS1 = -1 # The end of the spline is furtherest from the fiducial (Spline[-1] should be used to start intersection point finding) 

       # Getting points of intersection of measurements
        for i in range(len(dmatrix)):
            f1 = Fforpt2(self.S1.coeffx,self.S1.coeffy,dmatrix[i][0],self.Fiducial) # initalising class
            zsol1 = fsolve(f1, self.S1.zlist[whichEndS1]) # the second part of call to fsolve is initial guess... (set as point furtherest away on spline)
            xsol1 = Fforpt2.run_cubic(self.S1.coeffx[0],self.S1.coeffx[1],self.S1.coeffx[2],self.S1.coeffx[3],zsol1) # Running through cubic to find x
            ysol1 = Fforpt2.run_cubic(self.S1.coeffy[0],self.S1.coeffy[1],self.S1.coeffy[2],self.S1.coeffy[3],zsol1) # Running through cubic to find y
            a = [np.array(xsol1)[0], np.array(ysol1)[0], np.array(zsol1)[0]]
            S1intersec.append(a) # adding to a list of ndarrays

            f2 = Fforpt2(self.S2.coeffx,self.S2.coeffy,dmatrix[i][1],self.Fiducial)
            zsol2 = fsolve(f2, self.S2.zlist[whichEndS1]) # the second part of call to fsolve is initial guess... (set as point furtherest away on spline)
            xsol2 = Fforpt2.run_cubic(self.S2.coeffx[0],self.S2.coeffx[1],self.S2.coeffx[2],self.S2.coeffx[3],zsol2) # Running through cubic to find x
            ysol2 = Fforpt2.run_cubic(self.S2.coeffy[0],self.S2.coeffy[1],self.S2.coeffy[2],self.S2.coeffy[3],zsol2) # Running through cubic to find y
            b =[np.array(xsol2)[0], np.array(ysol2)[0], np.array(zsol2)[0]]
            S2intersec.append(b) # adding to a list of ndarrays

        self.S1.intersec = np.array(S1intersec)
        self.S2.intersec = np.array(S2intersec)

        # finding interseciton points from paramertised equations equations in darray type
        self.S1.XfromZequ = np.poly1d(np.polyfit(self.S1.ztup, self.S1.xtup, 3)) # X axis and y axis of parameterisation, and order of desired polynomial
        self.S1.YfromZequ = np.poly1d(np.polyfit(self.S1.ztup, self.S1.ytup, 3)) # X axis and y axis of parameterisation, and order of desired polynomial
        self.S2.XfromZequ = np.poly1d(np.polyfit(self.S2.ztup, self.S2.xtup, 3)) # X axis and y axis of parameterisation, and order of desired polynomial
        self.S2.YfromZequ = np.poly1d(np.polyfit(self.S2.ztup, self.S2.ytup, 3)) # X axis and y axis of parameterisation, and order of desired polynomial

    def geometricTangCalc(self, dmatrix):
        '''Finding values for tangent lines for each intersection point'''
        # Initalising arrays
        Tang2splines = []
        Norm2splines = []
        Norm2cut = []
        VecAB = []
        PlnCoeff = []
        midpoints = [] # finding the points between intersection objects for visualising quiver vectors

        # for i in range(len(dmatrix)):
        geometricEqs = GeometricEquClassConvex(self.S1, self.S2) #initalising tangent class for a Curve
        # ValXTangent, ValYTangent = geometricEqs.tangentLine(S1.intersec[0], S1) # making tangent vector at a point
        for i in range(len(dmatrix)):
            # making tangent vector using average deravitive
            avgTang2spline, ptXZ1, ptXZ2, ptYZ1, ptYZ2 = geometricEqs.tangentLine(i, self.S1, self.S2) 
            # finding normal 
            norm_2spline, VecA2B, midpoint = geometricEqs.normalSpline(i, avgTang2spline)

            '''Calculating the plane plane normal using normal to spline and vector between intersections'''
            norm_2plane = np.cross(norm_2spline, VecA2B) # getting normal to plane
            n_norm_2plane = norm_2plane / np.linalg.norm(norm_2plane) # normalising

            '''Calculating plane using plane normal and a point on the curve'''
            plane_coeff = geometricEqs.CuttingPlane(i, norm_2plane)

            Tang2splines.append(avgTang2spline)
            Norm2splines.append(norm_2spline)
            Norm2cut.append(n_norm_2plane)
            VecAB.append(VecA2B)
            PlnCoeff.append(plane_coeff)
            midpoints.append(midpoint)

        npTang2Splines = np.array(Tang2splines)
        npNorm2splines = np.array(Norm2splines)
        npNorm2Cut = np.array(Norm2cut)
        npvecAB = np.array(VecAB)
        npPlnCoeff = np.array(PlnCoeff)
        npmidpoints = np.array(midpoints)

        return ptXZ1, ptXZ2, ptYZ1, ptYZ2, npTang2Splines, npNorm2splines, npNorm2Cut, npvecAB, npPlnCoeff, npmidpoints

