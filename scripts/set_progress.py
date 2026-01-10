#!/usr/bin/env python3
"""Script to initalize data sources

For some weird permission reasons, this works better if done as a Streamlit app ...

"""

import polars as pl
from src.paths import PROGRESS_GCS_PATTERN


progress_map = {
    "changkyoon": [1, 2, 3, 4, 5],
    "eunkyoung": [1, 2, 3, 4, 5],
    "hanbyul": [1, 2, 3, 4],
    "hansol": [1, 2, 3],
    "jongbin": [1, 2, 3, 4, 5],
    "lexy": [1, 2, 3],
    "sangwon": [1, 2, 3, 4, 5],
    "sangyoung": [1, 2, 3, 4, 5],
    "seungho": [1, 2, 3, 4, 5, 6],
    "youngshin": [1, 2, 3, 4, 5],
}

for name, progress in progress_map.items():
    _dest = PROGRESS_GCS_PATTERN.format(name)
    print(f"Overwriting gs://{_dest}")
    pl.DataFrame(
        {
            "plan_id": [2026000 + pid for pid in progress],
            "completed": [True] * len(progress),
        }
    ).write_parquet(f"gs://{_dest}")
