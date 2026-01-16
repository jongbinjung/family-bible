import streamlit as st
from src import strings
import polars as pl
from src.data import load_viewables_data, load_members_data
from src import sections
from src.users import get_active_user_details
from src.models import Keys, Language, Role
from src import configs

st.session_state[Keys.LANGUAGE] = configs.DEFAULT_LANGUAGE

if st.context.locale is not None and st.context.locale.split("-")[0].lower() == "en":
    st.session_state[Keys.LANGUAGE] = Language.EN

title = strings.title[st.session_state[Keys.LANGUAGE]]

st.set_page_config(page_title=title)
st.title(title)


if not st.user.is_logged_in:
    sections.login_screen()
else:
    sections.init()

    sections.my_progress()

    sections.aggregate_progress()

    if st.session_state[Keys.CURRENT_USER_DETAILS].role == Role.ADMIN:
        with st.expander("Debug Info", expanded=False):
            st.write(get_active_user_details())

            members_df = load_members_data()
            viewables_df = load_viewables_data()

            st.write(viewables_df)
            user_record = members_df.filter(pl.col("email") == st.user.email).join(
                viewables_df, on="name", how="left"
            )
