import streamlit as st
from database import SessionLocal, ChargerDB, TransformerDB, CableDB


def user_dashboard():

    st.header("Infrastructure Database")

    db = SessionLocal()

    tab1, tab2, tab3 = st.tabs(
        ["Chargers", "Transformers", "Cables"]
    )

    # ==========================
    # TRANSFORMER DATABASE
    # ==========================

    with tab2:

        st.subheader("Transformer Database")

        transformers = db.query(TransformerDB).all()

        c1, c2 = st.columns([8, 2])

        with c2:
            if st.button("➕ Add Transformer"):
                st.session_state.add_transformer = True

        h1, h2, h3, h4 = st.columns(4)

        h1.write("Brand")
        h2.write("kVA")
        h3.write("Price")
        h4.write("Action")

        st.divider()

        for t in transformers:

            c1, c2, c3, c4 = st.columns(4)

            c1.write(t.brand)
            c2.write(t.kva)
            c3.write(t.price)

            edit_col, del_col = c4.columns(2)

            if edit_col.button("Edit", key=f"edit_t_{t.id}"):
                st.session_state.edit_transformer = t.id

            if del_col.button("Delete", key=f"del_t_{t.id}"):

                db.delete(t)
                db.commit()
                st.rerun()

        # ADD TRANSFORMER

        if st.session_state.get("add_transformer"):

            st.subheader("Add Transformer")

            brand = st.text_input("Brand")

            kva = st.number_input("kVA", value=1000)

            price = st.number_input("Price", value=500000)

            col1, col2 = st.columns(2)

            if col1.button("Save Transformer"):

                transformer = TransformerDB(
                    brand=brand,
                    kva=kva,
                    price=price
                )

                db.add(transformer)
                db.commit()

                st.session_state.add_transformer = False
                st.rerun()

            if col2.button("Cancel"):
                st.session_state.add_transformer = False
                st.rerun()

    # ==========================
    # CABLE DATABASE
    # ==========================

    with tab3:

        st.subheader("Cable Database")

        cables = db.query(CableDB).all()

        c1, c2 = st.columns([8, 2])

        with c2:
            if st.button("➕ Add Cable"):
                st.session_state.add_cable = True

        h1, h2, h3, h4 = st.columns(4)

        h1.write("Type")
        h2.write("Size")
        h3.write("Price / meter")
        h4.write("Action")

        st.divider()

        for c in cables:

            c1, c2, c3, c4 = st.columns(4)

            c1.write(c.type)
            c2.write(c.size)
            c3.write(c.price_per_meter)

            edit_col, del_col = c4.columns(2)

            if edit_col.button("Edit", key=f"edit_c_{c.id}"):
                st.session_state.edit_cable = c.id

            if del_col.button("Delete", key=f"del_c_{c.id}"):

                db.delete(c)
                db.commit()

                st.rerun()

        # ADD CABLE

        if st.session_state.get("add_cable"):

            st.subheader("Add Cable")

            cable_type = st.text_input("Type")

            size = st.number_input("Size (mm²)", value=50)

            price = st.number_input("Price per meter", value=200)

            col1, col2 = st.columns(2)

            if col1.button("Save Cable"):

                cable = CableDB(
                    type=cable_type,
                    size=size,
                    price_per_meter=price
                )

                db.add(cable)
                db.commit()

                st.session_state.add_cable = False
                st.rerun()

            if col2.button("Cancel"):

                st.session_state.add_cable = False
                st.rerun()

    db.close()
