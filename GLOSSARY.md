# Glossary

A plain-English reference for the technical terms used in
`Solar_PV_Forecasting.ipynb` (the combined final notebook). Skim this if anything
in the notebook reads as acronym-heavy — most entries are one or two sentences.
Section numbers (§1–§15) refer to the notebook's sections.

Grouped by topic for browsability; alphabetical within each group.

---

## Solar PV physics & instrumentation

**AC power (`ac_power_kw`)** — Alternating-current electrical output of the
solar inverter, measured in kilowatts. The *target variable* this notebook
is trying to predict.

**AOI — Angle of Incidence** — The angle between the sun's rays and the
direction the solar panel is pointing. At AOI = 0° the sun is hitting the
panel face-on (maximum power); at 90° the sun is grazing the panel surface
(no power). Computed in §4 from sun position + panel tilt/azimuth.

**Array** — A collection of PV panels wired together. The NIST Ground-1
array is rated 270.7 kW.

**Azimuth** — Compass direction the panels face. South-facing (180°) is
optimal in the Northern Hemisphere.

**Capacity / nameplate** — The maximum rated power output of a PV system
under standard test conditions (1000 W/m² irradiance, 25 °C cell temp).
For System 4902, capacity = 270.7 kW; for the Colorado System 1332, 1,153 kW.

**Clear-sky POA (`clear_sky_poa`)** — A *modeled* value of what POA
irradiance *would be* if the sky were perfectly clear, computed from
sun position and atmospheric turbidity (Ineichen model in §4).
Acts as the physical ceiling for measured POA.

**Clear-sky index (`clear_sky_index`)** — Ratio `measured POA / clear-sky POA`.
Equals 1.0 when the sky is empty, drops toward 0 under heavy cloud cover.
A direct quantification of cloud-driven irradiance attenuation.

**DC power (`dc_power_kw`)** — Direct-current power produced by the panels
*before* the inverter converts it to AC. Always ≥ AC power (inverter
efficiency loss, typically ~5%). Dropped from the model as target leakage.

**DHI — Diffuse Horizontal Irradiance** — Sunlight that has been scattered
by the atmosphere and arrives at a horizontal surface from all sky directions.
Dominates on overcast days.

**DNI — Direct Normal Irradiance** — Sunlight arriving in a straight beam
from the sun, measured on a surface perpendicular to that beam. Dominates
on clear days.

**Fixed-tilt array** — Panels mounted at a permanent tilt angle (no tracking).
The NIST Ground-1 array is fixed at 20° tilt facing south.

**GHI — Global Horizontal Irradiance** — Total solar irradiance reaching
a horizontal surface (DHI + DNI × cos(zenith angle)). The standard "how sunny
is it?" measurement.

**IAM — Incidence Angle Modifier** — Correction factor accounting for
reflection losses when sunlight hits the panel at an oblique angle (high AOI).
Related to the AOI feature; not modeled directly here.

**Inverter** — Electronic device that converts DC power from the panels into
grid-compatible AC power. Introduces ~5% conversion loss.

**Irradiance** — Solar power per unit area, measured in W/m². The fundamental
input to PV power production.

**Module** — A single PV panel. Modules are wired together into arrays.

**Module temperature (`temp_module_c`)** — Surface temperature of the panel
itself. Always ≥ ambient when the panel is producing (panels heat up under
sun). PV efficiency drops ~0.4 % per °C above the 25 °C reference.

**POA — Plane-of-Array irradiance (`poa_irradiance_wm2`)** — Solar irradiance
hitting the *tilted panel surface*, not the horizontal ground. The most
directly relevant irradiance measurement for PV output, and (per §8) the
single most valuable input when available. Measured by pyranometers mounted
in the plane of the panels.

**Pyranometer** — Instrument that measures broadband solar irradiance
(W/m²) at the location it's mounted. The NIST site uses two redundant
POA pyranometers; we average them during cleaning in §1.

**PV — Photovoltaic** — Technology that converts sunlight directly into
electricity. The system this notebook forecasts.

**Solar elevation** — Angle of the sun above the horizon, in degrees.
0° = on the horizon (sunrise/sunset), 90° = directly overhead.

**Solar zenith** — Angle between straight up and the sun, the complement
of elevation (zenith = 90° − elevation).

**Tilt** — Angle of the panels relative to horizontal ground.
NIST Ground-1 tilt = 20°.

---

## Time series & statistics

**Cyclical encoding** — Using sin/cos transformations of time (e.g., hour,
day-of-year) so that the model treats 23:00 and 00:00 as adjacent rather
than as the most-distant points on a number line. Used in §4.

**Diurnal** — "Daily-cycle" — the regular within-day variation in a quantity.
Solar PV is overwhelmingly diurnal (see the decomposition in §2).

**Forward-fill (`ffill`)** — Imputation method that propagates the last
known value forward. Used in §1 to project hourly Open-Meteo data onto
the 15-min PVDAQ cadence.

**Interpolation** — Estimating a missing value from its neighbors.
Linear time-interpolation in §1 fills small sensor gaps (train-side only,
to avoid leakage).

**Lag** — A time offset. "Lag 24 (hours)" means "the value 24 hours ago".
Lagged production values are the extra inputs tested in the forecasting
study (§12).

**MAPE — Mean Absolute Percentage Error** — Average percentage error
between predicted and actual. Reported on daytime samples (AC > 10 kW) to
avoid divide-by-zero at night; defined in the scoring helper in §5.

**MAE — Mean Absolute Error** — Average of the absolute gaps between
predicted and actual, in the original units (kW).

**Pearson r** — Correlation coefficient between two variables, ranging
−1 (perfect inverse) through 0 (uncorrelated) to +1 (perfect positive).
POA vs AC power has r ≈ 0.98 (§2).

**R² — Coefficient of Determination** — Fraction of the variance in the
target that the model explains. R² = 1 is a perfect fit; R² = 0 means
the model is no better than predicting the mean.

**Residual** — The gap between the observed value and the model's
prediction (`actual − predicted`). Squared and averaged, residuals form
the RMSE.

**RMSE — Root-Mean-Square Error** — Square-root of the mean squared
residual, in the same units as the target (kW). Penalizes large errors
more than small ones; the *primary* evaluation metric (§5, §9).

**Seasonal decomposition** — Splitting a time series into trend +
seasonal + residual components. Used in §2 with a 24-hour period to
isolate the diurnal cycle from the multi-day weather envelope.

**Stochastic** — Random / probabilistic — governed by a probability
distribution rather than fully determined by inputs. Cloud cover, wind,
and short-term temperature swings are stochastic outputs of weather, so
the irradiance and panel temperature that drive PV power inherit that
randomness — the reason a *regularized* model is appropriate.

**Trend** — The slow-varying component of a time series — in the §2
decomposition, the multi-day weather regime that remains after removing
the daily cycle.

---

## Machine learning models & evaluation

**Ablation** — Removing a feature (or set of features) from a model to
measure how much it contributed. §5 compares the model *with* the on-site
sensors (incl. measured POA) against the no-on-site-sensor feature set.

**Baseline** — A simple model used as a comparison point for more complex
models. Ridge in §5 is the linear baseline the tree/neural models must beat.

**Capacity factor** — A site's power output divided by its rated nameplate
capacity, giving a unit-free number in [0, 1]. Used in §11 so a model trained
on the 270.7 kW Maryland array can be applied to the 1,153 kW Colorado array
on the same scale.

**Coefficient (Ridge)** — The weight assigned to each feature by the
regression. After standardization, the magnitude of the coefficient is
directly comparable across features (the interpretation chart in §8).

**Cross-validation (TimeSeriesSplit)** — Repeatedly training on an
expanding window of past data and validating on the immediately
following block, instead of random folds. Avoids leakage in time-series
problems. Used in the model comparison (§5) and tuning (§6).

**Feature** — A predictor variable input to the model. The notebook uses two
feature sets: a 14-feature **FULL** set (with on-site sensors incl. measured
POA) and an 18-feature **FORECAST** set (deterministic geometry/time + weather
proxies, no on-site sensors) — see §4.

**Holdout** — The portion of the data reserved exclusively for final
evaluation, never used during training. Here the test set = the most
recent 20 % of the timeline (§3).

**Hyperparameter** — A model setting chosen by the practitioner (vs
learned from data), e.g. Ridge's regularization strength `alpha`, or
XGBoost's tree depth and learning rate (tuned in §6).

**Lasso** — Linear regression using L1 regularization, which drives some
coefficients exactly to zero (automatic feature selection). One of the models
compared in §5 (≈ Ridge on this feature set).

**Leakage** — When a model accidentally gets information about the answer
through its features, inflating evaluation scores. Avoided here by excluding
`dc_power_kw` and (in the nowcast) any lag/rolling stats of the target; in the
forecast study (§12) lags are shifted by ≥ the horizon so no future leaks.

**LSTM — Long Short-Term Memory** — A type of recurrent neural network
designed to handle sequences. Used as the neural arm of the model comparison
in §5 (24-step / 6-hour lookback).

**Nowcast vs forecast** — Nowcast: predict the present from current
information. Forecast: predict a future horizon. The §5 models are same-time
nowcasts; §12 builds genuine H = 1 / 6 / 24 h forecasts.

**Optical flow** — A computer-vision technique that estimates how pixels move
between consecutive frames. Proposed in §13 to derive cloud speed/direction
from a sky camera (research question c).

**Optuna** — A Bayesian hyperparameter-optimization library that searches
parameter space efficiently (TPE sampler). Used in §6 to tune XGBoost against
a time-series cross-validation objective (cross-checked there against grid
search).

**Grid search (`GridSearchCV`)** — Exhaustively evaluating every combination in
a predefined hyperparameter grid. Used in §6 alongside Optuna; the two agree on
near-identical performance.

**Pipeline** — Sequence of preprocessing + modeling steps applied
together. Here, e.g.: `StandardScaler` (fit on train) → `Ridge`.

**Random Forest** — Ensemble model averaging many decision trees. Compared in
§5 as a non-linear model (≈ +21 % RMSE vs Ridge on the forecast feature set).

**Regularization** — Penalty added to the loss function to prevent
overfitting. Ridge uses L2 (sum of squared coefficients); Lasso uses L1.

**Ridge regression** — Linear regression with L2 regularization. Robust
to correlated predictors, which are common in this feature set. The linear
baseline in §5.

**SHAP — SHapley Additive exPlanations** — A model-agnostic method that
attributes each prediction to its input features using cooperative-game theory,
giving a consistent, interaction-aware feature-importance ranking. Used in §8
to explain the winning XGBoost and answer research question (b).

**StandardScaler** — Subtracts the mean and divides by the std-dev so
each feature has mean 0 and variance 1. Needed for the linear models and the
LSTM so the penalty/optimizer treat features fairly. Fit on train only.

**Train / test split** — Partitioning the data so the model learns from
one slice (train) and is evaluated on a never-seen slice (test).
Time-series split: train = older 80 %, test = newer 20 % (§3).

**XGBoost — eXtreme Gradient Boosting** — Tree-based ensemble that
sequentially fits trees to the residuals of the previous tree. The winning
model (§5, tuned in §6 to R² 0.815 → 0.891); also used for the cross-site
(§11) and H-step forecast (§12) experiments, and saved in §10.

**Zero-shot transfer** — Applying a model trained on one dataset directly to a
new, unseen dataset with no retraining. §11 shows the 4902-trained
capacity-factor model transfers zero-shot to System 1332 with no accuracy
penalty.

---

## Data sources & weather forecasting

**ERA5** — ECMWF's global atmospheric *reanalysis* — a best estimate of
historical weather computed by re-running NWP models with all observations
that were available after the fact. Higher quality than real-time forecast,
since it's hindsight. Used by Open-Meteo to power its historical API.

**Forecast skill (or just "skill")** — Predictive accuracy of a model,
typically relative to a reference baseline. Here, the drop from the
full-sensor model (R² 0.977) to the no-on-site-sensor model (R² 0.815) in §5
quantifies how much skill is lost when sensors are replaced by weather proxies.

**HRRR — High-Resolution Rapid Refresh** — NOAA's 3 km operational NWP
model over CONUS, updated hourly. Listed in §14 as a follow-on candidate for
NWP-quality cloud cover (vs reanalysis).

**NIST Ground-1** — Reference name for PVDAQ System 4902. Located on
the NIST Gaithersburg, MD campus.

**NREL — National Renewable Energy Laboratory** — U.S. Department of
Energy lab that hosts PVDAQ and NSRDB.

**NSRDB — National Solar Radiation Database** — NREL's authoritative
satellite-derived irradiance + weather dataset for U.S. sites. Its current
PSM4 GOES CONUS endpoint covers 2018+ only, which is why this project uses
Open-Meteo / ERA5 for the 2014–2017 PVDAQ window.

**NWP — Numerical Weather Prediction** — Physics-based atmospheric
modeling that produces forecasts (e.g., GFS, HRRR). The "available
at deployment time" baseline of weather information.

**Open-Meteo** — Free, no-key-required weather API. Backed by ERA5 reanalysis
for historical data. Supplies the cloud cover, GHI/DNI/DHI, temperature, wind,
humidity, and surface pressure used as the no-on-site-sensor weather proxies
(§1 loading, §5 modeling).

**PSM4** — The current NSRDB v4 endpoint (GOES satellite-derived).
CONUS variant covers 2018+; earlier years require legacy products that
NREL has since deprecated.

**PVDAQ — Photovoltaic Data Acquisition** — NREL's public archive of
high-cadence PV plant performance data. Source of both the
`nist_ground_4902_15min.parquet` (Maryland) and System 1332 (Colorado) files.

**Reanalysis** — A "best estimate" of historical weather produced by
running an NWP model with all observations that eventually became available,
including those that arrived after real-time. ERA5 is a reanalysis — higher
quality than the real-time forecast it would have produced at the time
(so the reported skill is an optimistic upper bound for live deployment).

---

## Notebook tools & methodology

**CRISP-DM — Cross-Industry Standard Process for Data Mining** — A six-phase
data-mining methodology (Business Understanding → Data Understanding → Data
Preparation → Modeling → Evaluation → Deployment). This notebook follows the
same flow: load → clean → explore → engineer → model → evaluate → save.

**Jupyter notebook (`.ipynb`)** — Interactive document mixing markdown
text, executable code cells, and rendered output (plots, tables).
The format used for this entire submission.

**joblib** — Python library for efficient serialization of large
numpy-backed objects. Used in §10 (alongside `pickle`) to save the model.

**Matplotlib** — Foundational Python plotting library. All static plots
in the notebook.

**NumPy** — Core Python numerical / array library. Underpins everything.

**pandas** — Tabular data manipulation library; the notebook's primary
data structure is the `pandas.DataFrame`.

**Parquet** — Compressed columnar file format (`*.parquet`). Used for
the PVDAQ and Open-Meteo caches because it loads ~5× faster than CSV at
~1/8 the file size.

**pickle** — Python's built-in object-serialization format. Used in §10 to
save the trained model bundle; reloaded and verified in the same section.

**pvlib** — Open-source Python library for solar-energy modeling.
Used in §4 to compute solar position, AOI, and clear-sky POA.

**scikit-learn** — Python machine-learning library. Provides Ridge, Lasso,
Random Forest, StandardScaler, TimeSeriesSplit/GridSearchCV, and the metric
functions used across §5–§9.

**Seaborn** — Statistical-plotting library built on Matplotlib.
Used for the §2 correlation heatmap and distribution plots.

**statsmodels** — Python statistical-modeling library. Provides
`seasonal_decompose`, used for the time-series decomposition in §2.

**TensorFlow / Keras** — Deep-learning framework used to build and train the
LSTM in §5. Imported first in the setup cell to avoid a macOS threading
deadlock, and run single-threaded with op-determinism for reproducibility.

**XGBoost (library)** — Gradient-boosted-tree library providing the winning
model; see the *XGBoost* entry above.
