"""Functions for data operations"""

from st_files_connection import FilesConnection
import streamlit as st
import polars as pl
from src.paths import (
    MEMBERS_GCS_PATH,
    VIEWABLES_GCS_PATH,
    PLAN_GCS_PATH,
    PROGRESS_GCS_PATTERN,
)

MINUTE_SECONDS = 60  # 1 minute
HOUR_SECONDS = 60 * MINUTE_SECONDS  # 1 hour
DAY_SECONDS = 24 * HOUR_SECONDS  # 24 hours
WEEK_SECONDS = 7 * DAY_SECONDS


@st.cache_data(ttl=DAY_SECONDS)
def load_members_data() -> pl.DataFrame:
    """Load members data"""
    conn = st.connection("gcs", type=FilesConnection)
    pandas_df = conn.read(
        f"gcs://{MEMBERS_GCS_PATH}",
        input_format="parquet",
        ttl=DAY_SECONDS,
    )
    return pl.from_pandas(pandas_df)


@st.cache_data(ttl=HOUR_SECONDS)
def load_viewables_data() -> pl.DataFrame:
    """Load viewables data

    Returns:
        pl.DataFrame: DataFrame with rows for each member,
            name: str
            viewable_groups: list[Group]

    """
    conn = st.connection("gcs", type=FilesConnection)
    pandas_df = conn.read(
        f"gcs://{VIEWABLES_GCS_PATH}",
        input_format="parquet",
        ttl=HOUR_SECONDS,
    )
    return (
        pl.from_pandas(pandas_df)
        .unique()
        .group_by("name")
        .agg(pl.col("group").alias("viewable_groups"))
    )


@st.cache_data(ttl=WEEK_SECONDS)
def load_plan_data() -> pl.DataFrame:
    """Load plan data

    Returns:
        pl.DataFrame: DataFrame with columns
            id: int
            date_us: date
            date_kr: date
            plan_en: str
            plan_ko: str

    """
    conn = st.connection("gcs", type=FilesConnection)
    pandas_df = conn.read(
        f"gcs://{PLAN_GCS_PATH}",
        input_format="parquet",
        ttl=HOUR_SECONDS,
    )
    return pl.from_pandas(pandas_df).with_columns(
        pl.col("date_us").cast(pl.Date),
        pl.col("date_kr").cast(pl.Date),
    )


@st.cache_data(ttl=MINUTE_SECONDS)
def load_progress_data(username: str) -> pl.DataFrame:
    """Load progress data for a given user

    Args:
        username (str): username of the user

    Returns:
        pl.DataFrame: DataFrame with columns
            plan_id: int; FK to plan
            completed: bool

    """
    conn = st.connection("gcs", type=FilesConnection)
    pandas_df = conn.read(
        f"gcs://{PROGRESS_GCS_PATTERN.format(username)}",
        input_format="parquet",
        ttl=MINUTE_SECONDS,
    )
    return pl.from_pandas(pandas_df)


def update_progress_data(username: str, df: pl.DataFrame):
    """Overwrite existing progress data for a given user

    Args:
        username (str): username of the user
        df (pl.DataFrame): DataFrame with columns
            plan_id: int; FK to plan
            completed: bool

    """
    path = PROGRESS_GCS_PATTERN.format(username)
    conn = st.connection("gcs", type=FilesConnection)
    with conn.open(path, "wb") as f:
        df.write_parquet(f)


def uncached_progress(username: str) -> pl.DataFrame:
    """Load progress data for a given user

    Args:
        username (str): username of the user

    Returns:
        pl.DataFrame: DataFrame with columns
            plan_id: int; FK to plan
            completed: bool

    """
    conn = st.connection("gcs", type=FilesConnection)
    pandas_df = conn.read(
        f"gcs://{PROGRESS_GCS_PATTERN.format(username)}",
        input_format="parquet",
        ttl=0,
    )
    return pl.from_pandas(pandas_df)
