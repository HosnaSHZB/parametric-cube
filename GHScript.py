# ============================================================
# PARAMETRIC CUBE
# Rhino 7 + Grasshopper + GhPython
# completed on 2024.07.01
# ============================================================

import rhinoscriptsyntax as rs
import System.Drawing as sd
import Rhino.Geometry as rg

eX = 10  # Set the number of boxes in the X direction.
eY = 10  # Set the number of boxes in the Y direction.
sX = 10  # Set the spacing of boxes in the X direction.
sY = 10  # Set the spacing of boxes in the Y direction.
sZ = 10  # Set the initial height of the boxes.

def create_geometry(eX, eY, sX, sY, sZ, refPoint):
    geo = []
    colours = []

    # Loop for creating the boxes and colors
    for x in range(eX):
        for y in range(eY):
            pt1 = rg.Point3d(x * sX, y * sY, 0)
            pt2 = rg.Point3d((x + 1) * sX, y * sY, 0)
            pt3 = rg.Point3d(x * sX, (y + 1) * sY, 0)
            plane = rs.PlaneFromPoints(pt1, pt2, pt3)
            
            # Distance from current point to the reference point
            dist = rs.Distance(pt1, refPoint)
            
            # Calculate box height influenced by distance to refPoint
            heightFactor = dist if dist else 0.5 * sZ  # Replace sZ/2*-1 with 0.5 * sZ if using positive heights
            box = rg.Box(plane, rg.Interval(-0.5 * sX, 0.5 * sX), rg.Interval(-0.5 * sY, 0.5 * sY), rg.Interval(-0.5 * sZ, heightFactor))
            geo.append(box)
            
            # Calculate colors
            color_factor = 255 / eX  # Adjust color scaling factor based on eX
            red = int(min(x * color_factor, 255))
            green = int(min(y * color_factor, 255))
            blue = 150  # Static blue value

            colours.append(sd.Color.FromArgb(255, red, green, blue))  # Add full opacity

    return geo, colours

# Example usage
# Define a reference point that can be adjusted to affect the geometry.
refPoint = rg.Point3d(20, 20, 0)  # Update the coordinates as needed.

# Generate the geometry with the current reference point.
geo, colours = create_geometry(eX, eY, sX, sY, sZ, refPoint)
