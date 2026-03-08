import streamlit as st
from database import SessionLocal, ChargerDB


def charger_data_page():

    st.header("Charger Database")

    db = SessionLocal()

    chargers = db.query(ChargerDB).all()

    # -----------------------------
    # GRID STYLE
    # -----------------------------

    st.markdown(
        """
        <style>
        .grid-row {
            border-bottom:1px solid #ddd;
            padding:6px 0;
        }
        .grid-header {
            font-weight:bold;
            border-bottom:2px solid #999;
            padding:6px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # ADD BUTTON
    # -----------------------------

    col1, col2 = st.columns([8,2])

    with col2:
        if st.button("➕ Add Charger"):
            st.session_state.mode = "add"
            st.rerun()

    # -----------------------------
    # TABLE HEADER
    # -----------------------------

    h1, h2, h3, h4, h5, h6, h7 = st.columns(7)

    h1.markdown('<div class="grid-header">Name</div>', unsafe_allow_html=True)
    h2.markdown('<div class="grid-header">Type</div>', unsafe_allow_html=True)
    h3.markdown('<div class="grid-header">Power kW</div>', unsafe_allow_html=True)
    h4.markdown('<div class="grid-header">Current A</div>', unsafe_allow_html=True)
    h5.markdown('<div class="grid-header">Price</div>', unsafe_allow_html=True)
    h6.markdown('<div class="grid-header">Dispenser</div>', unsafe_allow_html=True)
    h7.markdown('<div class="grid-header">Action</div>', unsafe_allow_html=True)

    # -----------------------------
    # TABLE ROWS
    # -----------------------------

    for c in chargers:

        c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

        c1.markdown(f'<div class="grid-row">{c.name}</div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="grid-row">{c.type}</div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="grid-row">{c.power_kw}</div>', unsafe_allow_html=True)
        c4.markdown(f'<div class="grid-row">{c.current}</div>', unsafe_allow_html=True)
        c5.markdown(f'<div class="grid-row">{c.price}</div>', unsafe_allow_html=True)
        c6.markdown(f'<div class="grid-row">{c.dispenser_price}</div>', unsafe_allow_html=True)

        if c7.button("Edit", key=f"edit_{c.id}"):

            st.session_state.selected_charger = c.id
            st.session_state.mode = "edit"
            st.rerun()

    # -----------------------------
    # ADD CHARGER
    # -----------------------------

    if st.session_state.get("mode") == "add":

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

            st.session_state.mode = None
            st.rerun()

    # -----------------------------
    # EDIT CHARGER
    # -----------------------------

    if st.session_state.get("mode") == "edit":

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

            if st.button("Update Charger"):

                charger.name = name
                charger.type = ctype
                charger.power_kw = power
                charger.current = current
                charger.price = price
                charger.dispenser_price = dispenser

                db.commit()

                st.success("Updated")

                st.session_state.mode = None
                st.rerun()

        with col2:

            if st.button("Delete Charger"):
                st.session_state.confirm_delete = True

        # -----------------------------
        # CONFIRM DELETE
        # -----------------------------

        if st.session_state.get("confirm_delete"):

            st.warning("⚠️ Are you sure you want to delete this charger?")

            c1, c2 = st.columns(2)

            with c1:

                if st.button("Confirm Delete"):

                    db.delete(charger)
                    db.commit()

                    st.success("Deleted")

                    st.session_state.confirm_delete = False
                    st.session_state.mode = None

                    st.rerun()

            with c2:

                if st.button("Cancel"):

                    st.session_state.confirm_delete = False
                    st.rerun()

    db.close()
