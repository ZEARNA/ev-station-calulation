import streamlit as st
import pandas as pd
from database import SessionLocal, ChargerDB


def charger_data_page():

    db = SessionLocal()

    # -----------------------------
    # HEADER + ADD BUTTON (TOP RIGHT)
    # -----------------------------

    left, right = st.columns([8,2])

    with left:
        st.header("Charger Database")

    with right:
        add = st.button("➕ Add Charger", use_container_width=True)

    chargers = db.query(ChargerDB).all()

    data = []

    for c in chargers:
        data.append(
            {
                "id": c.id,
                "Name": c.name,
                "Type": c.type,
                "Power kW": c.power_kw,
                "Current A": c.current,
                "Price": c.price,
                "Dispenser": c.dispenser_price,
                "Delete": False,
            }
        )

    df = pd.DataFrame(data)

    # -----------------------------
    # TABLE
    # -----------------------------

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic",
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        save = st.button("💾 Save Changes")

    with col2:
        delete = st.button("🗑 Delete Selected")

    # -----------------------------
    # ADD CHARGER
    # -----------------------------

    if add:

        new = ChargerDB(
            name="New Charger",
            type="Standalone",
            power_kw=120,
            current=200,
            price=500000,
            dispenser_price=300000,
        )

        db.add(new)
        db.commit()

        st.success("New charger added")

        st.rerun()

    # -----------------------------
    # SAVE EDIT
    # -----------------------------

    if save:

        for _, row in edited_df.iterrows():

            charger = db.query(ChargerDB).filter(
                ChargerDB.id == row["id"]
            ).first()

            if charger:

                charger.name = row["Name"]
                charger.type = row["Type"]
                charger.power_kw = row["Power kW"]
                charger.current = row["Current A"]
                charger.price = row["Price"]
                charger.dispenser_price = row["Dispenser"]

        db.commit()

        st.success("Changes saved")

        st.rerun()

    # -----------------------------
    # DELETE
    # -----------------------------

    if delete:

        for _, row in edited_df.iterrows():

            if row["Delete"]:

                charger = db.query(ChargerDB).filter(
                    ChargerDB.id == row["id"]
                ).first()

                if charger:
                    db.delete(charger)

        db.commit()

        st.success("Deleted selected chargers")

        st.rerun()

    db.close()
    else:
        st.info("No chargers in database")

    # -----------------------------
    # ADMIN ONLY SECTION
    # -----------------------------

    if st.session_state.role != "admin":
        db.close()
        return

    st.divider()

    # -----------------------------
    # ADD CHARGER
    # -----------------------------

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

    # -----------------------------
    # EDIT / DELETE
    # -----------------------------

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
