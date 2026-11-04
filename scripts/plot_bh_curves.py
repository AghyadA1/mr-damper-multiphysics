"""Plot the nonlinear B-H curves used in Maxwell (MR fluid and steel 1008).

Output: figures/BH_curves.png
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
mr = np.loadtxt(ROOT / "maxwell/materials/MR_fluid_BH_kA-per-m_T.csv", delimiter=",")
# Steel 1008 B-H points from the Maxwell system material library (as stored in the .aedt)
steel_H = [0, 159.2, 318.3, 477.5, 636.6, 795.8, 1591.5, 3183.1, 4774.6, 6366.2, 7957.7, 15915.5,
           31831, 47746.5, 63662, 79577.5, 159155, 318310, 397887]
steel_B = [0, 0.2402, 0.8654, 1.1106, 1.2458, 1.331, 1.5, 1.6, 1.683, 1.741, 1.78, 1.905,
           2.025, 2.085, 2.13, 2.165, 2.28, 2.485, 2.5851]

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(mr[:, 0], mr[:, 1], "o-", ms=3, label="MR fluid (digitized, custom material)")
ax.plot(np.array(steel_H) / 1e3, steel_B, "s-", ms=3, label="Steel 1008 (piston, cylinder)")
ax.set_xlim(0, 400)
ax.set_xlabel("H [kA/m]"); ax.set_ylabel("B [T]")
ax.set_title("Nonlinear B-H curves used in the magnetostatic model")
ax.grid(alpha=0.3); ax.legend()
fig.tight_layout()
fig.savefig(ROOT / "figures/BH_curves.png", dpi=200)
print("wrote figures/BH_curves.png")
