"""Animated GIF: |B| on the gap mid-line, one excitation added per frame.

Output: figures/gap_line_B_vs_current.gif
"""
from pathlib import Path
import io
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
TURNS = 72
cases = [18, 36, 72, 144]  # ampere-turns, low to high
colors = ["#d62728", "#2ca02c", "#ff7f0e", "#1f77b4"]
data = {n: np.loadtxt(ROOT / f"data/gap_line/MagB_gap_midline_{n}At.txt", skiprows=1) for n in cases}

frames = []
for k in range(1, len(cases) + 1):
    fig, ax = plt.subplots(figsize=(7, 4), dpi=110)
    ax.axvspan(-22.5, 22.5, color="0.92", zorder=0)
    ax.text(0, 0.255, "piston (45 mm)", ha="center", fontsize=8, color="0.4")
    for n, c in zip(cases[:k], colors):
        d = data[n]
        ax.plot(d[:, 2] * 1e3, d[:, 3], color=c, lw=2, label=f"I = {n / TURNS:g} A ({n} A-turns)")
    n = cases[k - 1]
    ax.set_title(f"|B| along the gap mid-line, I = {n / TURNS:g} A ({n} A-turns)")
    ax.set_xlim(-30, 30); ax.set_ylim(0, 0.27)
    ax.set_xlabel("z relative to piston centre [mm]"); ax.set_ylabel("|B| [T]")
    ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    buf = io.BytesIO(); fig.savefig(buf, format="png"); plt.close(fig)
    frames.append(Image.open(buf).convert("P", palette=Image.ADAPTIVE))

out = ROOT / "figures/gap_line_B_vs_current.gif"
frames[0].save(out, save_all=True, append_images=frames[1:], duration=[1400] * 3 + [3000], loop=0)
print("wrote", out)
