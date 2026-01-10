#!/usr/bin/env python3
"""Script to initalize data sources

For some weird permission reasons, this works better if done as a Streamlit app ...

"""

import polars as pl
from src.paths import MEMBERS_GCS_PATH, VIEWABLES_GCS_PATH, PLAN_GCS_PATH


src2dest_mapping = {
    "inputs/members.csv": MEMBERS_GCS_PATH,
    "inputs/viewables.csv": VIEWABLES_GCS_PATH,
    "inputs/2026.csv": PLAN_GCS_PATH,
}


for src, dest in src2dest_mapping.items():
    print(f"Writing {src} to gs://{dest}")
    pl.read_csv(src).write_parquet(f"gs://{dest}")
