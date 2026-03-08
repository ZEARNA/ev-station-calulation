import hashlib
import streamlit as st
from database import SessionLocal, UserDB


def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()


def login_screen():

    st.title("EV Station Calculation Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        db = SessionLocal()

        user = (
            db.query(UserDB)
            .filter(
                UserDB.username == username,
                UserDB.password == hash_password(password),
            )
            .first()
        )

        db.close()

        if user:
            st.session_state.user = username
            st.session_state.role = user.role
            st.rerun()
        else:
            st.error("Invalid login")
