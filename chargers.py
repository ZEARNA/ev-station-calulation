import streamlit as st
import pandas as pd
from database import SessionLocal, ChargerDB


def charger_data_page():

    db = SessionLocal()

    st.header("Charger Database")

    chargers = db.query(ChargerDB).all()

    # ---------------------
    # ADD BUTTON
    # ---------------------

    col1, col2 = st.columns([8,2])

    with col2:
        if st.button("➕ Add Charger"):
            st.session_state.page_mode = "add"
            st.rerun()

    # ---------------------
    # LIST CHARGERS
    # ---------------------

    st.subheader("Chargers")

    for c in chargers:

        if st.button(f"{c.name} | {c.power_kw} kW", key=f"charger_{c.id}"):

            st.session_state.selected_charger = c.id
            st.session_state.page_mode = "edit"
            st.rerun()

    # ---------------------
    # ADD CHARGER PAGE
    # ---------------------

    if st.session_state.get("page_mode") == "add":

        st.divider()
        st.subheader("Add Charger")

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

            st.success("Charger added")

            st.session_state.page_mode = None
            st.rerun()

    # ---------------------
    # EDIT CHARGER PAGE
    # ---------------------

    if st.session_state.get("page_mode") == "edit":

        charger = db.query(ChargerDB).filter(
            ChargerDB.id == st.session_state.selected_charger
        ).first()

        st.divider()
        st.subheader(f"Edit Charger : {charger.name}")

        name = st.text_input("Name", value=charger.name)
        ctype = st.selectbox(
            "Type",
            ["Standalone", "Split"],
            index=0 if charger.type == "Standalone" else 1,
        )
        power = st.number_input("Power kW", value=charger.power_kw)
        current = st.number_input("Current A", value=charger.current)
        price = st.number_input("Price", value=charger.price)
        dispenser = st.number_input(
            "Dispenser Price", value=charger.dispenser_price
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("💾 Update Charger"):

                charger.name = name
                charger.type = ctype
                charger.power_kw = power
                charger.current = current
                charger.price = price
                charger.dispenser_price = dispenser

                db.commit()

                st.success("Updated")

                st.session_state.page_mode = None
                st.rerun()

        with col2:

            if st.button("🗑 Delete Charger"):

                db.delete(charger)
                db.commit()

                st.success("Deleted")

                st.session_state.page_mode = None
                st.rerun()

    db.close()
