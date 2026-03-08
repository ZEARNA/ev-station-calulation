import streamlit as st
from database import SessionLocal, ChargerDB, UserDB
from auth import hash_password


def admin_panel():

    st.header("Admin Management")

    db = SessionLocal()

    tab1, tab2, tab3 = st.tabs(
        ["Create User", "Add Charger", "Edit Chargers"]
    )

    # -----------------
    # CREATE USER
    # -----------------

    with tab1:

        username = st.text_input("Username")
        password = st.text_input("Password")

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

    # -----------------
    # ADD CHARGER
    # -----------------

    with tab2:

        name = st.text_input("Name")

        ctype = st.selectbox("Type", ["Standalone", "Split"])

        power = st.number_input("Power kW", value=120)

        current = st.number_input("Current A", value=200)

        price = st.number_input("Price", value=500000)

        dispenser = st.number_input("Dispenser Price", value=300000)

        if st.button("Save Charger"):

            charger = ChargerDB(
                name=name,
                type=ctype,
                power_kw=power,
                current=current,
                price=price,
                dispenser_price=dispenser,
            )

            db.add(charger)
            db.commit()

            st.success("Charger saved")

    # -----------------
    # EDIT / DELETE
    # -----------------

    with tab3:

        chargers = db.query(ChargerDB).all()

        if len(chargers) > 0:

            names = [c.name for c in chargers]

            selected = st.selectbox("Select Charger", names)

            charger = next(c for c in chargers if c.name == selected)

            new_price = st.number_input(
                "Price", value=float(charger.price)
            )

            if st.button("Update Price"):

                charger.price = new_price
                db.commit()

                st.success("Updated")

            if st.button("Delete Charger"):

                db.delete(charger)
                db.commit()

                st.success("Deleted")

                st.rerun()

    db.close()
