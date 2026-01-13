import polars as pl
import pendulum


def filter_progress(df: pl.DataFrame) -> pl.DataFrame:
    """Filter progress data to just the entries to show in the user's progress."""
    return df.filter(
        (pl.col("date_us") >= pendulum.now().date()) | ~pl.col("completed")
    ).filter(pl.col("date_us") <= pendulum.now().add(weeks=1).date())
