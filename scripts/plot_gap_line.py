"""Plot |B| along the mid-line of the 0.9 mm fluid gap for the four excitations.

Input : data/gap_line/MagB_gap_midline_<NI>At.txt  (Maxwell Fields Calculator export,
        header 'Scalar data "Mag_B"', columns x y z |B| in m and T).
        The line is r = 24.55 mm (half way between piston R=24.1 mm and wall R=25 mm),
        z = -30 ... +30 mm, 121 points (data/gap_line/gap_midline_points.pts).
Output: figures/gap_line_B_vs_current.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
TURNS = 72  # physical coil turns used in the report; Maxwell excitation is Amp*Turns
cases = [144, 72, 36, 18]  # ampere-turns

fig, ax = plt.subplots(figsize=(7, 4))
for nI in cases:
    d = np.loadtxt(ROOT / f"data/gap_line/MagB_gap_midline_{nI}At.txt", skiprows=1)
    ax.plot(d[:, 2] * 1e3, d[:, 3], label=f"{nI} A-turns (I = {nI / TURNS:g} A)")
ax.axvspan(-22.5, 22.5, color="0.9", zorder=0, label="piston length (45 mm)")
ax.set_xlabel("z relative to piston centre [mm]")
ax.set_ylabel("|B| on gap mid-line [T]")
ax.set_title("Magnetic flux density along the MR-fluid gap")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)
fig.tight_layout()
out = ROOT / "figures/gap_line_B_vs_current.png"
fig.savefig(out, dpi=200)
print("wrote", out)
