"""Step 1 of the coupling: turn the Fluent 2D cell centroids into a Maxwell point file.

Fluent (2D, axisymmetric about the damper axis) exports cell centroids as
    nodenumber, x-coordinate, y-coordinate      (x = axial, 0 ... 0.27 m)
Maxwell's 3D model has the piston centred on z = 0 and the fluid in r <= 25 mm.
The original work did this transform in Excel (data/coupling/02_maxwell_query_points_excel.pts):
    Z_maxwell = x_fluent - 0.1265            (axial shift: piston centre at z = 0)
    Y_maxwell = y_fluent - 0.025             (radial coordinate placed on the -Y side)
    X_maxwell = 0                            (sample the y-z half plane; field is axisymmetric)
Excel rounded the coordinates to 3 significant figures. This script writes full precision.

Usage: python scripts/fluent_to_maxwell_points.py
Output: data/coupling/02_maxwell_query_points.pts  (X Y Z in metres, tab separated)
Then in Maxwell: Fields Calculator -> Mag_B -> Export -> "Calculate grid points from file".
"""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
AXIAL_SHIFT = 0.1265   # m
RADIAL_SHIFT = 0.025   # m

c = np.loadtxt(ROOT / "data/coupling/01_fluent_cell_centroids.csv", delimiter=",", skiprows=1)
x_f, y_f = c[:, 1], c[:, 2]
pts = np.column_stack([np.zeros_like(x_f), y_f - RADIAL_SHIFT, x_f - AXIAL_SHIFT])
out = ROOT / "data/coupling/02_maxwell_query_points.pts"
np.savetxt(out, pts, fmt="%.9e", delimiter="\t")
print(f"wrote {len(pts)} points to {out}")
