"""Step 2 of the coupling: Maxwell |B| export -> table read by the Fluent UDF (DEFINE_INIT).

Input : data/coupling/03_maxwell_MagB_at_centroids_72At.txt
        header 'Scalar data "Mag_B"', columns X Y Z |B|
Output: fluent_udf/Finaluds_full_precision.txt with columns  x  y  B  (tab separated),
        x = Maxwell Z (axial), y = Maxwell Y (radial frame used in the export), B in tesla.
This reproduces data/coupling/04_Finaluds_x_y_B.txt (made in Excel) at full precision.
"""
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
d = np.loadtxt(ROOT / "data/coupling/03_maxwell_MagB_at_centroids_72At.txt", skiprows=1)
table = np.column_stack([d[:, 2], d[:, 1], d[:, 3]])
out = ROOT / "fluent_udf/Finaluds_full_precision.txt"
np.savetxt(out, table, fmt="%.9e", delimiter="\t")
print(f"wrote {len(table)} rows to {out}; |B| range {table[:,2].min():.3g} .. {table[:,2].max():.3g} T")
