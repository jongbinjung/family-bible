import streamlit as st
import polars as pl
from src.processors import filter_progress

from src import strings
from src.users import (
    get_viewables_progress,
    get_user_details,
    get_active_user_progress,
    get_active_user_details,
    get_active_lang,
)
from src import data
from src import configs
from src.models import Keys, Role


def login_screen():
    lang = st.session_state[Keys.LANGUAGE]
    st.button(
        strings.login[lang],
        icon=":material/login:",
        on_click=st.login,
        width="stretch",
        type="primary",
    )


def admin_panel():
    if st.session_state[Keys.CURRENT_USER_DETAILS].role != Role.ADMIN:
        return
    with st.expander("Admin Panel", expanded=False):
        st.write("This is the admin panel. Only admins can see this section.")

        st.selectbox(
            label="Impersonate User",
            key=Keys.IMPERSONATING_USER_EMAIL,
            options=data.load_members_data()["email"].sort().to_list(),
            index=None,
        )

        if st.session_state[Keys.IMPERSONATING_USER_EMAIL] is None:
            st.write("Not impersonating anyone.")
            st.session_state[Keys.IMPERSONATED_USER_DETAILS] = st.session_state[
                Keys.CURRENT_USER_DETAILS
            ]
        else:
            st.write(
                f"Impersonating user: {st.session_state[Keys.IMPERSONATING_USER_EMAIL]}"
            )
            st.session_state[Keys.IMPERSONATED_USER_DETAILS] = get_user_details(
                st.session_state[Keys.IMPERSONATING_USER_EMAIL]
            )


def init():
    """Initialization step that must run right after login to set states"""
    lang = st.session_state[Keys.LANGUAGE]
    if Keys.CURRENT_USER_DETAILS not in st.session_state:
        st.session_state[Keys.CURRENT_USER_DETAILS] = get_user_details(st.user.email)

    st.header(strings.welcome_pattern[lang].format(st.user.name))

    admin_panel()

    lang = get_active_lang()

    st.button(
        strings.logout[lang],
        icon=":material/logout:",
        on_click=st.logout,
        type="secondary",
        width="stretch",
    )


def aggregate_progress():
    lang = get_active_lang()

    st.header(strings.leaderboard[lang])

    progress_df = get_viewables_progress(get_active_user_details())

    progress_df.group_by("name").agg(
        pl.col("completed").sum().alias("completed_count"),
        pl.col("plan_id").unique().count().alias("total_count"),
    ).select(
        "name",
        pl.format("{}/{}", pl.col("completed_count"), pl.col("total_count")).alias(
            "progress_text"
        ),
        (pl.col("completed_count") / pl.col("total_count")).alias("progress"),
    ).sort(["progress", "name"], descending=[True, False]).pipe(
        st.dataframe,
        column_config={
            "name": st.column_config.TextColumn(
                label=strings.name[lang],
                width="small",
            ),
            "progress_text": st.column_config.TextColumn(
                label=strings.days[lang],
                width="small",
            ),
            "progress": st.column_config.ProgressColumn(
                label="Progress",
                format="percent",
            ),
        },
    )
    st.caption(strings.update_delay_notice[lang])


def my_progress():
    lang = get_active_lang()
    st.header(strings.my_progress[lang])

    st.write(f"`{get_active_user_details().email}`")
    progress_df = get_active_user_progress()

    edited_progress_df = st.data_editor(
        filter_progress(progress_df),
        column_config={
            "plan_id": None,
            "date_us": st.column_config.DateColumn(
                label="Date (US)",
                format="M/D (ddd)",
                width="small",
            ),
            "date_kr": st.column_config.DateColumn(
                label="Date (KR)",
                format="M/D (ddd)",
                width="small",
            ),
            "plan": st.column_config.TextColumn(label=strings.plan[lang]),
            "completed": st.column_config.CheckboxColumn(label=strings.read[lang]),
        },
        disabled=["plan_id", "date_us", "date_kr", "plan"],
        key=Keys.ACTIVE_USER_PROGRESS,
        num_rows="fixed",
        row_height=42,
    )

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
