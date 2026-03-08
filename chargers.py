import streamlit as st
from database import SessionLocal, ChargerDB, DispenserDB


def charger_data_page():

    db = SessionLocal()

    st.header("Charger Database")

    tab1, tab2 = st.tabs(["Chargers", "Dispensers"])

    # =============================
    # CHARGER TABLE
    # =============================

    with tab1:

        chargers = db.query(ChargerDB).all()

        h1,h2,h3 = st.columns(3)

        h1.write("Name")
        h2.write("Type")
        h3.write("Power kW")

        st.divider()

        for c in chargers:

            c1,c2,c3 = st.columns(3)

            c1.write(c.name)
            c2.write(c.type)
            c3.write(c.power_kw)

    # =============================
    # DISPENSER DATABASE
    # =============================

    with tab2:

        st.subheader("Dispenser Database")

        dispensers = db.query(DispenserDB).all()

        chargers = db.query(ChargerDB).all()

        charger_names = {c.id: c.name for c in chargers}

        # TABLE HEADER
        h1,h2,h3,h4,h5 = st.columns(5)

        h1.write("Charger")
        h2.write("Type")
        h3.write("Connectors")
        h4.write("Amp")
        h5.write("Action")

        st.divider()

        for d in dispensers:

            c1,c2,c3,c4,c5 = st.columns(5)

            c1.write(charger_names.get(d.charger_id,"Unknown"))
            c2.write(d.type)
            c3.write(d.connectors)
            c4.write(d.amp_per_connector)

            if c5.button("Edit", key=f"edit_disp_{d.id}"):

                st.session_state.edit_disp = d.id
                st.rerun()

        # =============================
        # ADD DISPENSER
        # =============================

        st.divider()
        st.subheader("Add Dispenser")

        charger_select = st.selectbox(
            "Compatible Charger",
            chargers,
            format_func=lambda x: x.name
        )

        d_type = st.selectbox("Type", ["Liquid", "Boost"])

        connectors = st.number_input("Connectors", value=2)

        amp = st.number_input("Amp per connector", value=250)

        if st.button("Add Dispenser"):

            dis = DispenserDB(
                charger_id=charger_select.id,
                type=d_type,
                connectors=connectors,
                amp_per_connector=amp
            )

            db.add(dis)
            db.commit()

            st.success("Dispenser added")

            st.rerun()

        # =============================
        # EDIT DISPENSER
        # =============================

        if "edit_disp" in st.session_state:

            disp = db.query(DispenserDB).filter(
                DispenserDB.id == st.session_state.edit_disp
            ).first()

            st.divider()
            st.subheader("Edit Dispenser")

            d_type = st.selectbox(
                "Type",
                ["Liquid","Boost"],
                index=0 if disp.type=="Liquid" else 1
            )

            connectors = st.number_input(
                "Connectors",
                value=disp.connectors
            )

            amp = st.number_input(
                "Amp per connector",
                value=disp.amp_per_connector
            )

            col1,col2 = st.columns(2)

            with col1:

                if st.button("Update Dispenser"):

                    disp.type = d_type
                    disp.connectors = connectors
                    disp.amp_per_connector = amp

                    db.commit()

                    st.success("Updated")

                    del st.session_state.edit_disp
                    st.rerun()

            with col2:

                if st.button("Delete Dispenser"):

                    db.delete(disp)
                    db.commit()

                    st.success("Deleted")

                    del st.session_state.edit_disp
                    st.rerun()

    db.close()
