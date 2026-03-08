import streamlit as st
from database import SessionLocal, ChargerDB, UserDB
from auth import hash_password


def admin_panel():

    st.header("Admin Panel")

    db = SessionLocal()

    tab1, tab2 = st.tabs(["Create User", "Create Charger"])

    with tab1:

        u = st.text_input("Username")
        p = st.text_input("Password")
        role = st.selectbox("Role", ["user", "admin"])

        if st.button("Create User"):

            user = UserDB(
                username=u,
                password=hash_password(p),
                role=role,
            )

            db.add(user)
            db.commit()

            st.success("User created")

    with tab2:

        name = st.text_input("Name")

        power = st.number_input("Power kW")

        price = st.number_input("Price")

        if st.button("Create Charger"):

            c = ChargerDB(
                name=name,
                power_kw=power,
                price=price,
            )

            db.add(c)
            db.commit()

            st.success("Charger created")

    db.close()
