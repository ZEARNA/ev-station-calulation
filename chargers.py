import streamlit as st
import pandas as pd
from database import SessionLocal, ChargerDB


def charger_data_page():

    st.header("Charger Database")

    db = SessionLocal()

    chargers = db.query(ChargerDB).all()

    # -----------------------
    # SHOW TABLE
    # -----------------------

    data = []

    for c in chargers:
        data.append(
            {
                "Name": c.name,
                "Type": c.type,
                "Power kW": c.power_kw,
                "Current A": c.current,
                "Price": c.price,
                "Dispenser": c.dispenser_price,
            }
        )

    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

    # -----------------------
    # ADMIN ONLY
    # -----------------------

    if st.session_state.role != "admin":
        db.close()
        return

    st.divider()

    # -----------------------
    # ADD CHARGER
    # -----------------------

    st.subheader("Add Charger")

    name = st.text_input("Name")
    ctype = st.selectbox("Type", ["Standalone", "Split"])
    power = st.number_input("Power kW", value=120)
    current = st.number_input("Current A", value=200)
    price = st.number_input("Price", value=500000)
    dispenser = st.number_input("Dispenser Price", value=300000)

    if st.button("Add Charger"):

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

        st.success("Charger added")

        st.rerun()

    st.divider()

    # -----------------------
    # EDIT / DELETE
    # -----------------------

    st.subheader("Edit / Delete Charger")

    chargers = db.query(ChargerDB).all()

    if len(chargers) > 0:

        names = [c.name for c in chargers]

        selected = st.selectbox("Select Charger", names)

        charger = next(c for c in chargers if c.name == selected)

        new_price = st.number_input(
            "Edit Price", value=float(charger.price)
        )

        if st.button("Update Charger"):

            charger.price = new_price
            db.commit()

            st.success("Updated")

        if st.button("Delete Charger"):

            db.delete(charger)
            db.commit()

            st.success("Deleted")

            st.rerun()

    db.close()
