# 'Guessing' coefficients of polynomial splines by fitting cubic to spline control points
# Robert Phillips
# 2024-03/04


# https://stackoverflow.com/questions/45350891/fitting-a-polynomial-using-np-polyfit-in-3-dimensions

# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.linear_model import LinearRegression
import numpy as np


def CubciCoeff(tTest, varTest):
    # 'Guessing coefficients' with numpy.polynomial.poly
    # This function can do higher order polynomials but thrid order has been chosen as bisection with bandsaw is rather coarse. The width of bandsaw blade will affect how sharp biseciton cuts can be (and how high a polynomial needs to be used)... testing needed
    PolyOrder = 3
    z = np.polynomial.Polynomial.fit(tTest, varTest, PolyOrder)
    c = z.convert().coef
    return c  # coefficient in form [etc,d,c,b,a for defining cubic polynomial]