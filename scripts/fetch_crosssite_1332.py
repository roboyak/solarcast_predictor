"""Fetch the cross-site generalization dataset: PVDAQ System 1332 (NREL Parking
Garage, Golden CO) power + Open-Meteo / ERA5 weather for Golden CO.

System 1332 has **power output but no on-site weather sensors** — exactly the
no-on-site-sensor deployment scenario the §F1 forecast model targets, at a
different site (1,153 kW vs 4902's 270.7 kW, 1,770 m elevation, different
climate). This is the cross-site test for the secondary research question
*"can the model generalize across geographic locations?"*.

Power data: public OEDI S3 bucket (no credentials). Daily 15-second CSVs are
downloaded in parallel for the requested year, the metered AC power channel is
kept, and the series is resampled to the 15-minute cadence used by System 4902.

Weather: Open-Meteo Historical (free, no key), same 11 ERA5 fields as 4902,
shifted to local standard time (Mountain, UTC-7) to match PVDAQ convention.

Run::
    python scripts/fetch_crosssite_1332.py            # default year 2017
    python scripts/fetch_crosssite_1332.py 2018
"""
from __future__ import annotations

import io
import sys
import calendar
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import requests

# --- System 1332 metadata (PVDAQ systems.csv) ---
SYS_ID = 1332
LAT, LON, ELEV_M = 39.7388, -105.1732, 1770.0   # Golden, CO
CAPACITY_KW = 1153.0
TZ_OFFSET_HOURS = -7                              # Mountain standard time, no DST
AC_POWER_COL = 'metered_ac_power__2638'           # site meter, kW

REPO_ROOT = Path(__file__).resolve().parent.parent
POWER_OUT = REPO_ROOT / 'data' / 'pvdaq_1332_15min.parquet'
WEATHER_OUT = REPO_ROOT / 'data' / 'openmeteo_1332_hourly.parquet'

S3_BASE = ('https://oedi-data-lake.s3.amazonaws.com/pvdaq/csv/pvdata/'
           f'system_id={SYS_ID}')

OM_HOURLY_VARS = [
    'temperature_2m', 'relative_humidity_2m', 'dew_point_2m',
    'cloud_cover', 'cloud_cover_low', 'cloud_cover_mid', 'cloud_cover_high',
    'shortwave_radiation', 'direct_normal_irradiance', 'diffuse_radiation',
    'direct_radiation', 'windspeed_10m', 'winddirection_10m', 'surface_pressure',
    'precipitation', 'rain', 'snowfall',
]


def _fetch_day(year: int, month: int, day: int) -> pd.DataFrame | None:
    url = (f'{S3_BASE}/year={year}/month={month}/day={day}/'
           f'system_{SYS_ID}__date_{year}_{month:02d}_{day:02d}.csv')
    try:
        with urllib.request.urlopen(url, timeout=60) as r:
            raw = r.read()
    except Exception:
        return None  # missing day — PVDAQ timelines are sparse
    df = pd.read_csv(io.BytesIO(raw), usecols=['measured_on', AC_POWER_COL])
    df['measured_on'] = pd.to_datetime(df['measured_on'])
    df = df.set_index('measured_on').sort_index()
    return df


def fetch_power(year: int) -> pd.DataFrame:
    tasks = [(year, m, d) for m in range(1, 13)
             for d in range(1, calendar.monthrange(year, m)[1] + 1)]
    frames = []
    print(f'[power] downloading {len(tasks)} daily CSVs for {year} (parallel)…',
          flush=True)
    with ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(_fetch_day, *t): t for t in tasks}
        done = 0
        for fut in as_completed(futs):
            df = fut.result()
            done += 1
            if df is not None and len(df):
                frames.append(df)
            if done % 60 == 0:
                print(f'  {done}/{len(tasks)} days fetched, {len(frames)} present',
                      flush=True)
    if not frames:
        raise RuntimeError(f'No System {SYS_ID} data found for {year}')
    combined = pd.concat(frames).sort_index()
    combined = combined[~combined.index.duplicated(keep='first')]
    # 15-second native -> 15-minute mean, matching System 4902 cadence.
    resampled = combined[[AC_POWER_COL]].resample('15min').mean().dropna()
    resampled = resampled.rename(columns={AC_POWER_COL: 'ac_power_kw'})
    resampled['capacity_factor'] = (resampled['ac_power_kw'] / CAPACITY_KW).clip(0, 1.2)
    print(f'[power] {len(resampled):,} 15-min rows  '
          f'{resampled.index.min()} -> {resampled.index.max()}', flush=True)
    return resampled


def fetch_weather(start: str, end: str) -> pd.DataFrame:
    print(f'[weather] Open-Meteo {start} -> {end} for ({LAT}, {LON})…', flush=True)
    params = {
        'latitude': LAT, 'longitude': LON, 'start_date': start, 'end_date': end,
        'hourly': ','.join(OM_HOURLY_VARS), 'timezone': 'UTC',
    }
    r = requests.get('https://archive-api.open-meteo.com/v1/archive',
                     params=params, timeout=180)
    r.raise_for_status()
    df = pd.DataFrame(r.json()['hourly'])
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time').sort_index()
    # UTC -> local standard time (Mountain, UTC-7), matching PVDAQ convention.
    df.index = df.index + pd.Timedelta(hours=TZ_OFFSET_HOURS)
    df.index.name = 'measured_on'
    df = df[~df.index.duplicated(keep='first')]
    print(f'[weather] {len(df):,} hourly rows', flush=True)
    return df


def main() -> int:
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 2017
    POWER_OUT.parent.mkdir(parents=True, exist_ok=True)

    power = fetch_power(year)
    power.to_parquet(POWER_OUT)
    print(f'wrote {POWER_OUT}', flush=True)

    pad_start = (power.index.min() - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    pad_end = (power.index.max() + pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    weather = fetch_weather(pad_start, pad_end)
    weather.to_parquet(WEATHER_OUT)
    print(f'wrote {WEATHER_OUT}', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
