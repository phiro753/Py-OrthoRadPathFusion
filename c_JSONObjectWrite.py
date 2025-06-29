# Defining seraliser for bringing in JSON (reading) 
# Robert Phillips
#  2024-03-14

import json

class MarkupContent:
    def __init__(self, type_, coordinateSystem, coordinateUnits, locked, fixedNumberOfControlPoints, labelFormat,
                 lastUsedControlPointNumber, planeType, sizeMode, autoScalingFactor, center, normal, objectToBase,
                 baseToNode, orientation, size, planeBounds, controlPoints, measurements,display):
        self.type = type_
        self.coordinateSystem = coordinateSystem
        self.coordinateUnits = coordinateUnits
        self.locked = locked
        self.fixedNumberOfControlPoints = fixedNumberOfControlPoints
        self.labelFormat = labelFormat
        self.lastUsedControlPointNumber = lastUsedControlPointNumber
        self.planeType = planeType
        self.sizeMode = sizeMode
        self.autoScalingFactor = autoScalingFactor
        self.center = center
        self.normal = normal
        self.objectToBase = objectToBase
        self.baseToNode = baseToNode
        self.orientation = orientation
        self.size = size
        self.planeBounds = planeBounds
        self.controlPoints = [self.ControlPoint(**cp) for cp in controlPoints]
        self.measurements = [self.Measurement(**m) for m in measurements]
        self.display = display
        
        
    class ControlPoint:
        def __init__(self, id_, label, description, associatedNodeID, position, orientation, selected, locked, visibility, positionStatus):
            self.id = id_
            self.label = label
            self.description = description
            self.associatedNodeID = associatedNodeID
            self.position = position
            self.orientation = orientation
            self.selected = selected
            self.locked = locked
            self.visibility = visibility
            self.positionStatus = positionStatus

    class Measurement:
        def __init__(self, name, enabled, units, printFormat):
            self.name = name
            self.enabled = enabled
            self.units = units
            self.printFormat = printFormat

    def to_json(self):
        return {
            "@schema": "https://raw.githubusercontent.com/slicer/slicer/master/Modules/Loadable/Markups/Resources/Schema/markups-schema-v1.0.3.json#",
            "markups": [
                {
                    "type": self.type,
                    "coordinateSystem": self.coordinateSystem,
                    "coordinateUnits": self.coordinateUnits,
                    "locked": self.locked,
                    "fixedNumberOfControlPoints": self.fixedNumberOfControlPoints,
                    "labelFormat": self.labelFormat,
                    "lastUsedControlPointNumber": self.lastUsedControlPointNumber,
                    "planeType": self.planeType,
                    "sizeMode": self.sizeMode,
                    "autoScalingFactor": self.autoScalingFactor,
                    "center": self.center,
                    "normal": self.normal,
                    "objectToBase": self.objectToBase,
                    "baseToNode": self.baseToNode,
                    "orientation": self.orientation,
                    "size": self.size,
                    "planeBounds": self.planeBounds,
                    "controlPoints": [cp.__dict__ for cp in self.controlPoints],
                    "measurements": [m.__dict__ for m in self.measurements],
                    "display": self.display
                }
            ]
        }