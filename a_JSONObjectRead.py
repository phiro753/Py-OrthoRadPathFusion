"""
Description: Seraliser for bringing in JSON data - reading 

History:
> Created by Robert Phillips 2024-03
"""
import json

class MarkupRead:
    def __init__(self, type_, coordinateSystem, coordinateUnits, locked, fixedNumberOfControlPoints, labelFormat, lastUsedControlPointNumber,
                 controlPoints, measurements, display):
        self.type = type_
        self.coordinateSystem = coordinateSystem
        self.coordinateUnits = coordinateUnits
        self.locked = locked
        self.fixedNumberOfControlPoints = fixedNumberOfControlPoints
        self.labelFormat = labelFormat
        self.lastUsedControlPointNumber = lastUsedControlPointNumber
        self.controlPoints = controlPoints
        self.measurements = measurements
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

    @classmethod
    def from_json(cls, json_data):
        # Extract markup data
        markup_data = json_data['markups'][0]
        
        # Extract display data
        display_data = markup_data['display']

        # Create Markup instance
        markup = cls(
            markup_data['type'],
            markup_data['coordinateSystem'],
            markup_data['coordinateUnits'],
            markup_data['locked'],
            markup_data['fixedNumberOfControlPoints'],
            markup_data['labelFormat'],
            markup_data['lastUsedControlPointNumber'],
            markup_data['controlPoints'],
            markup_data['measurements'],
            display_data
        )

        return markup