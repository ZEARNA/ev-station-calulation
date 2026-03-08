import streamlit as st

from auth import login_screen
from dashboard import user_dashboard
from admin import admin_panel
from chargers import charger_data_page
from database import init_db

init_db()


def main():

    if "user" not in st.session_state:
        login_screen()
        return

    st.sidebar.write(f"User: {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # MENU

    if st.session_state.role == "admin":

        st.sidebar.markdown("### Admin Menu")

        if st.sidebar.button("ROI Calculator"):
            st.session_state.page = "roi"

        if st.sidebar.button("Database"):
            st.session_state.page = "database"

        if st.sidebar.button("Admin Management"):
            st.session_state.page = "admin"

    else:

        st.sidebar.markdown("### User Menu")

        if st.sidebar.button("ROI Calculator"):
            st.session_state.page = "roi"

        if st.sidebar.button("Database"):
            st.session_state.page = "database"

    if "page" not in st.session_state:
        st.session_state.page = "roi"

    # PAGE ROUTER

    if st.session_state.page == "roi":
        user_dashboard()

    elif st.session_state.page == "database":
        charger_data_page()

    elif st.session_state.page == "admin":
        admin_panel()


if __name__ == "__main__":
    main()
