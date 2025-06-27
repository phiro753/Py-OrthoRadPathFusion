# script written by Robert Phillips
# Robert Phillips
# 2024-03/04

import numpy as np

class GeometricEquClassConvex:
    
    def __init__(self, S1, S2):
        '''components needed as coefficients for straight tangent line'''
        self.m = []
        self.intersect = []
        self.solution = []
        self.S1xGrad = [] # Deravitives equation of curve 
        self.S1yGrad = [] # Deravitive equation of curve
        self.S2xGrad = [] # Deravitives equation of curve 
        self.S2yGrad = [] # Deravitive equation of curve
        self.avgxGrad = [] # average parametric derivative of curve
        self.avgyGrad = [] # average parametric derivative of curve
        self.TangentInX = [] # What are the X values of the tangent
        self.TangentInY = [] # What are the Y values of the tangent
        self.S1intersec = S1.intersec # "the intersection points on Curve S1 are {S1.intersec} in format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]""
        self.S2intersec = S2.intersec # "the intersection points on Curve S2 are {S2.intersec} in format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]"
       
        
    def tangentLine(self, i, S1, S2):
        '''Computing tangents to splines at intersection points for each plane'''
        # Splitting out the 'one point'
        x0 = self.S1intersec[i][0]
        y0 = self.S1intersec[i][1]
        z0 = self.S1intersec[i][2]
                
        # Gradient at specified point
        self.S1xGrad = S1.Xder(z0) # what is the gradient of S1 polynomial in x, z plane
        self.S1yGrad = S1.Yder(z0) # what is gradient of S1 polynomial in y, z plane
        self.S2xGrad = S2.Xder(z0) # what is the gradient of S2 polynomial in x, z plane
        self.S2yGrad = S2.Yder(z0) # what is gradient of S2 polynomial in y, z plane
        
        # Finding average gradient/differentiation of splines at the intersection points ptA and ptB
        self.avgxGrad = (self.S1xGrad + self.S2xGrad) / 2 # Getting average of derivatives
        self.avgyGrad = (self.S1yGrad + self.S2yGrad) / 2 # Getting average of derivatives

        # Getting tangent lines to parametric equations in XZ and YZ planes
        yintersectX = np.asarray(x0 - self.avgxGrad*z0)
        self.TangentInX = self.avgxGrad*np.asarray([z0 + 1, z0 - 1]) + yintersectX

        yintersectY = np.asarray(y0 - self.avgyGrad*z0)
        self.TangentInY = self.avgyGrad*np.asarray([z0 + 1, z0 - 1]) + yintersectY

        ## Getting cross product to parametric tangents
        # points on X, Z plane
        ptXZ1 = np.array([self.TangentInX[0], y0, z0 + 1])
        ptXZ2 = np.array([self.TangentInX[1], y0, z0 - 1])
        vecXZ = ptXZ1 - ptXZ2 # Subtraction of points gives one vector on tangent plane
        n_vecXZ = vecXZ / np.linalg.norm(vecXZ)
        # points on Y, Z plane
        ptYZ1 = np.array([x0, self.TangentInY[0], z0 + 1])
        ptYZ2 = np.array([x0, self.TangentInY[1], z0 - 1])
        vecYZ = ptYZ1 - ptYZ2
        n_vecYZ = vecYZ / np.linalg.norm(vecYZ) # normalising (dont confuse with normal vector) i.e. making vector 1 unit long

        # print(paraVecYZ)
        ## Computing normal vector from two vectors of plane
        # https://stackoverflow.com/questions/48335279/given-general-3d-plane-equation
        # norm2Spline = np.cross(normalized_vecXZ, normalized_vecYZ)
        # normalised_normSpline = norm2Spline / np.linalg.norm(norm2Spline)

        avgTang2splines = (n_vecXZ + n_vecYZ)/2 # average the parametrised vectors
        n_avgTang2splines = avgTang2splines / np.linalg.norm(avgTang2splines) # normalising 
        # return normalised_normSpline, n_avgTang2splines
        return n_avgTang2splines, ptXZ1, ptXZ2, ptYZ1, ptYZ2
    
    def normalSpline(self, i, Tang2Psplines):
        '''Getting normal to splines for ith planes'''
        
        # Vecctor between pair of intersection points (ptA to ptB)
        ptA = self.S2intersec[i]
        ptB = self.S1intersec[i]
        VecA2B = [ptA - ptB for ptA, ptB in zip(ptA, ptB)]
        n_VecA2B = VecA2B / np.linalg.norm(VecA2B) # normalising 

        # Finding the normals to vector of average tangent and vector between ptA-ptB 
        norm_2spline = np.cross(Tang2Psplines, n_VecA2B)
        # Then normalising this
        n_norm_2spline = norm_2spline / np.linalg.norm(norm_2spline)
        
        # getting midpoint between ptA and ptB
        midpoint = [(ptA + ptB)/2 for ptA, ptB in zip(ptA, ptB)]
        return n_norm_2spline, n_VecA2B, midpoint
    

    def CuttingPlane(self, i, norm_2plane):
        '''Using normal to cutting plane and a known point on the plane to get plane coefficients'''
        # A point on curve 2 which is on the cutting plane -> self.S2intersec[i] {x.y.z}

        # Calculate d
        d = -np.dot(norm_2plane, self.S2intersec[i]) # this uses a point on spline2 but could be spline 1
    
        plane_coeff = np.append(norm_2plane, d)
        
        return plane_coeff
    
