"""
Monthly electricity price model (SARIMA / SARIMAX) -- Jan 2015 to Jun 2026.

Usage:  python sarimax_price_model.py [path/to/data.csv] [--cv]

Selected by rolling-origin cross-validation (see cv_compare below):
  * Default model: SARIMA(2,1,0)(0,1,1,12) with NO exogenous variables.
  * Exogenous variants are included (USE_EXOG) but did not improve out-of-sample error.
"""
import sys, warnings
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox

warnings.filterwarnings("ignore")
_args     = [a for a in sys.argv[1:] if not a.startswith("--")]
PATH      = _args[0] if _args else "data.csv"
ORDER     = (2, 1, 0)
SEASONAL  = (0, 1, 1, 12)
USE_EXOG  = True                                     # flip to True to include predictors
EXOG_COLS = ["temp", "crude", "ng", "spending", "cpi"] # low-collinearity set (see notes)
HORIZON   = 12

# ---------------------------------------------------------------- data
def load(path=PATH):
    df = pd.read_csv(path, parse_dates=["Date"], index_col="Date")
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
    df.index.freq = "MS"
    df = df.rename(columns={"Electricity Price": "price", "CPI Change": "cpi"})
    df.columns = [c.lower() for c in df.columns]
    df["spending"] = np.log(df["spending"])            # grows ~30x over the sample
    X = df.drop(columns="price").interpolate(limit_area="inside")  # fills isolated gaps only
    return df["price"], X

def fit(y, X=None, order=ORDER, seasonal=SEASONAL):
    m = SARIMAX(y, exog=X, order=order, seasonal_order=seasonal,
                enforce_stationarity=False, enforce_invertibility=False)
    return m.fit(disp=False, maxiter=300)

# ---------------------------------------------------------------- validation
def cv_compare(y, X, first_train=72, step=3, H=HORIZON):
    """Rolling-origin CV. Exog models use the TRUE future exog values (best case)."""
    yo = y.dropna(); out = {}
    cfgs = {"SARIMA (no exog)": None, "SARIMAX (exog)": EXOG_COLS}
    for name, cols in cfgs.items():
        Z = None if cols is None else X.loc[yo.index, cols]
        if Z is not None: Z = (Z - Z.mean()) / Z.std()
        errs = []
        for o in range(first_train, len(yo) - H + 1, step):
            r = fit(yo.iloc[:o], None if Z is None else Z.iloc[:o])
            f = r.forecast(H, exog=None if Z is None else Z.iloc[o:o+H])
            errs.append(yo.values[o:o+H] - f.values)
        e = np.array(errs)
        out[name] = dict(RMSE_h1=np.sqrt((e[:, 0]**2).mean()),
                         RMSE_h1_12=np.sqrt((e**2).mean()), MAE_h1_12=np.abs(e).mean())
    e = np.array([yo.values[o:o+H] - yo.values[o-12:o-12+H]
                  for o in range(first_train, len(yo) - H + 1, step)])
    out["Seasonal naive"] = dict(RMSE_h1=np.sqrt((e[:, 0]**2).mean()),
                                 RMSE_h1_12=np.sqrt((e**2).mean()), MAE_h1_12=np.abs(e).mean())
    return pd.DataFrame(out).T.round(3)

# ---------------------------------------------------------------- main
if __name__ == "__main__":
    y, X = load()
    yo = y.dropna()
    print(f"Response: {len(yo)} obs, {yo.index[0].date()} -> {yo.index[-1].date()}")

    cols = EXOG_COLS if USE_EXOG else None
    if cols:
        mu, sd = X.loc[yo.index, cols].mean(), X.loc[yo.index, cols].std()
        Xs = (X[cols] - mu) / sd
    res = fit(yo, None if not cols else Xs.loc[yo.index])
    print(res.summary())

    lb = acorr_ljungbox(res.resid.iloc[13:], lags=[12, 24], return_df=True)
    print("\nLjung-Box on residuals (p > 0.05 = no leftover autocorrelation):\n", lb.round(3))
    res.plot_diagnostics(figsize=(12, 8)); plt.tight_layout(); plt.savefig("diagnostics.png", dpi=120)

    # Forecast: the 3 months with missing price (Jul-Sep 2026) + a further year
    last = yo.index[-1]
    fidx = pd.date_range(last + pd.offsets.MonthBegin(1), periods=HORIZON, freq="MS")
    if cols:
        Xf = Xs.reindex(fidx)
        if Xf.isna().any().any():
            print("\nNOTE: future exog has gaps -> forecast only where all predictors are known")
            fidx = Xf.dropna().index; Xf = Xf.loc[fidx]
    fc = res.get_forecast(len(fidx), exog=None if not cols else Xf)
    out = pd.concat([fc.predicted_mean.rename("forecast"), fc.conf_int(alpha=0.2)], axis=1)
    out.columns = ["forecast", "lower_80", "upper_80"]
    out.index = fidx
    print("\nForecast:\n", out.round(2)); out.to_csv("forecast.csv")

    ax = yo["2022":].plot(figsize=(10, 4), label="actual")
    out["forecast"].plot(ax=ax, label="forecast")
    ax.fill_between(out.index, out["lower_80"], out["upper_80"], alpha=.2)
    ax.legend(); ax.set_ylabel("Electricity price"); plt.tight_layout(); plt.savefig("forecast.png", dpi=120)

    if "--cv" in sys.argv:
        print("\nRolling-origin CV:\n", cv_compare(y, X))
