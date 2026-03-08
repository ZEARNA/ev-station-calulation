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

    st.sidebar.write(f"User: {st.session_state.user}")

    if st.sidebar.button("Logout"):
        del st.session_state.user
        del st.session_state.role
        st.rerun()

    if st.session_state.role == "admin":

        page = st.sidebar.radio(
            "Admin Menu",
            ["ROI Calculator", "Admin Management"],
        )

        if page == "Admin Management":
            admin_panel()
        else:
            user_dashboard()

    else:

        user_dashboard()


main()
