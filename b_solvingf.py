"""
Description: Function for solving a cubic polynomial

History:
> Created by Robert Phillips 2024-03
"""

'''
https://stackoverflow.com/questions/15008396/is-there-any-numerical-solver-in-python-with-control-of-each-iteration

This file will need to be changed if a different order polynomial is desired to be used
'''

import math
import numpy as np

class Fforpt2:
    @classmethod
    def run_cubic(cls, a, b, c, d, x):
        """
        Solves the cubic equation ax^3 + bx^2 + cx + d = 0.

                Parameters:
        a (float): Coefficient of x^3.
        b (float): Coefficient of x^2.
        c (float): Coefficient of x.
        d (float): Constant term.

        Returns:
        float or None: The real root of the cubic equation. Returns None if the root is complex.
        """
        return a*pow(x,3)+b*pow(x,2)+c*x+d
        
    def __init__(self, coeffx, coeffy, distance, pt1):
        '''specifying what coefficients are, etc'''
        """ coeffx, coeffy - lists of the coefficients for the cubic parametric equation for x in terms of z and y in terms of z,
                assigning these to the coefficients, i.e. ax is coefficient of the first term of the cubic and so on
        """
        # coefficients for x of Z parameterisation
        self.ax = coeffx[0]
        self.bx = coeffx[1]
        self.cx = coeffx[2]
        self.dx = coeffx[3]
        
        # coefficients for Y of Z parameterisation
        self.ay = coeffy[0]
        self.by = coeffy[1]
        self.cy = coeffy[2]
        self.dy = coeffy[3]
        
        self.dis = distance
        self.pt1x = pt1[0] 
        self.pt1y = pt1[1] 
        self.pt1z = pt1[2] 
    
    def __call__(self,z): 
        '''Finding the second point pt2'''
        # minimising dis - pt2
        # dis - sqrt((self.ax*z^3+self.bx*z^2+self.cx*z+self.dx-self.pt1[0])^2+(self.ay*z^3+self.by*z^2+self.cy*z+self.dy-self.pt1[1])^2+(z-self.pt1[3])^2)
        return self.dis - math.sqrt((self.ax*z**3+self.bx*z**2+self.cx*z+self.dx-self.pt1x)**2+(self.ay*z**3+self.by*z**2+self.cy*z+self.dy-self.pt1y)**2+(z-self.pt1z)**2)