# Data Sources

## Primary — NREL PVDAQ System 4902 (NIST Ground-1)

- **Location:** Gaithersburg, MD — 39.1319°N, −77.2141°W, 138 m elevation
- **System:** 270.7 kW fixed ground-mount PV array
- **Cadence / span:** 15-minute, July 2014 → March 2018 (~112,000 rows)
- **Channels:** AC / DC power, dual-redundant POA irradiance, ambient and module temperature, wind
- **License:** Public, Creative Commons via NREL PVDAQ on AWS S3
- **Local file:** `data/nist_ground_4902_15min.parquet`

### Where it lives

| Source | URL |
|---|---|
| OEDI submission page (canonical) | https://data.openei.org/submissions/4568 |
| AWS S3 bucket (raw, partitioned by system_id/year/month/day) | `s3://oedi-data-lake/pvdaq/` |
| Systems metadata index | https://oedi-data-lake.s3.amazonaws.com/pvdaq/csv/systems.csv |
| DOE Data Explorer record | https://www.osti.gov/dataexplorer/biblio/1846021-photovoltaic-data-acquisition-pvdaq-public-datasets |
| OSTI biblio record | https://www.osti.gov/biblio/1846021 |
| data.gov mirror | https://catalog.data.gov/dataset/photovoltaic-data-acquisition-pvdaq-public-datasets |
| openEDI PVDAQ documentation | https://github.com/openEDI/documentation/blob/main/pvdaq.md |
| PVDAQ v3 API docs | https://developer.nrel.gov/docs/solar/pvdaq-v3/ |

### Sister systems at the NIST Gaithersburg site

- **4901** — NIST_Canopy_1
- **4902** — NIST_Ground_1 *(this dataset)*
- **4903** — NIST_Roof_1

Raw data reported at 15-minute increments in ISO 8601, partitioned by `system_id / year / month / day`.

---

## Secondary — Open-Meteo reanalysis (co-located)

- **Local file:** `data/openmeteo_nist_4902_hourly.parquet`
- **Cadence:** hourly, co-located to the NIST Ground-1 coordinates above
- **Source:** Open-Meteo Historical Weather API — https://open-meteo.com/en/docs/historical-weather-api
- **License:** CC BY 4.0 — https://creativecommons.org/licenses/by/4.0/
- **Attribution:** Weather data by Open-Meteo.com — https://open-meteo.com/
- **Open-Meteo licence page:** https://open-meteo.com/en/licence
- **Project modifications:** cached locally, renamed fields with an `om_`
  prefix, and forward-filled hourly values onto the 15-min PVDAQ index.

---

## Cross-site (Final Report §F2) — NREL PVDAQ System 1332 (NREL Parking Garage)

- **Location:** Golden, CO — 39.7388°N, −105.1732°W, 1,770 m elevation
- **System:** 1,153 kW parking-garage canopy PV array; **power output only, no
  on-site weather sensors** — the no-on-site-sensor deployment scenario
- **Cadence / span fetched:** native 15-second, resampled to 15-minute mean;
  calendar year 2017 (~34,000 rows)
- **Target channel:** `metered_ac_power__2638` (site meter, kW)
- **License:** Public, Creative Commons via NREL PVDAQ on AWS S3
- **Local file:** `data/pvdaq_1332_15min.parquet`
- **Fetch:** `python scripts/reproduce.py fetch-crosssite` (public OEDI S3, no key)
- **Source:** `s3://oedi-data-lake/pvdaq/csv/pvdata/system_id=1332/`

### Co-located weather — Open-Meteo reanalysis (Golden, CO)

- **Local file:** `data/openmeteo_1332_hourly.parquet`
- **Cadence:** hourly, co-located to the System 1332 coordinates above,
  shifted to Mountain standard time (UTC−7) to match PVDAQ convention
- **Source / license:** Open-Meteo Historical Weather API, CC BY 4.0 (as above);
  attribution: Weather data by Open-Meteo.com
