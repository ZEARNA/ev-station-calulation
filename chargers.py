import streamlit as st
from database import SessionLocal, ChargerDB, DispenserDB


def charger_data_page():

    db = SessionLocal()

    st.header("Charger Database")

    chargers = db.query(ChargerDB).all()

    col1, col2 = st.columns([8,2])

    with col2:
        if st.button("➕ Add Charger"):
            st.session_state.mode = "add"
            st.rerun()

    # TABLE HEADER
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

        if c4.button("Edit", key=c.id):
            st.session_state.selected = c.id
            st.session_state.mode = "edit"
            st.rerun()

    # ---------------- ADD ----------------

    if st.session_state.get("mode") == "add":

        st.subheader("Add Charger")

        name = st.text_input("Name")

        ctype = st.selectbox("Type", ["Standalone","Split"])

        power = st.number_input("Power Unit kW", value=120)

        price = st.number_input("Price", value=500000)

        dispensers = []

        if ctype == "Split":

            n = st.number_input("Number of Dispensers",1,10,1)

            for i in range(n):

                st.markdown(f"### Dispenser {i+1}")

                d_type = st.selectbox(
                    "Type",
                    ["Liquid","Boost"],
                    key=f"type{i}"
                )

                connectors = st.number_input(
                    "Connectors",
                    value=2,
                    key=f"conn{i}"
                )

                amp = st.number_input(
                    "Amp per connector",
                    value=250,
                    key=f"amp{i}"
                )

                dispensers.append((d_type,connectors,amp))

        if st.button("Save Charger"):

            charger = ChargerDB(
                name=name,
                type=ctype,
                power_kw=power,
                price=price
            )

            db.add(charger)
            db.commit()

            if ctype == "Split":

                for d in dispensers:

                    dis = DispenserDB(
                        charger_id=charger.id,
                        type=d[0],
                        connectors=d[1],
                        amp_per_connector=d[2]
                    )

                    db.add(dis)

                db.commit()

            st.success("Charger added")

            st.session_state.mode = None
            st.rerun()

    # ---------------- EDIT ----------------

    if st.session_state.get("mode") == "edit":

        charger = db.query(ChargerDB).filter(
            ChargerDB.id == st.session_state.selected
        ).first()

        st.subheader(f"Edit Charger : {charger.name}")

        name = st.text_input("Name", value=charger.name)

        power = st.number_input(
            "Power kW",
            value=charger.power_kw
        )

        price = st.number_input(
            "Price",
            value=charger.price
        )

        if st.button("Update Charger"):

            charger.name = name
            charger.power_kw = power
            charger.price = price

            db.commit()

            st.success("Updated")

            st.session_state.mode = None
            st.rerun()

        if st.button("Delete Charger"):

            db.delete(charger)
            db.commit()

            st.success("Deleted")

            st.session_state.mode = None
            st.rerun()

    db.close()
