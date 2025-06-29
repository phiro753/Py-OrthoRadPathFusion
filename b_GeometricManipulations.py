"""
Description:  Calculation of plane coefficients in M1 and M2

History:
> Created by Robert Phillips 2024-03
> rewritten by Jaime Uy De Baron 2024-11
"""
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
""" READ ME
    
    THIS FILE:
    # Outputs plane coefficients for plotting/writing to json files for 3Dslicer usage
    
    Methods for cut plane projection:
    # Method 1 (M1): Computes plane orientation using the cross product of two vectors, for convex bisected bone specimens
                     1. The average vector of the tangent to the spline at each intersection point
                     2. The vector between each corresponding (pair of) intersection points
                     
                     On the assumption that cut technicians kept the cut points flat and parallel to the plane of the table

    # Method 2 (M2): Same calculation procedure as M1, but with different vectors, ideally for concave bisected bone specimens
                     1. The vector from the fiducial side end point of the spline to the intersection point that was most recently cut
                     2. The vector between each corresponding (pair of) intersection points

                     On the assumption that for concave bone bisections, the most recent cut will 'sit' on the table flat

    # Method 3 (M3): Same cross-product calculation procedure, but with 3 splines instead of two, the third spline allows the identification of a third point on the plane,
                    which produces two vectors that are known to sit parallel to the cut plane, and therefore eliminates assumptions made on the plane's orientation
                
    # Future development will see a Method 3 (M3) implementation that involves a third spline and the two original ones, to reduce the 'assumptions' made during calculation

    
"""
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Pre-written module import statements
import numpy as np

class GeometricM1Class:
    def __init__(self, S1, S2):
        # Class attributes

        # Tangential vector calculation attributes
        self.m = []
        self.S1xGrad = [] # Derivatives equation of curve 
        self.S1yGrad = [] # Derivatives equation of curve
        self.S2xGrad = [] # Derivatives equation of curve 
        self.S2yGrad = [] # Derivatives equation of curve
        self.avgxGrad = [] # Average parametric derivative of curve
        self.avgyGrad = [] # Average parametric derivative of curve
        self.TangentInX = [] # What are the X values of the tangent
        self.TangentInY = [] # What are the Y values of the tangent
        self.n_avgTang2Splines = []

        # Normal vectors for plane calculation
        self.N2 = []

        # Plane coefficient array
        self.planeCoeffs = []

        # S1, S2 attributes, assigning these removes the need of continuously inputting S1, S2 as function arguments
        self.S1intersec = S1.intersec 
        self.S2intersec = S2.intersec # The intersection points on Curve S1, S2 are {S1.intersec} in format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]
        self.midpoints = S1.midpoints
        self.n_vecA2B = S1.n_vecA2B

    def tangentLine(self, i, S1, S2):
        """ Returns the vector direction for the tangent and points on that tangent
            Actions:
        
        """

        # Separating out the point, in question, on the spline
        x0 = self.S1intersec[i][0]
        y0 = self.S1intersec[i][1]
        z0 = self.S1intersec[i][2]

        # Finding the gradient at the specified point
        self.S1xGrad = S1.Xder(z0) # Gradient of S1 polynomial in x, z plane
        self.S1yGrad = S1.Yder(z0) # Gradient of S1 polynomial in y, z plane
        self.S2xGrad = S2.Xder(z0) # Gradient of S2 polynomial in x, z plane
        self.S2yGrad = S2.Yder(z0) # Gradient of S2 polynomial in y, z plane

        # Finding the average gradient/differentiation of splines at the spline points ptA and ptB
        self.avgxGrad = (self.S1xGrad + self.S2xGrad) / 2
        self.avgyGrad = (self.S1yGrad + self.S2yGrad) / 2

        # Getting tangent lines to parametric equations in XZ and YZ planes
        """ yintersectX, yintersectY - the y intercepts of the tangent line to the spline in XZ and YZ planes
            These are processed into the point-slope formula of a line to calculate the equation of the line, which is stored as multiple points
            z0 +- 1 is to get other points on the line to define it better
        """
        yintersectX = np.asarray(x0 - self.avgxGrad * z0)
        self.TangentInX = self.avgxGrad * np.asarray([z0 + 1, z0 - 1]) + yintersectX

        yintersectY = np.asarray(y0 - self.avgyGrad*z0)
        self.TangentInY = self.avgyGrad*np.asarray([z0 + 1, z0 - 1]) + yintersectY

        # Obtaining the vectors of the tangent average using the above equation and the points given
        # For points on X, Z plane
        ptXZ1 = np.array([self.TangentInX[0], y0, z0 + 1])
        ptXZ2 = np.array([self.TangentInX[1], y0, z0 - 1])
        vecXZ = ptXZ1 - ptXZ2 # Subtraction of points gives one vector on tangent plane
        n_vecXZ = vecXZ / np.linalg.norm(vecXZ)
        # For points on Y, Z plane
        ptYZ1 = np.array([x0, self.TangentInY[0], z0 + 1])
        ptYZ2 = np.array([x0, self.TangentInY[1], z0 - 1])
        vecYZ = ptYZ1 - ptYZ2

        n_vecYZ = vecYZ / np.linalg.norm(vecYZ) # Normalising (dont confuse with normal vector) i.e. making vector length = 1

        avgTang2splines = (n_vecXZ + n_vecYZ)/2 # Average the parametrised vectors
        n_avgTang2splines = avgTang2splines / np.linalg.norm(avgTang2splines) # Normalize the average vector

        self.n_avgTang2Splines.append(n_avgTang2splines)

    def normalSpline(self, i):
        """ Getting normal to splines for ith planes
            Normal 1 (N1): The vector normal to the plane spanned by vecA2B and tang2Splines """
        # Computing normal vector from two vectors of plane
        # https://stackoverflow.com/questions/48335279/given-general-3d-plane-equation
        # Finding the normals to vector of average tangent and vector between ptA-ptB
        norm2Spline = np.cross(self.n_avgTang2Splines[i], self.n_vecA2B[i])
        N1 = norm2Spline / np.linalg.norm(norm2Spline) # Normalizing

        # Finding the normal to the plane spanned by N1 and the vector between two points
        N2 = np.cross(self.n_vecA2B[i], N1)
        N2 = N2 / np.linalg.norm(N2)

        self.N2.append(N2)
        
    def planeCoefficients(self, i):
        """ Using normal to cutting plane and a known point on the plane to get plane coefficients """
        # A point on curve 2 which is on the cutting plane -> self.S2intersec[i] {x.y.z}
        # Calculate the plane constant
        d = -np.dot(self.N2[i], self.S2intersec[i]) # This uses a point on spline 2 but can also use spline 1

        planeCoeff = np.append(self.N2[i], d)

        self.planeCoeffs.append(planeCoeff)

    def geometricTangCalcs(self, S1, S2):
        """ Main function on M1, written like this due to it being written in this style in iteration 1 """
        # For loop calculation
        for i in range(len(self.S1intersec)):
            self.tangentLine(i, S1, S2)
            self.normalSpline(i)
            self.planeCoefficients(i)

        self.planeCoeffs = np.array(self.planeCoeffs)

# Geometric calculations for convex case using method 2
# Written by Jaime Uy De Baron
# Created 2024-11-26

class GeometricM2Class:
    """ The class calculations for method 2, applied to concave structures
        The method uses a vector formed between the the endpoint of the bone where the fiducial is and the furthest spline point outside
        This assumption is based on the geometry of a concave bone always resting on the two 'endpoints' atop a flat surface such as the cut table
    """
    def __init__(self, S1, S2, Fiducial):
        # Class attributes
        
        # Attributes for further calculations
        self.n_vecA2B = S1.n_vecA2B
        self.midpoints = S1.midpoints

        # S1, S2 attributes, assigning these removes the need of continuously inputting S1, S2 as function arguments
        self.S1 = S1
        self.S2 = S2
        self.Fiducial = np.array(Fiducial)
        self.S1intersec = S1.intersec 
        self.S2intersec = S2.intersec # The intersection points on Curve S1, S2 are {S1.intersec} in format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]
        self.midpoints = S1.midpoints 

    def endpoints(self):
        """
        Calculates the position of the endpoints (side of the fiducial)
        """
        point1S1 = np.array([self.S1.xlist[0], self.S1.ylist[0], self.S1.zlist[0]])
        point2S1 = np.array([self.S1.xlist[-1], self.S1.ylist[-1], self.S1.zlist[-1]])

        if abs(np.linalg.norm(point1S1 - self.Fiducial)) < abs(np.linalg.norm(point2S1 - self.Fiducial)):
            self.endPointS1 = point1S1
        else:
            self.endPointS1 = point2S1

        point1S2 = np.array([self.S2.xlist[0], self.S2.ylist[0], self.S2.zlist[0]])
        point2S2 = np.array([self.S2.xlist[-1], self.S2.ylist[-1], self.S2.zlist[-1]])
        if abs(np.linalg.norm(point1S2 - self.Fiducial)) < abs(np.linalg.norm(point2S2 - self.Fiducial)):
            self.endPointS2 = point1S2
        else:
            self.endPointS2 = point2S2

    def calculate_normal_vectors(self):
        """
        Calculate two normal vectors:
        1. N1: Normal to plane formed by endpoint-to-intersection and intersection-to-previous-intersection lines
        2. N2: Normal to plane formed by N1 and vector between corresponding intersection points
        """
        N1_vectors = []
        self.N2_vectors = []

        for i in range(len(self.S1intersec)):
            if i > 0:
                # Vector from endpoint to the previous intersection point on S1
                endpoint_to_prev_inter = ((self.S1intersec[i-1] - self.endPointS1) + (self.S2intersec[i-1] - self.endPointS2)) / 2

                # Vector between the intersection points on S1
                inter2Inter = self.S1intersec[i] - self.S2intersec[i]

                # N1: Normal to the plane formed by these two vectors
                N1 = np.cross(endpoint_to_prev_inter, inter2Inter)
                N1 = N1 / np.linalg.norm(N1)  # Normalize
            else:
                # For the first intersection point, fall back to the original method
                endpoint_to_inter = self.S1intersec[i] - self.endPointS1
                inter_to_inter = self.S2intersec[i] - self.S1intersec[i]
                N1 = np.cross(endpoint_to_inter, inter_to_inter)
                N1 = N1 / np.linalg.norm(N1)

            N1_vectors.append(N1)

            # N2: Normal to plane formed by N1 and inter-intersection vector
            inter_to_inter = self.S2intersec[i] - self.S1intersec[i]
            N2 = np.cross(N1, inter_to_inter)
            N2 = N2 / np.linalg.norm(N2)  # Normalize
            self.N2_vectors.append(N2)
        self.N1 = np.array(N1_vectors)
        self.N2_vectors = np.array(self.N2_vectors)
    
    def CuttingPlane(self):
        ''' Using normal to cutting plane and a known point on the plane to get plane coefficients '''
        # A point on curve 2 which is on the cutting plane -> self.S2intersec[i] {x.y.z}

        planeCoefficients = []
        
        # Iterate through each point in S2intersec and its corresponding normal vector
        for i, point in enumerate(self.midpoints):
            # Get the normal vector for the current point (n_normalToPlane is an array of normal vectors)
            normal_vector = self.N2_vectors[i]

            # Compute the constant term d for this plane using the point and normal vector
            d = -np.dot(normal_vector, point)

            # Combine the normal vector and d to form the plane coefficients [a, b, c, d]
            coefficients = np.append(normal_vector, d)
            planeCoefficients.append(coefficients)

        self.planeCoefficients = np.array(planeCoefficients)

# Geometric calculations for convex case using method 3
# Written by Jaime Uy De Baron
# Created 2024-12/17

class GeometricM3Class:

    def __init__(self, S1, S2, S3):

        # S1, S2, S3 attributes, assigning these removes the need of continuously inputting S1, S2 as function arguments
        self.S1 = S1
        self.S2 = S2
        self.S3 = S3

        self.S1intersec = S1.intersec 
        self.S2intersec = S2.intersec # The intersection points on Curve S1, S2 are {S1.intersec} in format [[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]]
        self.S3intersec = S3.intersec # S3 is the third point on the plane to calculate to on-plane vectors

        self.S1S3vecs = []
        self.S2S3vecs = []

        self.planeCoefficients = []

    def vecCalcs(self):
        """ Calculates the vector between S1 and S3, and the vector between S2 and S3 intersection points """

        S1S3vecs = []
        S2S3vecs = []
        for i in range(len(self.S3intersec)):
            S1S3vector = self.S3intersec[i] - self.S1intersec[i]
            S2S3vector = self.S3intersec[i] - self.S2intersec[i]
            S1S3vecs.append(S1S3vector)
            S2S3vecs.append(S2S3vector)
        self.S1S3vecs = np.array(S1S3vecs)
        self.S2S3vecs = np.array(S2S3vecs)

    def crossProd(self):
        """ Calculates the normal vector to the plane spanned by S1S3 and S2S3 vectors """
        N2 = []
        for i in range(len(self.S1S3vecs)):
            N2vec = np.cross(self.S1S3vecs[i], self.S2S3vecs[i])
            N2.append(N2vec)
        self.normalVectors = np.array(N2)

    def cuttingPlane(self):
        ''' Using normal to cutting plane and a known point on the plane to get plane coefficients '''
        # A point on curve 2 which is on the cutting plane -> self.S2intersec[i] {x.y.z}

        planeCoefficients = []
        
        # Iterate through each point in S2intersec and its corresponding normal vector
        for i, point in enumerate(self.S3intersec):
            # Get the normal vector for the current point (n_normalToPlane is an array of normal vectors)
            normalVector = self.normalVectors[i]

            # Compute the constant term d for this plane using the point and normal vector
            d = -np.dot(normalVector, point)

            # Combine the normal vector and d to form the plane coefficients [a, b, c, d]
            coefficients = np.append(normalVector, d)
            planeCoefficients.append(coefficients)

        self.planeCoefficients = np.array(planeCoefficients)