"""
Monthly U.S. residential electricity price model (SARIMA / SARIMAX).

PROJECT QUESTION
    Can a SARIMAX model predict monthly U.S. residential electricity prices
    (per kWh) from past trends in predictors (temperature, crude oil, natural
    gas, consumer spending, CPI) with an accuracy of at least 85%?

HOW "ACCURACY" IS DEFINED
    Accuracy = 100% - MAPE
    MAPE (mean absolute percentage error) is the average size of the forecast
    error as a percent of the real price. So 85% accuracy means forecasts are
    off by 15% or less on average.

WHAT THIS SCRIPT DOES
    1. HOLDOUT TEST: hide the last 12 months of real prices, train on
       everything before them, forecast those 12 months, and compare the
       forecast to the real prices. This is the accuracy evidence.
    2. ROLLING CROSS-VALIDATION (only with --cv): repeat the "hide, forecast,
       compare" test over many different past periods, so the result does not
       depend on one lucky or unlucky year.
    3. FINAL FORECAST: refit on ALL the data and forecast into the future.
       These future months cannot be scored (they have not happened yet).

HOW TO RUN (from the project root, the folder containing data/ and output/)
    python scripts/sarimax_model_final.py data/data.csv          # holdout + forecast

OUTPUTS (all saved in output/)
    holdout_results.csv          accuracy metrics for the holdout test
    holdout.png                  forecast vs actual plot (validation slide)
    accuracy_vs_goal.png         bar chart of accuracy vs the 85% goal (results slide)
    coefficients.png             which predictors matter (results slide)

    diagnostics.png              residual diagnostic plots
    forecast_sarimax.csv         forecast using predictors (months where all are known)
    forecast_sarima_12mo.csv     full 12-month forecast without predictors
    forecast_sarimax.png         forecast plot
"""

#importing packages
import os, sys, warnings
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")    # "Agg" = save plots to files, never open a window
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX          # the model
from statsmodels.stats.diagnostic import acorr_ljungbox          # residual autocorrelation test

warnings.filterwarnings("ignore")   # hide routine statsmodels warnings to keep output readable

# SETTINGS (set them here and they are used throughout the rest of the script

# Command-line arguments: anything not starting with "--" is treated as the data file path.
_args       = [a for a in sys.argv[1:] if not a.startswith("--")]
PATH        = _args[0] if _args else "data/data.csv"   # where the data file is
OUT         = "output"                                 # folder where results are saved

# SARIMA settings. Notation: SARIMA(p,d,q)(P,D,Q,s)
ORDER       = (2, 1, 0)       # p=2 autoregressive terms, d=1 difference (removes the trend), q=0
SEASONAL    = (0, 1, 1, 12)   # D=1 seasonal difference, Q=1 seasonal MA term, s=12 (yearly cycle)

EXOG_COLS   = ["temp", "crude", "ng", "spending", "cpi"]   # the five predictors ("exogenous" variables)
HORIZON     = 12              # forecast this many months ahead
ALPHA       = 0.2             # 0.2 -> 80% prediction intervals (1 - 0.2 = 80%)
FIRST_TRAIN = 72              # CV: the first training window is the first 72 months
CV_STEP     = 3               # CV: move the forecast starting point forward 3 months each round
TARGET      = 85.0            # the project's accuracy goal, in percent

# Colorblind-safe palette (Okabe-Ito). Every model also gets its own line style
# and marker, so the plots still work in grayscale or with color-vision deficiency.
COLORS = {"SARIMA (no exog)": "#0072B2",    # blue
          "SARIMAX (exog)":   "#D55E00",    # vermillion
          "Seasonal naive":   "#009E73"}    # bluish green
LINESTYLES = {"SARIMA (no exog)": "--", "SARIMAX (exog)": ":", "Seasonal naive": "-."}
MARKERS    = {"SARIMA (no exog)": "o",  "SARIMAX (exog)": "s", "Seasonal naive": "^"}

# The two models we compare. None = no predictors (plain SARIMA); a list = use those predictors (SARIMAX).
CONFIGS = {"SARIMA (no exog)": None, "SARIMAX (exog)": EXOG_COLS}


# ======================================================================
# DATA LOADING AND CLEANING
# ======================================================================
def load(path=PATH):
    """Read the CSV and return (price, predictors).
    price      = the monthly electricity price we want to forecast (the response)
    predictors = temp, crude, ng, spending, cpi (used by SARIMAX only)"""
    # Read the file, treating the "Date" column as the row index.
    df = pd.read_csv(path, parse_dates=["Date"], index_col="Date")
    # Drop any blank "Unnamed" columns that Excel sometimes adds.
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")])
    df.index.freq = "MS"   # tell pandas the data is monthly, dated at the start of each month

    # Give the columns shorter names, then make all names lowercase for consistency.
    df = df.rename(columns={"Electricity Price": "price", "CPI Change": "cpi"})
    df.columns = [c.lower() for c in df.columns]

    # Log-transform spending: it was highly skewed (skew 1.68) and the log
    # makes it roughly symmetric (skew 0.43). Natural gas is also skewed but a
    # log transform did not improve accuracy, so it is left as is.
    df["spending"] = np.log(df["spending"])

    # Everything except price is a predictor. Fill gaps that sit BETWEEN known
    # values (interpolate), but never invent values past the end of the data.
    X = df.drop(columns="price").interpolate(limit_area="inside")
    return df["price"], X


# ======================================================================
# MODEL FITTING AND FORECASTING
# ======================================================================
def fit(y, X=None, order=ORDER, seasonal=SEASONAL):
    """Fit one SARIMA (X=None) or SARIMAX (X=predictors) model and return it.
    enforce_* = False lets the optimizer search more freely, which avoids
    failed fits on short series."""
    m = SARIMAX(y, exog=X, order=order, seasonal_order=seasonal,
                enforce_stationarity=False, enforce_invertibility=False)
    return m.fit(disp=False, maxiter=300)   # disp=False keeps the optimizer quiet


def forecast_from(train, Xall, cols, H=HORIZON):
    """Train on `train` (a price series), then forecast the next H months.
    Returns three arrays: forecast, lower 80% bound, upper 80% bound.

    Important details:
      * Predictors are standardized using the TRAINING months only, so the
        months being forecast never influence the scaling (no data leakage).
      * The forecast uses the TRUE future predictor values, so SARIMAX results
        are a best case. In real use you would have to forecast those too."""
    # The H months right after the end of the training data.
    fidx = pd.date_range(train.index[-1] + pd.offsets.MonthBegin(1), periods=H, freq="MS")
    Xtr = Xf = None   # stay None for the no-predictor SARIMA model
    if cols:
        Xt = Xall.loc[train.index, cols]       # predictors during the training months
        mu, sd = Xt.mean(), Xt.std()           # their average and standard deviation (training only)
        Xtr = (Xt - mu) / sd                   # standardize: (value - average) / std dev
        Xf = (Xall.reindex(fidx)[cols] - mu) / sd   # standardize future values the same way
        if Xf.isna().any().any():
            raise ValueError("future predictor values missing")   # can't forecast without them
    res = fit(train, Xtr)                       # fit the model
    fc = res.get_forecast(H, exog=Xf)           # forecast H months ahead
    ci = fc.conf_int(alpha=ALPHA).values        # 80% prediction interval: [:,0]=lower, [:,1]=upper
    return fc.predicted_mean.values, ci[:, 0], ci[:, 1]


# ======================================================================
# SCORING (turning forecasts into accuracy numbers)
# ======================================================================
def score(actual, pred, lo=None, hi=None):
    """Compare forecasts to real prices. `actual` and `pred` are 2-D arrays
    shaped (number of forecast rounds, months per round). lo/hi are the 80%
    interval bounds (optional).

    Sign convention: error = actual - forecast. Bias is forecast - actual,
    so a positive Bias means the model over-forecasts."""
    e = actual - pred                          # error for every forecast
    ape = np.abs(e) / actual * 100             # absolute percent error for every forecast
    out = dict(
        RMSE=np.sqrt(np.nanmean(e ** 2)),      # typical error size; punishes big misses more
        MAE=np.nanmean(np.abs(e)),             # average miss, in price units
        MAPE_pct=np.nanmean(ape),              # average miss as a percent of the real price
        Accuracy_pct=100 - np.nanmean(ape),    # the project's accuracy: 100 - MAPE
        Accuracy_h1_pct=100 - np.nanmean(ape[:, 0]),   # accuracy for just the 1-month-ahead forecast
        # R2: share of price variation explained. Looks high for trending data, so use with care.
        R2=1 - np.nansum(e ** 2) / np.nansum((actual - np.nanmean(actual)) ** 2),
        Bias=np.nanmean(pred - actual),                       # average over/under-forecast, price units
        Bias_pct=np.nanmean((pred - actual) / actual * 100),  # same, as a percent
    )
    if lo is not None:
        # Coverage: share of real prices inside the 80% interval (should be near 0.80).
        out["Cov80"] = np.nanmean((actual >= lo) & (actual <= hi))
        # Average interval width: narrower = more precise (as long as coverage is still ok).
        out["Avg_width"] = np.nanmean(hi - lo)
    return out


def by_horizon(actual, pred):
    """Accuracy (%) for each months-ahead step: 1 month ahead, 2 months ahead, ... 12."""
    ape = np.abs(actual - pred) / actual * 100
    return 100 - np.nanmean(ape, axis=0)   # average over forecast rounds, keep each horizon separate


# ======================================================================
# 1. HOLDOUT TEST
# ======================================================================
def holdout(yo, Xall, H=HORIZON):
    """Train on all but the last H months, forecast those H months, and score
    the forecast against the real prices."""
    train, test = yo.iloc[:-H], yo.iloc[-H:]   # everything before / the last 12 months
    print(f"\nHOLDOUT: train {train.index[0].date()} -> {train.index[-1].date()}, "
          f"test {test.index[0].date()} -> {test.index[-1].date()}")

    rows, fcs = {}, {}   # rows = metrics per model, fcs = forecasts per model (for plotting)
    for name, cols in CONFIGS.items():
        m, lo, hi = forecast_from(train, Xall, cols, H)
        fcs[name] = (m, lo, hi)
        # [None, :] turns a 1-D array into a 2-D one with a single forecast round.
        rows[name] = score(test.values[None, :], m[None, :], lo[None, :], hi[None, :])

    # Baseline: "seasonal naive" simply predicts each month equals the same month last year.
    # Any useful model should beat this.
    naive = train.values[-12:][:H]
    fcs["Seasonal naive"] = (naive, None, None)
    rows["Seasonal naive"] = score(test.values[None, :], naive[None, :])

    table = pd.DataFrame(rows).T.round(3)
    print(table.to_string())
    table.to_csv(f"{OUT}/holdout_results.csv")

    # ---- Plot: forecast vs actual ----
    # Everything is drawn with matplotlib (not pandas .plot) so all lines line up on the same axis.
    fig, ax = plt.subplots(figsize=(10, 4.5))
    hist = yo.iloc[-36 - H:]   # show the last 36 months of history plus the 12 test months (zoomed in)
    ax.plot(hist.index, hist.values, color="black", lw=2.5, label="actual")
    # Colors, line styles and markers differ so overlapping lines can still be told apart.
    for name, (m, lo, hi) in fcs.items():
        c, ls, mk = COLORS[name], LINESTYLES[name], MARKERS[name]
        ax.plot(test.index, m, color=c, ls=ls, marker=mk, ms=5, lw=1.8, label=name)
        if name == "SARIMAX (exog)":
            # Shaded band = 80% prediction interval: real prices should land inside it ~80% of the time.
            ax.fill_between(test.index, lo, hi, color=c, alpha=.12,
                            label="SARIMAX 80% interval")
    ax.axvline(test.index[0], color="grey", ls="--")   # dashed line = where the test period starts
    ax.set_ylabel("Electricity price"); ax.set_title("Holdout: forecast vs actual")
    ax.legend()
    fig.tight_layout(); fig.savefig(f"{OUT}/holdout.png", dpi=120)
    plt.close(fig)

    # ---- Plot: accuracy vs the 85% goal (bar chart for the results slide) ----
    acc = table["Accuracy_pct"]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(acc.index, acc.values, color=[COLORS[n] for n in acc.index])
    ax.axhline(TARGET, color="black", ls="--", label=f"{TARGET:.0f}% goal")   # the goal line
    ax.set_ylim(0, 100)   # full 0-100 axis so the bar heights are not exaggerated
    ax.set_ylabel("Accuracy (%)")
    ax.set_title("Holdout accuracy vs goal"); ax.legend(loc="lower right")
    for b, v in zip(bars, acc.values):   # write the exact value inside the top of each bar
        ax.text(b.get_x() + b.get_width() / 2, v - 2, f"{v:.1f}%",
                ha="center", va="top", color="white", fontweight="bold")
    fig.tight_layout(); fig.savefig(f"{OUT}/accuracy_vs_goal.png", dpi=120)
    plt.close(fig)
    return table


# ======================================================================
# 2. ROLLING-ORIGIN CROSS-VALIDATION (only runs with --cv)
# ======================================================================
def cv_compare(yo, Xall, H=HORIZON):
    """Repeat the hide-forecast-compare test many times. Each round trains on
    the months up to an 'origin', forecasts the next 12, and moves the origin
    forward 3 months. Averaging over all rounds gives a more trustworthy
    accuracy than a single holdout year."""
    # Origins = how many months of data the model trains on in each round.
    origins = list(range(FIRST_TRAIN, len(yo) - H + 1, CV_STEP))
    print(f"\nCV: {len(origins)} origins x {len(CONFIGS)} models (may take a few minutes)...")
    # The real prices for the 12 months after each origin.
    actual = np.array([yo.values[o:o + H] for o in origins])

    rows, horizons = {}, {}
    for name, cols in CONFIGS.items():
        P, L, U = [], [], []   # forecasts, lower bounds, upper bounds from every round
        for i, o in enumerate(origins, 1):
            try:
                m, lo, hi = forecast_from(yo.iloc[:o], Xall, cols, H)
            except Exception:
                # If one round fails (e.g. predictors missing), record NaN and keep going.
                m = lo = hi = np.full(H, np.nan)
            P.append(m); L.append(lo); U.append(hi)
            print(f"  {name}: origin {i}/{len(origins)}", end="\r")   # progress counter
        print()
        P, L, U = map(np.array, (P, L, U))
        rows[name] = score(actual, P, L, U)
        horizons[name] = by_horizon(actual, P)

    # Baseline again: same month last year, for each round.
    naive = np.array([yo.values[o - 12:o - 12 + H] for o in origins])
    rows["Seasonal naive"] = score(actual, naive)
    horizons["Seasonal naive"] = by_horizon(actual, naive)

    table = pd.DataFrame(rows).T.round(3)
    hz = pd.DataFrame(horizons, index=range(1, H + 1)).round(2)   # rows = months ahead (1..12)
    table.to_csv(f"{OUT}/cv_results.csv"); hz.to_csv(f"{OUT}/cv_by_horizon.csv")
    print("\nRolling-origin CV (Cov80 should be ~0.80):\n", table.to_string())
    print("\nAccuracy (%) by forecast horizon:\n", hz.to_string())

    # ---- Plot: accuracy by months ahead ----
    fig, ax = plt.subplots(figsize=(8, 4))
    for name in hz.columns:
        ax.plot(hz.index, hz[name], color=COLORS[name], ls=LINESTYLES[name],
                marker=MARKERS[name], label=name)
    ax.axhline(TARGET, color="black", ls="--", label=f"{TARGET:.0f}% goal")
    ax.set_ylim(0, 100)   # full 0-100 axis, same as the bar chart
    ax.set_xlabel("Months ahead"); ax.set_ylabel("Accuracy (%)")
    ax.set_title("Accuracy by forecast horizon (CV)"); ax.legend()
    fig.tight_layout(); fig.savefig(f"{OUT}/cv_accuracy_by_horizon.png", dpi=120)
    plt.close(fig)
    return table


# ======================================================================
# 3. FINAL FIT AND FUTURE FORECAST
# ======================================================================
def final_forecast(yo, Xall):
    """Refit on ALL available data, print the model summary and diagnostics,
    and forecast the future. These forecasts cannot be scored because the
    real prices do not exist yet."""
    last = yo.index[-1]
    print(f"\nFINAL FIT on all data: {yo.index[0].date()} -> {last.date()} ({len(yo)} obs)")
    # The 12 months after the last known price.
    fidx = pd.date_range(last + pd.offsets.MonthBegin(1), periods=HORIZON, freq="MS")

    # Standardize predictors using all known months, then fit the SARIMAX model.
    mu, sd = Xall.loc[yo.index, EXOG_COLS].mean(), Xall.loc[yo.index, EXOG_COLS].std()
    Xs = (Xall[EXOG_COLS] - mu) / sd
    res = fit(yo, Xs.loc[yo.index])

    # ---- Plot: which predictors matter ----
    # Dot = estimated effect on price of a 1-standard-deviation increase in that predictor.
    # Line = 95% confidence interval. If the line crosses the dashed zero line, the effect
    # is not clearly different from zero.
    coef = res.params[EXOG_COLS]
    ci = res.conf_int().loc[EXOG_COLS]
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.errorbar(coef.values, range(len(coef)),
                xerr=[coef.values - ci.iloc[:, 0].values, ci.iloc[:, 1].values - coef.values],
                fmt="o", capsize=4)
    ax.set_yticks(range(len(coef))); ax.set_yticklabels(coef.index)
    ax.axvline(0, color="grey", ls="--")
    ax.set_xlabel("Effect on price per 1 standard deviation (95% interval)")
    ax.set_title("Which predictors matter")
    fig.tight_layout(); fig.savefig(f"{OUT}/coefficients.png", dpi=120); plt.close(fig)

    # Full statistical summary (coefficients, p-values, AIC, diagnostic tests).
    print(res.summary())

    # Ljung-Box test: checks whether the errors still contain a pattern.
    # p > 0.05 = no leftover pattern = the model captured trend and seasonality.
    # [13:] skips the first 13 residuals, which are distorted by differencing.
    lb = acorr_ljungbox(res.resid.iloc[13:], lags=[12, 24], return_df=True)
    print("\nLjung-Box on residuals (p > 0.05 = no leftover autocorrelation):\n", lb.round(3))

    # Standard residual plots: errors over time, histogram, Q-Q plot, autocorrelation.
    res.plot_diagnostics(figsize=(12, 8)); plt.tight_layout()
    plt.savefig(f"{OUT}/diagnostics.png", dpi=120); plt.close("all")

    # ---- Forecast A: SARIMAX, only months where EVERY predictor is known ----
    # SARIMAX needs future predictor values to forecast, which is why this
    # forecast covers fewer months than the plain SARIMA one below.
    Xf = Xs.reindex(fidx).dropna()
    out_x = None
    if len(Xf):
        fc = res.get_forecast(len(Xf), exog=Xf)
        out_x = pd.concat([fc.predicted_mean, fc.conf_int(alpha=ALPHA)], axis=1)
        out_x.columns = ["forecast", "lower_80", "upper_80"]; out_x.index = Xf.index
        print("\nSARIMAX forecast (months with known predictors):\n", out_x.round(2))
        out_x.to_csv(f"{OUT}/forecast_sarimax.csv")
    else:
        print("\nNo future predictor values available -> skipping SARIMAX forecast.")

    # ---- Forecast B: plain SARIMA (no predictors), full 12 months ----
    res0 = fit(yo)
    fc0 = res0.get_forecast(HORIZON)
    out_0 = pd.concat([fc0.predicted_mean, fc0.conf_int(alpha=ALPHA)], axis=1)
    out_0.columns = ["forecast", "lower_80", "upper_80"]; out_0.index = fidx
    print("\nSARIMA forecast (no predictors, 12 months):\n", out_0.round(2))
    out_0.to_csv(f"{OUT}/forecast_sarima_12mo.csv")

    # ---- Plot: history plus forecasts ----
    fig, ax = plt.subplots(figsize=(10, 4))
    hist = yo["2022":]   # show 2022 onward (change to hist = yo to show the full 2015+ history)
    ax.plot(hist.index, hist.values, color="black", label="actual")
    # Each forecast line starts at the last actual point so there is no visible gap.
    ax.plot([hist.index[-1], *out_0.index], [hist.values[-1], *out_0["forecast"]],
            color=COLORS["SARIMA (no exog)"], ls="--", label="SARIMA 12-mo forecast")
    ax.fill_between(out_0.index, out_0["lower_80"], out_0["upper_80"],
                    color=COLORS["SARIMA (no exog)"], alpha=.15, label="80% interval")
    if out_x is not None:
        ax.plot([hist.index[-1], *out_x.index], [hist.values[-1], *out_x["forecast"]],
                color=COLORS["SARIMAX (exog)"], marker="s", ms=6, label="SARIMAX forecast")
    ax.set_ylabel("Electricity price"); ax.legend()
    fig.tight_layout(); fig.savefig(f"{OUT}/forecast_sarimax.png", dpi=120); plt.close(fig)


# ======================================================================
# MAIN: runs when you execute the script
# ======================================================================
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)   # create output/ if it does not exist yet

    y, X = load()
    # Keep only months that have a price, as a clean monthly series.
    yo = y.dropna().asfreq("MS")
    print(f"Response: {len(yo)} obs, {yo.index[0].date()} -> {yo.index[-1].date()}")

    # Fill gaps in the predictors ONLY over months where the price is known.
    # Months after the last price stay NaN so we can see which future predictor
    # values are truly unknown.
    Xall = X.copy()
    Xall.loc[Xall.index.isin(yo.index)] = Xall.loc[yo.index].ffill().bfill()

    # Step 1: holdout test (always runs, fast). Step 2: rolling CV (only with --cv).
    tables = {"Holdout": holdout(yo, Xall)}
    if RUN_CV:
        tables["Rolling CV"] = cv_compare(yo, Xall)

    # Summary: did each model meet the 85% accuracy goal?
    print("\n" + "=" * 60)
    print(f"ACCURACY vs {TARGET:.0f}% TARGET (Accuracy = 100 - MAPE)")
    for label, t in tables.items():
        for name in ("SARIMA (no exog)", "SARIMAX (exog)"):
            a = t.loc[name, "Accuracy_pct"]
            print(f"  {label:<11} {name:<17} {a:6.2f}%   {'MEETS' if a >= TARGET else 'below'} target")
    print("=" * 60)

    # Step 3: refit on all data and forecast the future.
    final_forecast(yo, Xall)
    print(f"\nDone. Results saved in {OUT}/")