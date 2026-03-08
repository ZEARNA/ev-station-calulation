import streamlit as st
from database import SessionLocal, ChargerDB, DispenserDB


def charger_data_page():

    db = SessionLocal()

    st.header("Charger Database")

    chargers = db.query(ChargerDB).all()

    col1, col2 = st.columns([8,2])

    with col2:
        if st.button("➕ Add Charger"):
            st.session_state.mode = "add_charger"
            st.rerun()

    # TABLE
    h1,h2,h3,h4 = st.columns(4)

    h1.write("Name")
    h2.write("Type")
    h3.write("Power kW")
    h4.write("Action")

    st.divider()

    for c in chargers:

        c1,c2,c3,c4 = st.columns(4)

        c1.write(c.name)
        c2.write(c.type)
        c3.write(c.power_kw)

        if c4.button("Manage", key=f"charger{c.id}"):

            st.session_state.selected_charger = c.id
            st.session_state.mode = "manage_dispensers"

            st.rerun()

    # ---------------- ADD CHARGER ----------------

    if st.session_state.get("mode") == "add_charger":

        st.subheader("Add Charger")

        name = st.text_input("Name")

        ctype = st.selectbox("Type", ["Standalone","Split"])

        power = st.number_input("Power kW", value=120)

        price = st.number_input("Price", value=500000)

        if st.button("Save Charger"):

            charger = ChargerDB(
                name=name,
                type=ctype,
                power_kw=power,
                price=price
            )

            db.add(charger)
            db.commit()

            st.success("Charger added")

            st.session_state.mode = None
            st.rerun()

    # ---------------- MANAGE DISPENSERS ----------------

    if st.session_state.get("mode") == "manage_dispensers":

        charger = db.query(ChargerDB).filter(
            ChargerDB.id == st.session_state.selected_charger
        ).first()

        st.subheader(f"Dispensers for {charger.name}")

        dispensers = db.query(DispenserDB).filter(
            DispenserDB.charger_id == charger.id
        ).all()

        for d in dispensers:

            c1,c2,c3,c4 = st.columns(4)

            c1.write(d.type)
            c2.write(f"{d.connectors} connectors")
            c3.write(f"{d.amp_per_connector} A")

            if c4.button("Delete", key=f"d{d.id}"):

                db.delete(d)
                db.commit()

                st.rerun()

        st.divider()

        st.subheader("Add Dispenser")

        d_type = st.selectbox("Type", ["Liquid","Boost"])

        connectors = st.number_input("Connectors", value=2)

        amp = st.number_input("Amp per connector", value=250)

        if st.button("Add Dispenser"):

            dis = DispenserDB(
                charger_id=charger.id,
                type=d_type,
                connectors=connectors,
                amp_per_connector=amp
            )

            db.add(dis)
            db.commit()

            st.success("Dispenser added")

            st.rerun()

    db.close()
