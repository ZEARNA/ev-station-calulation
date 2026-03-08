import streamlit as st
from database import SessionLocal, ChargerDB, DispenserDB


def charger_data_page():

    db = SessionLocal()

    st.header("Infrastructure Database")

    tab1, tab2, tab3, tab4 = st.tabs(["Chargers", "Dispensers", "Transformers", "Cables"])

    # =====================================================
    # CHARGER DATABASE
    # =====================================================

    with tab1:

        chargers = db.query(ChargerDB).all()

        col1, col2 = st.columns([8, 2])

        with col2:
            if st.button("➕ Add Charger", key="btn_add_charger"):
                st.session_state.add_charger = True

        # TABLE HEADER
        h1, h2, h3, h4, h5 = st.columns(5)

        h1.write("Name")
        h2.write("Type")
        h3.write("Power kW")
        h4.write("Price")
        h5.write("Action")

        st.divider()

        for c in chargers:

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.write(c.name)
            c2.write(c.type)
            c3.write(c.power_kw)
            c4.write(c.price)

            edit_col, del_col = c5.columns(2)

            if edit_col.button("Edit", key=f"edit_charger_{c.id}"):
                st.session_state.edit_charger = c.id

            if del_col.button("Delete", key=f"delete_charger_{c.id}"):

                db.delete(c)
                db.commit()

                st.rerun()

        # ---------------- ADD CHARGER ----------------

        if st.session_state.get("add_charger"):

            st.subheader("Add Charger")

            name = st.text_input("Name", key="add_charger_name")

            ctype = st.selectbox(
                "Type",
                ["Standalone", "Split"],
                key="add_charger_type",
            )

            power = st.number_input(
                "Power kW",
                value=120,
                key="add_charger_power",
            )

            price = st.number_input(
                "Price",
                value=500000,
                key="add_charger_price",
            )

            max_conn = st.number_input(
                "Max connectors per power unit",
                value=8,
                key="add_charger_max_conn",
            )

            col1, col2 = st.columns(2)

            if col1.button("Save Charger", key="save_charger"):

                charger = ChargerDB(
                    name=name,
                    type=ctype,
                    power_kw=power,
                    price=price,
                    max_connectors=max_conn,
                )

                db.add(charger)
                db.commit()

                st.session_state.add_charger = False

                st.rerun()

            if col2.button("Cancel", key="cancel_add_charger"):

                st.session_state.add_charger = False
                st.rerun()

        # ---------------- EDIT CHARGER ----------------

        if "edit_charger" in st.session_state:

            charger = db.query(ChargerDB).filter(
                ChargerDB.id == st.session_state.edit_charger
            ).first()

            st.subheader("Edit Charger")

            name = st.text_input(
                "Name",
                value=charger.name,
                key="edit_charger_name",
            )

            ctype = st.selectbox(
                "Type",
                ["Standalone", "Split"],
                index=0 if charger.type == "Standalone" else 1,
                key="edit_charger_type",
            )

            power = st.number_input(
                "Power kW",
                value=charger.power_kw,
                key="edit_charger_power",
            )

            price = st.number_input(
                "Price",
                value=charger.price,
                key="edit_charger_price",
            )

            max_conn = st.number_input(
                "Max connectors per power unit",
                value=charger.max_connectors,
                key="edit_charger_max_conn",
            )

            col1, col2 = st.columns(2)

            if col1.button("Update Charger", key="update_charger"):

                charger.name = name
                charger.type = ctype
                charger.power_kw = power
                charger.price = price
                charger.max_connectors = max_conn

                db.commit()

                del st.session_state.edit_charger

                st.rerun()

            if col2.button("Cancel Edit", key="cancel_edit_charger"):

                del st.session_state.edit_charger
                st.rerun()

    # =====================================================
    # DISPENSER DATABASE
    # =====================================================

    with tab2:

        dispensers = db.query(DispenserDB).all()
        chargers = db.query(ChargerDB).all()

        charger_names = {c.id: c.name for c in chargers}

        col1, col2 = st.columns([8, 2])

        with col2:
            if st.button("➕ Add Dispenser", key="btn_add_disp"):
                st.session_state.add_disp = True

        # TABLE HEADER
        h1, h2, h3, h4, h5 = st.columns(5)

        h1.write("Charger")
        h2.write("Type")
        h3.write("Connectors")
        h4.write("Amp")
        h5.write("Action")

        st.divider()

        for d in dispensers:

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.write(charger_names.get(d.charger_id, "Unknown"))
            c2.write(d.type)
            c3.write(d.connectors)
            c4.write(d.amp_per_connector)

            edit_col, del_col = c5.columns(2)

            if edit_col.button("Edit", key=f"edit_disp_{d.id}"):

                st.session_state.edit_disp = d.id

            if del_col.button("Delete", key=f"delete_disp_{d.id}"):

                db.delete(d)
                db.commit()

                st.rerun()

        # ---------------- ADD DISPENSER ----------------

        if st.session_state.get("add_disp"):

            st.subheader("Add Dispenser")

            charger_select = st.selectbox(
                "Compatible Charger",
                chargers,
                format_func=lambda x: x.name,
                key="add_disp_charger",
            )

            d_type = st.selectbox(
                "Type",
                ["Liquid", "Boost"],
                key="add_disp_type",
            )

            connectors = st.number_input(
                "Connectors",
                value=2,
                key="add_disp_conn",
            )

            amp = st.number_input(
                "Amp per connector",
                value=250,
                key="add_disp_amp",
            )

            col1, col2 = st.columns(2)

            if col1.button("Save Dispenser", key="save_disp"):

                dis = DispenserDB(
                    charger_id=charger_select.id,
                    type=d_type,
                    connectors=connectors,
                    amp_per_connector=amp,
                )

                db.add(dis)
                db.commit()

                st.session_state.add_disp = False

                st.rerun()

            if col2.button("Cancel", key="cancel_disp"):

                st.session_state.add_disp = False
                st.rerun()

    db.close()
