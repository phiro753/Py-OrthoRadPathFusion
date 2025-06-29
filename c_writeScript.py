""" 
Description: Writing py plane (defined by origin and coefficients) info to JSON plane in format for import back into Slicer Scene

History:
> Created by Robert Phillips 2024-04
"""

from c_JSONObjectWrite import MarkupContent # calling the seraliser as an object
import json
import numpy as np
import math
import os


class writeRunning:
    def __init__(self, dmatrix, offsets, sign, S1, S2, npNorm2Cut):
        self.dmatrix = dmatrix
        self.offsets = offsets
        self.sign = sign
        self.S1 = S1
        self.S2 = S2
        self.npNorm2Cut = npNorm2Cut


    def write_to_folder(self, output_directory, bisection):
    # Ensure output directory exists
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        NormalsArray = self.npNorm2Cut
        Plxorigins = np.mean([self.S1.intx, self.S2.intx], axis=0)
        Plyorigins = np.mean([self.S1.inty, self.S2.inty], axis=0)
        Plzorigins = np.mean([self.S1.intz, self.S2.intz], axis=0)
        CentresArray = np.zeros((len(self.dmatrix), 3))

        for i in range(len(self.dmatrix)):
            offsets_vector = NormalsArray[i] * (self.sign * self.offsets[i] / 1000)
            CentresArray[i, :] = [Plxorigins[i], Plyorigins[i], Plzorigins[i]] + offsets_vector
            
            # Safely construct output file path
            writefile = os.path.join(output_directory, f"{bisection}_P_{i+1}.json")
            
            # Create plane JSON
            Writ = writeFunschema(writefile, CentresArray[i], NormalsArray[i])
            baseToNode = Writ.CalcBase2Node()
            Writ.writeFun(baseToNode.flatten().tolist())


class writeFunschema:
    def __init__(self, writefilename, centre, normal):
        self.filename = writefilename
        self.centre = centre
        self.normal = normal

    def CalcBase2Node(self):
        '''Calculating the baseToNode matrix for JSON import into Slicer'''
        # Normalize the normal vector
        self.normal /= np.linalg.norm(self.normal)

        # Choose an arbitrary vector not parallel to the self.normal (e.g., x-axis)
        arbitrary_vector = np.array([1, 0, 0])

        # Calculate the third axis of the plane coordinate system
        third_axis = np.cross(self.normal, arbitrary_vector)
        third_axis /= np.linalg.norm(third_axis)

        # Calculate the second axis of the plane coordinate system
        second_axis = np.cross(self.normal, third_axis)
        second_axis /= np.linalg.norm(second_axis)

        # Construct the rotation-translation matrix baseToNode
        base_to_node_matrix = np.eye(4)
        base_to_node_matrix[:3, 0] = third_axis
        base_to_node_matrix[:3, 1] = second_axis
        base_to_node_matrix[:3, 2] = self.normal
        base_to_node_matrix[:3, 3] = self.centre

        return base_to_node_matrix

    def writeFun(self, base2n):
        '''calling seraliser and writing function'''
        # Need each of the below objects specified before run seraliser
        # Example instance of PlaneMarkup
        markupcontent = MarkupContent(
            type_="Plane",
            coordinateSystem="LPS",
            coordinateUnits="mm",
            locked=False,
            fixedNumberOfControlPoints=False,
            labelFormat="%N-%d",
            lastUsedControlPointNumber=1,
            planeType="pointNormal",
            sizeMode="auto",
            autoScalingFactor=1.0,
            ## Inputting parameters of plane
            center = self.centre.tolist(),
            normal = self.normal.tolist(),
            objectToBase=[-1.0, -0.0, -0.0, -0.0, -0.0, -1.0, -0.0, -0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0],
            ## for baseToNode note: https://discourse.slicer.org/t/plane-markup-json-files-how-to-create-basetonode-and-orientation-matrices/31826/2 
            baseToNode = base2n,
            orientation=[0, 0, self.normal[0], 0, 0, self.normal[1], 0, 0, self.normal[2]], 
            # 
            size=[10.0, 10.0, 0.0],
            planeBounds=[-20.0, 20.0, -20.0, 20.0],
            controlPoints=[
                {
                    "id_": "1",
                    "label": "P-1",
                    "description": "",
                    "associatedNodeID": "",
                    "position": self.centre.tolist(),
                    "orientation": [-1.0, -0.0, -0.0, -0.0, -1.0, -0.0, 0.0, 0.0, 1.0],
                    "selected": True,
                    "locked": False,
                    "visibility": True,
                    "positionStatus": "defined"
                }
            ],
            measurements=[
                {
                    "name": "area",
                    "enabled": False,
                    "units": "cm2",
                    "printFormat": "%-#4.4g%s"
                }
            ],
            display={
                "visibility": False,
                "opacity": 1.0,
                "color": [0.4, 1.0, 0.0],
                "selectedColor": [1.0, 0.500008, 0.500008],
                "activeColor": [0.4, 1.0, 0.0],
                "propertiesLabelVisibility": True,
                "pointLabelsVisibility": False,
                "textScale": 3.0,
                "glyphType": "Sphere3D",
                "glyphScale": 3.0,
                "glyphSize": 5.0,
                "useGlyphScale": True,
                "sliceProjection": False,
                "sliceProjectionUseFiducialColor": True,
                "sliceProjectionOutlinedBehindSlicePlane": False,
                "sliceProjectionColor": [1.0, 1.0, 1.0],
                "sliceProjectionOpacity": 0.6,
                "lineThickness": 0.2,
                "lineColorFadingStart": 1.0,
                "lineColorFadingEnd": 10.0,
                "lineColorFadingSaturation": 1.0,
                "lineColorFadingHueoffsets": 0.0,
                "handlesInteractive": True,
                "translationHandleVisibility": False,
                "rotationHandleVisibility": False,
                "scaleHandleVisibility": True,
                "interactionHandleScale": 3.0,
                "snapMode": "toVisibleSurface"
            }
        )

        # creating then writing to a JSON file
        with open(self.filename,"w") as fw:
            json.dump(markupcontent.to_json(),fw,indent=4)
