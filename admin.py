import streamlit as st
from database import SessionLocal, UserDB
from auth import hash_password


def admin_panel():

    st.header("Admin Management")

    db = SessionLocal()

    tab1 = st.tabs(["Create User"])[0]

    # =====================
    # CREATE USER
    # =====================

    with tab1:

        st.subheader("Create User")

        username = st.text_input("Username")

        password = st.text_input("Password", type="password")

        role = st.selectbox("Role", ["user", "admin"])

        if st.button("Create User"):

            user = UserDB(
                username=username,
                password=hash_password(password),
                role=role,
            )

            db.add(user)
            db.commit()

            st.success("User created")

    db.close()
