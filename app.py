import streamlit as st

from database import init_db
from auth import login_screen
from admin import admin_panel
from dashboard import user_dashboard

init_db()


def main():

    if "user" not in st.session_state:
        login_screen()
        return

    st.sidebar.write(st.session_state.user)

    if st.session_state.role == "admin":

        page = st.sidebar.selectbox("Menu", ["Dashboard", "Admin"])

        if page == "Admin":
            admin_panel()
        else:
            user_dashboard()

    else:

        user_dashboard()


main()
