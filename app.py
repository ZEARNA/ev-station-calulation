import streamlit as st
from database import (
    SessionLocal,
    ChargerDB,
    DispenserDB,
    TransformerDB,
    CableDB
)


def charger_data_page():

    st.header("Database")

    db = SessionLocal()

    tab1, tab2, tab3, tab4 = st.tabs(
        ["Chargers", "Dispensers", "Transformers", "Cables"]
    )

    # ==========================
    # CHARGERS
    # ==========================

    with tab1:

        st.subheader("Chargers")

        chargers = db.query(ChargerDB).all()

        h1, h2, h3, h4 = st.columns(4)
        h1.write("Name")
        h2.write("Type")
        h3.write("Power kW")
        h4.write("Price")

        st.divider()

        for c in chargers:

            c1, c2, c3, c4 = st.columns(4)

            c1.write(c.name)
            c2.write(c.type)
            c3.write(c.power_kw)
            c4.write(c.price)

        st.divider()

        if st.button("Add Charger"):

            st.session_state.add_charger = True

        if st.session_state.get("add_charger"):

            name = st.text_input("Name")
            ctype = st.selectbox("Type", ["Standalone", "Split"])
            power = st.number_input("Power kW", value=120)
            price = st.number_input("Price", value=500000)
            max_conn = st.number_input("Max connectors", value=4)

            if st.button("Save Charger"):

                charger = ChargerDB(
                    name=name,
                    type=ctype,
                    power_kw=power,
                    price=price,
                    max_connectors=max_conn
                )

                db.add(charger)
                db.commit()

                st.session_state.add_charger = False

                st.rerun()

    # ==========================
    # DISPENSERS
    # ==========================

    with tab2:

        st.subheader("Dispensers")

        dispensers = db.query(DispenserDB).all()

        chargers = db.query(ChargerDB).all()

        charger_map = {c.id: c.name for c in chargers}

        h1, h2, h3, h4 = st.columns(4)

        h1.write("Charger")
        h2.write("Type")
        h3.write("Connectors")
        h4.write("Amp")

        st.divider()

        for d in dispensers:

            c1, c2, c3, c4 = st.columns(4)

            c1.write(charger_map.get(d.charger_id))
            c2.write(d.type)
            c3.write(d.connectors)
            c4.write(d.amp_per_connector)

    # ==========================
    # TRANSFORMERS
    # ==========================

    with tab3:

        st.subheader("Transformers")

        transformers = db.query(TransformerDB).all()

        h1, h2, h3 = st.columns(3)

        h1.write("Brand")
        h2.write("kVA")
        h3.write("Price")

        st.divider()

        for t in transformers:

            c1, c2, c3 = st.columns(3)

            c1.write(t.brand)
            c2.write(t.kva)
            c3.write(t.price)

        st.divider()

        if st.button("Add Transformer"):

            st.session_state.add_transformer = True

        if st.session_state.get("add_transformer"):

            brand = st.text_input("Brand")
            kva = st.number_input("kVA", value=1000)
            price = st.number_input("Price", value=800000)

            if st.button("Save Transformer"):

                transformer = TransformerDB(
                    brand=brand,
                    kva=kva,
                    price=price
                )

                db.add(transformer)
                db.commit()

                st.session_state.add_transformer = False

                st.rerun()

    # ==========================
    # CABLES
    # ==========================

    with tab4:

        st.subheader("Cables")

        cables = db.query(CableDB).all()

        h1, h2, h3 = st.columns(3)

        h1.write("Type")
        h2.write("Size")
        h3.write("Price / meter")

        st.divider()

        for c in cables:

            c1, c2, c3 = st.columns(3)

            c1.write(c.type)
            c2.write(c.size)
            c3.write(c.price_per_meter)

        st.divider()

        if st.button("Add Cable"):

            st.session_state.add_cable = True

        if st.session_state.get("add_cable"):

            cable_type = st.text_input("Type")
            size = st.number_input("Size mm²", value=50)
            price = st.number_input("Price per meter", value=200)

            if st.button("Save Cable"):

                cable = CableDB(
                    type=cable_type,
                    size=size,
                    price_per_meter=price
                )

                db.add(cable)
                db.commit()

                st.session_state.add_cable = False

                st.rerun()

    db.close()
