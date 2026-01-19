import polars as pl
from src.models import Keys
import streamlit as st
import pendulum
from src import configs, data
from src.users import get_active_user_details
from src.configs import MAX_FUTURE_WEEKS


def filter_progress(df: pl.DataFrame) -> pl.DataFrame:
    """Filter progress data to just the entries to show in the user's progress."""
    past_days = 1
    if st.session_state.get(Keys.SHOW_COMPLETED, False):
        past_days = 14
    return df.filter(
        (pl.col("date_us") >= pendulum.now().subtract(days=past_days).date())
        | ~pl.col("completed")
    ).filter(pl.col("date_us") <= pendulum.now().add(weeks=MAX_FUTURE_WEEKS).date())


def build_new_progress_df(progress_df: pl.DataFrame) -> pl.DataFrame:
    """Build a new progress DataFrame from the plan DataFrame."""

    edited_rows = st.session_state[Keys.ACTIVE_USER_PROGRESS].get("edited_rows", dict())
    edited_progress_pd = filter_progress(progress_df).to_pandas()

    for row_idx, changes in edited_rows.items():
        for col, new_value in changes.items():
            edited_progress_pd.at[row_idx, col] = new_value

    edited_progress_df = pl.from_pandas(edited_progress_pd)

    updated_user_progress_df = (
        pl.concat(
            [
                progress_df.join(edited_progress_df, how="anti", on="plan_id").select(
                    "plan_id", "completed"
                ),
                edited_progress_df.filter(pl.col("completed")).select(
                    "plan_id", "completed"
                ),
            ]
        )
        .filter(pl.col("completed"))
        .sort("plan_id")
    )

    if configs.DEBUG:
        st.write("Updated value:", updated_user_progress_df)

    data.update_progress_data(
        get_active_user_details().username,
        updated_user_progress_df,
    )

    if configs.DEBUG:
        st.write(
            "Live value:", data.uncached_progress(get_active_user_details().username)
        )
