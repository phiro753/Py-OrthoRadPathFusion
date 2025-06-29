""" 
Description: Script that utilises seraliser and gets the control points for splines from 3DSlier

History: 
> Created by Robert Phillips 2024-03
"""
from a_JSONObjectRead import MarkupRead
import json

def extract_control_point_positions(file_path):
    # Load JSON data from file
    with open(file_path, 'r') as f:
        json_data = json.load(f)

    # Create Markup instance from JSON data (if needed can pull anything else from this class)
    markup = MarkupRead.from_json(json_data)
    
    # Extracting spline controlPoints 'positions'
    contorlpointlist = []
    for f in markup.controlPoints:
        contorlpointlist.append(f.get('position'))
    
    return contorlpointlist
