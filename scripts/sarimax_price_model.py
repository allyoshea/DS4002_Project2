"""
Monthly electricity price model (SARIMA / ETS / combination) -- Jan 2015 to Jun 2026.

Usage:
    python sarimax_price_model.py [path/to/data.csv]          # fit default model, forecast 12 months
    python sarimax_price_model.py [path/to/data.csv] --cv     # compare candidates by rolling-origin CV,
                                                              # then forecast with the best one

What changed vs. the earlier version
  * USE_EXOG defaults to False (CV showed exog did not help; also gives the full 12-month forecast).
  * Plot bug fixed: diagnostics and forecast are now separate figures.
  * CV is leak-free: exog (if used) is standardized using each fold's training window only.
  * CV compares log vs level, several SARIMA orders, ETS, and an average of the best SARIMA + best ETS.
  * CV reports RMSE, MAE, MASE and 80% interval COVERAGE (should be close to 0.80).
  * With --cv, the final forecast uses the best candidate by 12-month RMSE.
"""

import sys, warnings
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.exponential_smoothing.ets import ETSModel
from statsmodels.stats.diagnostic import acorr_ljungbox

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------- config
_args         = [a for a in sys.argv[1:] if not a.startswith("--")]
PATH          = _args[0] if _args else "data.csv"
RUN_CV        = "--cv" in sys.argv
SEASONAL      = (0, 1, 1, 12)
ORDERS        = [(2, 1, 0), (0, 1, 2), (1, 1, 1)]   # candidate non-seasonal orders for CV
DEFAULT_MODEL = "SARIMA(2,1,0) level"               # used when --cv is not given
USE_EXOG      = False                               # True adds a SARIMAX candidate (see EXOG_COLS)
EXOG_COLS     = ["temp", "ng"]                      # keep this small
HORIZON       = 12
ALPHA         = 0.2                                 # 80% prediction intervals
FIRST_TRAIN   = 72                                  # months in the first CV training window
CV_STEP       = 3                                   # months between CV origins


# ---------------------------------------------------------------- data
def load(path=PATH):
    df = pd.read_csv(path, parse_dates=["Date"], index_col="Date")
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
    df.index.freq = "MS"
    df = df.rename(columns={"Electricity Price": "price", "CPI Change": "cpi"})
    df.columns = [c.lower() for c in df.columns]
    df["spending"] = np.log(df["spending"])
    X = df.drop(columns="price").interpolate(limit_area="inside")
    return df["price"], X


# ---------------------------------------------------------------- models
def build_specs():
    specs = {}
    for o in ORDERS:
        for log in (False, True):
            name = f"SARIMA({o[0]},{o[1]},{o[2]}) {'log' if log else 'level'}"
            specs[name] = dict(kind="sarima", order=o, seasonal=SEASONAL, log=log)
    for log in (False, True):
        specs[f"ETS {'log' if log else 'level'}"] = dict(kind="ets", log=log)
    if USE_EXOG:
        specs["SARIMAX(2,1,0) exog"] = dict(kind="sarima", order=(2, 1, 0), seasonal=SEASONAL,
                                            log=False, exog=True)
    return specs


def fit_sarima(z, Xtr, order, seasonal):
    m = SARIMAX(z, exog=Xtr, order=order, seasonal_order=seasonal,
                enforce_stationarity=False, enforce_invertibility=False)
    return m.fit(disp=False, maxiter=300)


def predict(spec, ytr, H, X=None):
    """Forecast H steps beyond ytr. Returns (mean, lower, upper) in ORIGINAL price units.
    For log models the mean is the median forecast (exp of the log-scale mean)."""
    z = np.log(ytr) if spec["log"] else ytr
    if spec["kind"] == "sarima":
        Xtr = Xf = None
        if spec.get("exog"):
            fidx = pd.date_range(ytr.index[-1] + pd.offsets.MonthBegin(1), periods=H, freq="MS")
            Xt = X.loc[ytr.index, EXOG_COLS]
            mu, sd = Xt.mean(), Xt.std()                     # training window only -> no leakage
            Xtr, Xf = (Xt - mu) / sd, (X.reindex(fidx)[EXOG_COLS] - mu) / sd
            if Xf.isna().any().any():
                raise ValueError("future exog values missing")
        res = fit_sarima(z, Xtr, spec["order"], spec["seasonal"])
        fc = res.get_forecast(H, exog=Xf)
        m, ci = fc.predicted_mean.values, fc.conf_int(alpha=ALPHA).values
        lo, hi = ci[:, 0], ci[:, 1]
    else:
        res = ETSModel(z, error="add", trend="add", damped_trend=True,
                       seasonal="add", seasonal_periods=12).fit(disp=False)
        pf = res.get_prediction(start=len(z), end=len(z) + H - 1).summary_frame(alpha=ALPHA)
        m, lo, hi = pf["mean"].values, pf["pi_lower"].values, pf["pi_upper"].values
    if spec["log"]:
        m, lo, hi = np.exp(m), np.exp(lo), np.exp(hi)
    return m, lo, hi


def safe_predict(spec, ytr, H, X=None):
    try:
        return predict(spec, ytr, H, X)
    except Exception:
        nan = np.full(H, np.nan)
        return nan, nan, nan


# ---------------------------------------------------------------- cross-validation
def score(preds, actuals, scales):
    """preds: list of (mean, lo, hi) per fold; actuals: list of arrays; scales: MASE denominators."""
    e = np.array([a - p[0] for a, p in zip(actuals, preds)])
    inside = np.array([(a >= p[1]) & (a <= p[2]) for a, p in zip(actuals, preds)], dtype=float)
    inside[np.isnan(np.array([p[1] for p in preds]))] = np.nan
    mase = np.nanmean([np.nanmean(np.abs(ei)) / s for ei, s in zip(e, scales)])
    return dict(RMSE_h1=np.sqrt(np.nanmean(e[:, 0] ** 2)),
                RMSE_h1_12=np.sqrt(np.nanmean(e ** 2)),
                MAE_h1_12=np.nanmean(np.abs(e)),
                MASE=mase,
                Cov80=np.nanmean(inside) if not np.isnan(inside).all() else np.nan)


def cv_compare(yo, X, specs, H=HORIZON):
    """Rolling-origin CV. Exog (if used) gets the TRUE future values, so it is a best case."""
    origins = list(range(FIRST_TRAIN, len(yo) - H + 1, CV_STEP))
    print(f"CV: {len(origins)} origins x {len(specs)} models (this can take a few minutes)...")
    store = {n: [] for n in specs}
    store["Seasonal naive"] = []
    actuals, scales = [], []
    for i, o in enumerate(origins, 1):
        ytr = yo.iloc[:o]
        actuals.append(yo.values[o:o + H])
        scales.append(np.mean(np.abs(ytr.values[12:] - ytr.values[:-12])))
        for n, sp in specs.items():
            store[n].append(safe_predict(sp, ytr, H, X))
        naive = ytr.values[-12:][:H]
        store["Seasonal naive"].append((naive, np.full(H, np.nan), np.full(H, np.nan)))
        print(f"  origin {i}/{len(origins)} done", end="\r")
    print()

    table = {n: score(p, actuals, scales) for n, p in store.items()}

    # combination: best SARIMA-type + best ETS (by 12-month RMSE), simple average
    best = lambda kind: min((n for n in specs if specs[n]["kind"] == kind and not specs[n].get("exog")),
                            key=lambda n: table[n]["RMSE_h1_12"])
    s_name, e_name = best("sarima"), best("ets")
    combo_name = f"Combo: {s_name} + {e_name}"
    store[combo_name] = [tuple((a + b) / 2 for a, b in zip(ps, pe))
                         for ps, pe in zip(store[s_name], store[e_name])]
    table[combo_name] = score(store[combo_name], actuals, scales)

    return pd.DataFrame(table).T.round(3), (combo_name, s_name, e_name)


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    y, X = load()
    yo = y.dropna().asfreq("MS")
    print(f"Response: {len(yo)} obs, {yo.index[0].date()} -> {yo.index[-1].date()}")
    specs = build_specs()

    combo = None
    if RUN_CV:
        cv, combo = cv_compare(yo, X, specs)
        print("\nRolling-origin CV (Cov80 should be ~0.80; MASE < 1 beats in-sample seasonal naive):\n", cv)
        cv.to_csv("cv_results.csv")
        chosen = cv.drop(index="Seasonal naive")["RMSE_h1_12"].idxmin()
        print(f"\nBest by 12-month RMSE: {chosen}")
    else:
        chosen = DEFAULT_MODEL
        print(f"Model: {chosen}")

    # ---- resolve the chosen model into component spec(s)
    if combo and chosen == combo[0]:
        parts = [specs[combo[1]], specs[combo[2]]]
    else:
        parts = [specs[chosen]]

    # ---- diagnostics for the (first) SARIMA component
    sar = next((p for p in parts if p["kind"] == "sarima"), None)
    if sar is not None:
        z = np.log(yo) if sar["log"] else yo
        Xd = None
        if sar.get("exog"):
            Xt = X.loc[yo.index, EXOG_COLS]
            Xd = (Xt - Xt.mean()) / Xt.std()
        res = fit_sarima(z, Xd, sar["order"], sar["seasonal"])
        print(res.summary())
        lb = acorr_ljungbox(res.resid.iloc[13:], lags=[12, 24], return_df=True)
        print("\nLjung-Box on residuals (p > 0.05 = no leftover autocorrelation):\n", lb.round(3))
        res.plot_diagnostics(figsize=(12, 8))
        plt.tight_layout(); plt.savefig("diagnostics_2.png", dpi=120)
        plt.close("all")                                    # <- fixes the overwritten forecast.png

    # ---- final forecast (Jul-Sep 2026 missing prices + a further year)
    fidx = pd.date_range(yo.index[-1] + pd.offsets.MonthBegin(1), periods=HORIZON, freq="MS")
    preds = [predict(p, yo, HORIZON, X) for p in parts]
    m, lo, hi = (np.mean([p[i] for p in preds], axis=0) for i in range(3))
    out = pd.DataFrame({"forecast": m, "lower_80": lo, "upper_80": hi}, index=fidx)
    print("\nForecast:\n", out.round(2))
    out.to_csv("forecast_2.csv")

    fig, ax = plt.subplots(figsize=(10, 4))                 # its own figure and axes
    yo["2022":].plot(ax=ax, label="actual")
    out["forecast"].plot(ax=ax, label="forecast")
    ax.fill_between(out.index, out["lower_80"], out["upper_80"], alpha=.2, label="80% interval")
    ax.set_ylabel("Electricity price"); ax.legend()
    fig.tight_layout(); fig.savefig("forecast_2.png", dpi=120)