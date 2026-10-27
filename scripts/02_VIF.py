"""
Collinearity check: variance inflation factor (VIF) for the 8 candidate
predictors vs the 5 predictors kept in the model.

VIF measures how much a predictor is duplicated by the other predictors.
Rules of thumb: under 5 = fine, 5 to 10 = moderate overlap, above 10 = high.

Usage (run from the project root):
    python scripts/vif_plot.py

Outputs:
    output/vif_table.csv    the VIF values
    output/vif_check.png    before/after bar chart (log scale)
"""

import os
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")   # save to file, never open a window
import matplotlib.pyplot as plt
from statsmodels.tools.tools import add_constant
from statsmodels.stats.outliers_influence import variance_inflation_factor

PATH = "data/data.csv"
OUT = "output"
ALL8 = ["Cooling", "Heating", "Crude", "NG", "Temp", "Spending", "CPI Change", "PowerPlantGeneration"]
FINAL5 = ["Crude", "NG", "Temp", "Spending", "CPI Change"]   # predictors kept in the model

os.makedirs(OUT, exist_ok=True)
df = pd.read_csv(PATH, index_col="Date", parse_dates=True)
df["Spending"] = np.log(df["Spending"])   # same log transform the model uses


def vifs(cols):
    """VIF for each column. add_constant adds the intercept; without it the
    VIFs are badly inflated for variables that sit far from zero."""
    Xc = add_constant(df[cols].dropna())
    # start at 1 to skip the intercept column itself
    return pd.Series([variance_inflation_factor(Xc.values, i) for i in range(1, Xc.shape[1])],
                     index=cols)


v8, v5 = vifs(ALL8), vifs(FINAL5)
table = pd.DataFrame({"VIF_all8": v8, "VIF_final5": v5}).round(1)
print(table)
table.to_csv(f"{OUT}/vif_table.csv")

# ---- Plot: grouped bars, log scale (Temp's 140 would flatten everything else on a linear axis) ----
x = np.arange(len(ALL8)); w = 0.38
fig, ax = plt.subplots(figsize=(11, 5))
bars8 = ax.bar(x - w / 2, v8.values, w, color="#0072B2", label="All 8 predictors")
v5_aligned = v5.reindex(ALL8)                  # NaN for the 3 dropped predictors
keep = v5_aligned.notna().values
bars5 = ax.bar(x[keep] + w / 2, v5_aligned.values[keep], w, color="#D55E00", label="Final 5 predictors")

ax.set_yscale("log")
ax.axhline(5, color="black", ls=":", lw=1.2, label="VIF = 5 (moderate overlap)")
ax.axhline(10, color="black", ls="--", lw=1.2, label="VIF = 10 (high overlap)")
ax.set_ylim(0.5, v8.max() * 4)                 # headroom so value labels never touch the frame

# value label above each bar
for bars in (bars8, bars5):
    for b in bars:
        h = b.get_height()
        ax.text(b.get_x() + b.get_width() / 2, h * 1.12, f"{h:.1f}", ha="center", va="bottom", fontsize=9)

ax.set_xticks(x)
# Long names are split over two lines so neighboring labels don't collide.
NICE = {"PowerPlantGeneration": "Power Plant\nGeneration", "CPI Change": "CPI\nChange"}
ax.set_xticklabels([NICE.get(c, c) + ("\n(dropped)" if c not in FINAL5 else "") for c in ALL8])
ax.set_ylabel("VIF (log scale)")
ax.set_title("Collinearity before and after dropping overlapping predictors")
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout(); fig.savefig(f"{OUT}/vif_check.png", dpi=120)
plt.close(fig)
print(f"\nSaved {OUT}/vif_check.png and {OUT}/vif_table.csv")