""" 
Description: Python file that holds sample specimen information for code testing 

History: 
> Created by Jaime Uy De Baron 2024-12
"""

"""
In each pre-made entry:
    Offset = is for incouperating microtomb thickness of tissue from cut-face to get to where
        histolgoy should be co-registered to. It has been set to 0 nm for b_Specimens
    Sign = is the cirection of these offsets 
    dmatrix = is a nx2 matrix (list of lists) containing the euclidean measurement
        of the spline point and the fiducial
    fileS1 = contains the coordinates for the spline 1, we operate on this to produce a 3rd order
        polynomial that's meant to fit this, fileS2 is the exact same thing 
"""
import numpy as np

""" Specimens for manual data input, see README for usage details"""

""" Building/development data from previous work - R. Phillips (2025) publicaiton
    - Note the two Build specimens miss the 3rd laboratory measurement in the dmatrix
    so can only be run through M1 and M2. 
    - Main.py

"""
# # Specimen Build Lateral bisection
# name = "SpecimenBuild Lateral"
# dmatrix = [[148.9,152.4],
#            [135.0,137.1],
#            [119.3,124.3],
#            [99.12,105.3],
#            [85.45,80.25],
#            [69.94,69.31],
#            [53.66,54.12],
#            [30.92,32.67],
#            [20.87,22.99]]
# offsets = [910,1970,1265,0,0,0,0,0,0]  # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = -1 # should the offsets numbers be subtracted (shifted back towards fid_ref) dissection blockface or added to? (subtracted from in this testcase... it depends on which side of dissection sections were processed in histology)
# fileS1 = "DataStorage2/Specimen_Build/SplineLat_ma.json" # Vet Tumour specimen 06
# fileS2 = "DataStorage2/Specimen_Build/SplineLat_mb.json" # Vet Tumour specimen 06
# fileS3 = "DataStorage2/Specimen_Build/SplineLatVal_mc.json" # FOR VALIDATION
# fileF1 = "DataStorage2/Specimen_Build/F_Lat.json" # Vet Tumour specimen 06
# bisection = "L"
# d1 = np.array([15, 14.23, 15.88, 14.26, 13.56, 15.93, 22.78, 10.37]) # Data for d1, d2, and d3
# d2 = np.array([14.76, 14.35, 15.72, 16.61, 12.07, 15.6, 21.82, 10.2])
# d3 = np.array([16.73, 15.05, 16.3, 20.96, 11.35, 15.31, 21.3, 10.6])


# # For Specimen Build Medial bisection
# name = "SpecimenBuild Medial"
# dmatrix = [[150.8,160.0],
#            [135.8,142.5],
#            [117.8,121.8],
#            [99.11,96.57],
#            [79.43,78.39],
#            [51.21,53.84],
#            [44.93,44.75]]
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage2/Specimen_Build/SplineMed_ma.json" # Vet Tumour specimen 06
# fileS2 = "DataStorage2/Specimen_Build/SplineMed_mb.json"
# fileS3 = "DataStorage2/Specimen_Build/SplineMedVal_mc.json" # Vet Tumour specimen 06
# fileF1 = "DataStorage2/Specimen_Build/F_Med.json" 
# bisection = "M"
# d1 = np.array([15.26, 19.34, 18.46, 19.59, 24.7, 13.99]) # Data for d1, d2, and d3
# d2 = np.array([15.05, 20.78, 21.89, 19.93, 26.26, 12.41])
# d3 = np.array([12.91, 21.19, 22.59, 20.99, 28.04, 9.9])


'''Testing data that was collected for J. Uy De Baron (2025) publication'''
# # For Specimen 01 Anterior bisection
# name = "Specimen01 Anterior"
# dmatrix = np.array([
#     [137.94, 145.39, 141.13],
#     [118.6, 125.51, 121.51],
#     [95.15, 104.76, 100.81],
#     [72.55, 76.44, 73.7],
#     [49.05, 50.5, 49.38],
#     [26.62, 27.92, 26.5]
# ])
# offsets = np.zeros(len(dmatrix)) #  # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Specimen_01/SplineAnt_ma.json"
# fileS2 = "DataStorage/Specimen_01/SplineAnt_mb.json"
# fileS3 = "DataStorage/Specimen_01/SplineAnt_mc.json"
# fileF1 = "DataStorage/Specimen_01/F_Ant.json"
# bisection = "A"
# d1 = np.array([18.59, 21.19, 24.84, 25.14, 22.38])
# d2 = np.array([19.84, 23.58, 25.58, 27.36, 22.12])
# d3 = np.array([18.2, 20.6, 27.86, 24.17, 21.41])

# For Specimen 02 Anterior Bisection
name = "Specimen02 Anterior"
dmatrix = np.array([
    [94.19, 98.4, 96.74],
    [70.66, 75.18, 72.06],
    [49.76, 53.39, 51.23],
    [23.08, 27.82, 23.96]
])
offsets = np.zeros(len(dmatrix))  # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
sign = 1
fileS1 = "DataStorage/Specimen_02/SplineAnt_ma.json"
fileS2 = "DataStorage/Specimen_02/SplineAnt_mb.json"
fileS3 = "DataStorage/Specimen_02/SplineAnt_mc.json"
fileF1 = "DataStorage/Specimen_02/F_Ant.json"
bisection = "A"
d1 = np.array([22.03, 20.96, 25.75])
d2 = np.array([23.6, 22.66, 26.18])
d3 = np.array([25.09, 21.31, 26.09])


# # For Specimen 02 Posterior Bisection
# name = "Specimen02 Posterior"
# dmatrix = np.array([
#     [108.06, 118.79, 106.07],
#     [97.62, 104.06, 99.13],
#     [89.25, 95.04, 90.14],
#     [81.04, 85.78, 83.06],
#     [72.54, 75.97, 74.19],
#     [65.65, 66.82, 65.55],
#     [58.57, 60.76, 58.2],
#     [50.55, 53.07, 50.01],
#     [42.81, 43.61, 41.81],
#     [31.95, 33.37, 31.32],
#     [21.57, 23.12, 21.07]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Specimen_02/SplinePost_ma.json"
# fileS2 = "DataStorage/Specimen_02/SplinePost_mb.json"
# fileS3 = "DataStorage/Specimen_02/SplinePost_mc.json"
# fileF1 = "DataStorage/Specimen_02/F_Post.json"
# bisection = "P"
# d1 = np.array([12.47, 9.48, 7.42, 8.16, 6.3, 7.49, 7.6, 6.98, 10.36, 9.63])
# d2 = np.array([18.55, 10.01, 9.88, 8.64, 8.83, 6.18, 7.22, 8.98, 9.49, 10.1])
# d3 = np.array([12.52, 10.15, 7.7, 8.71, 7.91, 6.38, 7.42, 7.54, 9.76, 9.83])

# # For Specimen 03 Anterior Bisection
# name = "Specimen03 Anterior"
# dmatrix = np.array([
#     [101.28, 119.29, 114.00],
#     [98.25, 106.58, 102.03],
#     [83.18, 89.78, 87.21],
#     [66.84, 72.37, 69.21],
#     [53.33, 54.72, 53.96],
#     [37.74, 39.27, 38.47],
#     [17.7, 17.1, 14.54]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Specimen_03/SplineAnt_ma.json"
# fileS2 = "DataStorage/Specimen_03/SplineAnt_mb.json"
# fileS3 = "DataStorage/Specimen_03/SplineAnt_mc.json"
# fileF1 = "DataStorage/Specimen_03/F_Ant.json"
# bisection = "A"
# d1 = np.array([2.48, 15.5, 16.32, 14.94, 16.05, 22.09])
# d2 = np.array([12.35, 17.08, 17.68, 12.89, 15.17, 23.66])
# d3 = np.array([11.86, 14.06, 16.21, 14.37, 15.33, 22.66])


# # For Specimen 03 Posterior Bisection
# name = "Specimen03 Posterior"
# dmatrix = np.array([
#     [110.74, 105.06, 105.43],
#     [99.49, 97.56, 96.9],
#     [80.17, 80.94, 79.74],
#     [62.13, 65.68, 62.2],
#     [46.67, 46.23, 44.74],
#     [30.79, 30.46, 29.42]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Specimen_03/SplinePost_ma.json"
# fileS2 = "DataStorage/Specimen_03/SplinePost_mb.json"
# fileS3 = "DataStorage/Specimen_03/SplinePost_mc.json"
# fileF1 = "DataStorage/Specimen_03/F_Post.json"
# bisection = "P"
# d1 = np.array([13.91, 19.55, 19.15, 14.94, 15.05])
# d2 = np.array([8.73, 18.36, 16.08, 19.62, 15.2])
# d3 = np.array([7.97, 18.1, 15.69, 16.93, 14.78])


# # For Specimen 04 Anterior Bisection
# name = "Specimen04 Anterior"
# dmatrix = np.array([
#     [99.85, 101.45, 98.03],
#     [86.48, 87.14, 83.77],
#     [68.38, 68.35, 65.32],
#     [57.69, 57.24, 54.56],
#     [49.7, 48.41, 46.97],
#     [36.27, 35.58, 29.17],
#     [23.14, 19.61, 12.44]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Specimen_04/SplineAnt_ma.json"
# fileS2 = "DataStorage/Specimen_04/SplineAnt_mb.json"
# fileS3 = "DataStorage/Specimen_04/SplineAnt_mc.json"
# fileF1 = "DataStorage/Specimen_04/F_Ant.json"
# bisection = "A"
# d1 = np.array([13.78, 17.36, 9.89, 8.93, 13.3, 15.34])
# d2 = np.array([13.75, 18.18, 11.02, 8.4, 14.1, 16.65])
# d3 = np.array([13.94, 17.23, 9.14, 8.68, 15.17, 16.32])

# # For Specimen 04 Posterior Bisection
# name = "Specimen04 Posterior"
# dmatrix = np.array([
#     [94.86, 90.37, 89.09],
#     [70.14, 69.48, 68.86],
#     [43.48, 41.95, 41.73],
#     [27.32, 22.85, 21.04]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Specimen_04/SplinePost_ma.json"
# fileS2 = "DataStorage/Specimen_04/SplinePost_mb.json"
# fileS3 = "DataStorage/Specimen_04/SplinePost_mc.json"
# fileF1 = "DataStorage/Specimen_04/F_Post.json"
# bisection = "P"
# d1 = np.array([24.17, 26.3, 23.09])
# d2 = np.array([25.37, 26.31, 21.54])
# d3 = np.array([24.09, 26.51, 21.54])




'''Sensitivity testing
1st set sensitivity splines
'''
# # For Specimen 01 Anterior bisection
# name = "Specimen01 Anterior"
# dmatrix = np.array([
#     [137.94, 145.39, 141.13],
#     [118.6, 125.51, 121.51],
#     [95.15, 104.76, 100.81],
#     [72.55, 76.44, 73.7],
#     [49.05, 50.5, 49.38],
#     [26.62, 27.92, 26.5]
# ])
# offsets = np.zeros(len(dmatrix)) #  # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_01/SplineSensAnt_ma.json"
# fileS2 = "DataStorage/Sensitivity_01/SplineSensAnt_mb.json"
# fileS3 = "DataStorage/Sensitivity_01/SplineSensAnt_mc.json"
# fileF1 = "DataStorage/Sensitivity_01/F_Ant.json"
# bisection = "A"
# d1 = np.array([18.59, 21.19, 24.84, 25.14, 22.38])
# d2 = np.array([19.84, 23.58, 25.58, 27.36, 22.12])
# d3 = np.array([18.2, 20.6, 27.86, 24.17, 21.41])

# # For Specimen 02 Anterior Bisection
# name = "Specimen02 Anterior"
# dmatrix = np.array([
#     [94.19, 98.4, 96.74],
#     [70.66, 75.18, 72.06],
#     [49.76, 53.39, 51.23],
#     [23.08, 27.82, 23.96]
# ])
# offsets = np.zeros(len(dmatrix))  # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_02/SplineSensAnt_ma.json"
# fileS2 = "DataStorage/Sensitivity_02/SplineSensAnt_mb.json"
# fileS3 = "DataStorage/Sensitivity_02/SplineSensAnt_mc.json"
# fileF1 = "DataStorage/Sensitivity_02/F_Ant.json"
# bisection = "A"
# d1 = np.array([22.03, 20.96, 25.75])
# d2 = np.array([23.6, 22.66, 26.18])
# d3 = np.array([25.09, 21.31, 26.09])


# # For Specimen 02 Posterior Bisection
# name = "Specimen02 Posterior"
# dmatrix = np.array([
#     [108.06, 118.79, 106.07],
#     [97.62, 104.06, 99.13],
#     [89.25, 95.04, 90.14],
#     [81.04, 85.78, 83.06],
#     [72.54, 75.97, 74.19],
#     [65.65, 66.82, 65.55],
#     [58.57, 60.76, 58.2],
#     [50.55, 53.07, 50.01],
#     [42.81, 43.61, 41.81],
#     [31.95, 33.37, 31.32],
#     [21.57, 23.12, 21.07]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_02/SplineSensPost_ma.json"
# fileS2 = "DataStorage/Sensitivity_02/SplineSensPost_mb.json"
# fileS3 = "DataStorage/Sensitivity_02/SplineSensPost_mc.json"
# fileF1 = "DataStorage/Sensitivity_02/F_Post.json"
# bisection = "P"
# d1 = np.array([12.47, 9.48, 7.42, 8.16, 6.3, 7.49, 7.6, 6.98, 10.36, 9.63])
# d2 = np.array([18.55, 10.01, 9.88, 8.64, 8.83, 6.18, 7.22, 8.98, 9.49, 10.1])
# d3 = np.array([12.52, 10.15, 7.7, 8.71, 7.91, 6.38, 7.42, 7.54, 9.76, 9.83])

# # For Specimen 03 Anterior Bisection
# name = "Specimen03 Anterior"
# dmatrix = np.array([
#     [101.28, 119.29, 114.00],
#     [98.25, 106.58, 102.03],
#     [83.18, 89.78, 87.21],
#     [66.84, 72.37, 69.21],
#     [53.33, 54.72, 53.96],
#     [37.74, 39.27, 38.47],
#     [17.7, 17.1, 14.54]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_03/SplineSensAnt_ma.json"
# fileS2 = "DataStorage/Sensitivity_03/SplineSensAnt_mb.json"
# fileS3 = "DataStorage/Sensitivity_03/SplineSensAnt_mc.json"
# fileF1 = "DataStorage/Sensitivity_03/F_Ant.json"
# bisection = "A"
# d1 = np.array([2.48, 15.5, 16.32, 14.94, 16.05, 22.09])
# d2 = np.array([12.35, 17.08, 17.68, 12.89, 15.17, 23.66])
# d3 = np.array([11.86, 14.06, 16.21, 14.37, 15.33, 22.66])


# # For Specimen 03 Posterior Bisection
# name = "Specimen03 Posterior"
# dmatrix = np.array([
#     [110.74, 105.06, 105.43],
#     [99.49, 97.56, 96.9],
#     [80.17, 80.94, 79.74],
#     [62.13, 65.68, 62.2],
#     [46.67, 46.23, 44.74],
#     [30.79, 30.46, 29.42]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_03/SplineSensPost_ma_2.json"
# fileS2 = "DataStorage/Sensitivity_03/SplineSensPost_mb_2.json"
# fileS3 = "DataStorage/Sensitivity_03/SplineSensPost_mc_2.json"
# fileF1 = "DataStorage/Sensitivity_03/F_Post.json"
# bisection = "P"
# d1 = np.array([13.91, 19.55, 19.15, 14.94, 15.05])
# d2 = np.array([8.73, 18.36, 16.08, 19.62, 15.2])
# d3 = np.array([7.97, 18.1, 15.69, 16.93, 14.78])


# # For Specimen 04 Anterior Bisection
# name = "Specimen04 Anterior"
# dmatrix = np.array([
#     [99.85, 101.45, 98.03],
#     [86.48, 87.14, 83.77],
#     [68.38, 68.35, 65.32],
#     [57.69, 57.24, 54.56],
#     [49.7, 48.41, 46.97],
#     [36.27, 35.58, 29.17],
#     [23.14, 19.61, 12.44]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_04/SplineSensAnt_ma.json"
# fileS2 = "DataStorage/Sensitivity_04/SplineSensAnt_mb.json"
# fileS3 = "DataStorage/Sensitivity_04/SplineSensAnt_mc.json"
# fileF1 = "DataStorage/Sensitivity_04/F_Ant.json"
# bisection = "A"
# d1 = np.array([13.78, 17.36, 9.89, 8.93, 13.3, 15.34])
# d2 = np.array([13.75, 18.18, 11.02, 8.4, 14.1, 16.65])
# d3 = np.array([13.94, 17.23, 9.14, 8.68, 15.17, 16.32])

# # For Specimen 04 Posterior Bisection
# name = "Specimen04 Posterior"
# dmatrix = np.array([
#     [94.86, 90.37, 89.09],
#     [70.14, 69.48, 68.86],
#     [43.48, 41.95, 41.73],
#     [27.32, 22.85, 21.04]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_04/SplineSensPost_ma.json"
# fileS2 = "DataStorage/Sensitivity_04/SplineSensPost_mb.json"
# fileS3 = "DataStorage/Sensitivity_04/SplineSensPost_mc.json"
# fileF1 = "DataStorage/Sensitivity_04/F_Post.json"
# bisection = "P"
# d1 = np.array([24.17, 26.3, 23.09])
# d2 = np.array([25.37, 26.31, 21.54])
# d3 = np.array([24.09, 26.51, 21.54])




'''Sensitivity testing
2nd set sensitivity splines
'''
# # For Specimen 01 Anterior bisection
# name = "Specimen01 Anterior"
# dmatrix = np.array([
#     [137.94, 145.39, 141.13],
#     [118.6, 125.51, 121.51],
#     [95.15, 104.76, 100.81],
#     [72.55, 76.44, 73.7],
#     [49.05, 50.5, 49.38],
#     [26.62, 27.92, 26.5]
# ])
# offsets = np.zeros(len(dmatrix)) #  # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_01/SplineSensAnt_ma_2.json"
# fileS2 = "DataStorage/Sensitivity_01/SplineSensAnt_mb_2.json"
# fileS3 = "DataStorage/Sensitivity_01/SplineSensAnt_mc_2.json"
# fileF1 = "DataStorage/Sensitivity_01/F_Ant.json"
# bisection = "A"
# d1 = np.array([18.59, 21.19, 24.84, 25.14, 22.38])
# d2 = np.array([19.84, 23.58, 25.58, 27.36, 22.12])
# d3 = np.array([18.2, 20.6, 27.86, 24.17, 21.41])

# # For Specimen 02 Anterior Bisection
# name = "Specimen02 Anterior"
# dmatrix = np.array([
#     [94.19, 98.4, 96.74],
#     [70.66, 75.18, 72.06],
#     [49.76, 53.39, 51.23],
#     [23.08, 27.82, 23.96]
# ])
# offsets = np.zeros(len(dmatrix))  # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_02/SplineSensAnt_ma_2.json"
# fileS2 = "DataStorage/Sensitivity_02/SplineSensAnt_mb_2.json"
# fileS3 = "DataStorage/Sensitivity_02/SplineSensAnt_mc_2.json"
# fileF1 = "DataStorage/Sensitivity_02/F_Ant.json"
# bisection = "A"
# d1 = np.array([22.03, 20.96, 25.75])
# d2 = np.array([23.6, 22.66, 26.18])
# d3 = np.array([25.09, 21.31, 26.09])


# # For Specimen 02 Posterior Bisection
# name = "Specimen02 Posterior"
# dmatrix = np.array([
#     [108.06, 118.79, 106.07],
#     [97.62, 104.06, 99.13],
#     [89.25, 95.04, 90.14],
#     [81.04, 85.78, 83.06],
#     [72.54, 75.97, 74.19],
#     [65.65, 66.82, 65.55],
#     [58.57, 60.76, 58.2],
#     [50.55, 53.07, 50.01],
#     [42.81, 43.61, 41.81],
#     [31.95, 33.37, 31.32],
#     [21.57, 23.12, 21.07]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_02/SplineSensPost_ma_2.json"
# fileS2 = "DataStorage/Sensitivity_02/SplineSensPost_mb_2.json"
# fileS3 = "DataStorage/Sensitivity_02/SplineSensPost_mc_2.json"
# fileF1 = "DataStorage/Sensitivity_02/F_Post.json"
# bisection = "P"
# d1 = np.array([12.47, 9.48, 7.42, 8.16, 6.3, 7.49, 7.6, 6.98, 10.36, 9.63])
# d2 = np.array([18.55, 10.01, 9.88, 8.64, 8.83, 6.18, 7.22, 8.98, 9.49, 10.1])
# d3 = np.array([12.52, 10.15, 7.7, 8.71, 7.91, 6.38, 7.42, 7.54, 9.76, 9.83])


# # For Specimen 03 Anterior Bisection
# name = "Specimen03 Anterior"
# dmatrix = np.array([
#     [101.28, 119.29, 114.00],
#     [98.25, 106.58, 102.03],
#     [83.18, 89.78, 87.21],
#     [66.84, 72.37, 69.21],
#     [53.33, 54.72, 53.96],
#     [37.74, 39.27, 38.47],
#     [17.7, 17.1, 14.54]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_03/SplineSensAnt_ma_2.json"
# fileS2 = "DataStorage/Sensitivity_03/SplineSensAnt_mb_2.json"
# fileS3 = "DataStorage/Sensitivity_03/SplineSensAnt_mc_2.json"
# fileF1 = "DataStorage/Sensitivity_03/F_Ant.json"
# bisection = "A"
# d1 = np.array([2.48, 15.5, 16.32, 14.94, 16.05, 22.09])
# d2 = np.array([12.35, 17.08, 17.68, 12.89, 15.17, 23.66])
# d3 = np.array([11.86, 14.06, 16.21, 14.37, 15.33, 22.66])


# # For Specimen 03 Posterior Bisection
# name = "Specimen03 Posterior"
# dmatrix = np.array([
#     [110.74, 105.06, 105.43],
#     [99.49, 97.56, 96.9],
#     [80.17, 80.94, 79.74],
#     [62.13, 65.68, 62.2],
#     [46.67, 46.23, 44.74],
#     [30.79, 30.46, 29.42]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_03/SplineSensPost_ma_2.json"
# fileS2 = "DataStorage/Sensitivity_03/SplineSensPost_mb_2.json"
# fileS3 = "DataStorage/Sensitivity_03/SplineSensPost_mc_2.json"
# fileF1 = "DataStorage/Sensitivity_03/F_Post.json"
# bisection = "P"
# d1 = np.array([13.91, 19.55, 19.15, 14.94, 15.05])
# d2 = np.array([8.73, 18.36, 16.08, 19.62, 15.2])
# d3 = np.array([7.97, 18.1, 15.69, 16.93, 14.78])


# # For Specimen 04 Anterior Bisection
# name = "Specimen04 Anterior"
# dmatrix = np.array([
#     [99.85, 101.45, 98.03],
#     [86.48, 87.14, 83.77],
#     [68.38, 68.35, 65.32],
#     [57.69, 57.24, 54.56],
#     [49.7, 48.41, 46.97],
#     [36.27, 35.58, 29.17],
#     [23.14, 19.61, 12.44]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_04/SplineSensAnt_ma_2.json"
# fileS2 = "DataStorage/Sensitivity_04/SplineSensAnt_mb_2.json"
# fileS3 = "DataStorage/Sensitivity_04/SplineSensAnt_mc_2.json"
# fileF1 = "DataStorage/Sensitivity_04/F_Ant.json"
# bisection = "A"
# d1 = np.array([13.78, 17.36, 9.89, 8.93, 13.3, 15.34])
# d2 = np.array([13.75, 18.18, 11.02, 8.4, 14.1, 16.65])
# d3 = np.array([13.94, 17.23, 9.14, 8.68, 15.17, 16.32])

# # For Specimen 04 Posterior Bisection
# name = "Specimen04 Posterior"
# dmatrix = np.array([
#     [94.86, 90.37, 89.09],
#     [70.14, 69.48, 68.86],
#     [43.48, 41.95, 41.73],
#     [27.32, 22.85, 21.04]
# ])
# offsets = np.zeros(len(dmatrix)) # um, offsets of histology from cut face (due to thickness*number of microtomb slices).
# sign = 1
# fileS1 = "DataStorage/Sensitivity_04/SplineSensPost_ma_2.json"
# fileS2 = "DataStorage/Sensitivity_04/SplineSensPost_mb_2.json"
# fileS3 = "DataStorage/Sensitivity_04/SplineSensPost_mc_2.json"
# fileF1 = "DataStorage/Sensitivity_04/F_Post.json"
# bisection = "P"
# d1 = np.array([24.17, 26.3, 23.09])
# d2 = np.array([25.37, 26.31, 21.54])
# d3 = np.array([24.09, 26.51, 21.54])