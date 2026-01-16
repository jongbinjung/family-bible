"""Functions for dealing with users"""

from src import data
import streamlit as st
import polars as pl
from src.models import Role, UserDetails, Group, Language, Keys
from src import strings


@st.cache_data(ttl=3600)
def get_user_details(email: str) -> UserDetails:
    """Get the role of a user based on their email"""
    members_df = data.load_members_data()
    viewables_df = data.load_viewables_data()
    user_records = (
        members_df.filter(pl.col("email") == email)
        .join(viewables_df, on="name", how="left")
        .to_dicts()
    )
    if len(user_records) == 0:
        raise RuntimeError(f"User {email} unknown!")
    if len(user_records) > 1:
        raise RuntimeError(f"More than one user {email} found!")
    user_record = user_records[0]

    viewable_groups = [Group(g) for g in user_record["viewable_groups"] if g in Group]

    return UserDetails(
        username=user_record["name"],
        email=user_record["email"],
        role=Role(user_record["role"]),
        group=Group(user_record["group"]),
        language=Language(user_record["lang"]),
        viewables=viewable_groups,
    )


def get_active_user_details() -> UserDetails:
    """Get the details of the currently active user

    For admin users, this could be an impersonated user

    """
    try:
        return st.session_state[Keys.IMPERSONATED_USER_DETAILS]
    except KeyError:
        return st.session_state[Keys.CURRENT_USER_DETAILS]


def get_active_lang() -> Language:
    """Get the language of the currently active user"""
    return get_active_user_details().language


def get_active_user_progress() -> pl.DataFrame:
    """Get progress for active user"""
    # Read from data sources
    active_user = get_active_user_details()
    plan_df = data.load_plan_data()
    progress_df = data.uncached_progress(username=active_user.username)

    plan_col = f"plan_{active_user.language.value.lower()}"

    return plan_df.join(
        progress_df,
        left_on="id",
        right_on="plan_id",
        how="left",
    ).select(
        pl.col("id").alias("plan_id"),
        pl.col("date_us"),
        pl.col("date_kr"),
        pl.col(plan_col).alias("plan"),
        pl.col("completed").fill_null(False),
    )


def get_viewables_progress(user_details: UserDetails) -> pl.DataFrame:
    """Get progress for viewable groups"""
    viewable_names = (
        data.load_members_data()
        .filter(pl.col("group").is_in(user_details.viewables))
        .select("name")
        .unique()
    )

    plan_df = data.load_plan_data()

    return pl.concat(
        [
            plan_df.join(
                data.load_progress_data(username=name),
                left_on="id",
                right_on="plan_id",
                how="left",
            ).select(
                pl.col("id").alias("plan_id"),
                pl.col("completed").fill_null(False),
                pl.lit(
                    strings.display_name(
                        name=name,
                        lang=user_details.language,
                    )
                ).alias("name"),
            )
            for name in viewable_names["name"]
        ]
    )
