import streamlit as st

from auth import login_screen
from dashboard import user_dashboard
from admin import admin_panel
from chargers import charger_data_page
from database import init_db


# =========================
# INITIALIZE DATABASE
# =========================

init_db()


def main():

    # =========================
    # LOGIN CHECK
    # =========================

    if "user" not in st.session_state:
        login_screen()
        return

    # =========================
    # SIDEBAR USER INFO
    # =========================

    st.sidebar.write(f"User: {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    # =========================
    # SIDEBAR MENU
    # =========================

    if st.session_state.role == "admin":

        st.sidebar.markdown("### Admin Menu")

        if st.sidebar.button("ROI Calculator"):
            st.session_state.page = "roi"

        if st.sidebar.button("Charger Database"):
            st.session_state.page = "chargers"

        if st.sidebar.button("Admin Management"):
            st.session_state.page = "admin"

    else:

        st.sidebar.markdown("### User Menu")

        if st.sidebar.button("ROI Calculator"):
            st.session_state.page = "roi"

        if st.sidebar.button("Database"):
            st.session_state.page = "database"

    # =========================
    # DEFAULT PAGE
    # =========================

    if "page" not in st.session_state:
        st.session_state.page = "roi"

    # =========================
    # PAGE ROUTER
    # =========================

    if st.session_state.page == "roi":
        user_dashboard()

    elif st.session_state.page == "database":
    charger_data_page()

    elif st.session_state.page == "admin":
        admin_panel()


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    main()
