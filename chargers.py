import streamlit as st
import pandas as pd
from database import SessionLocal, ChargerDB


def charger_data_page():

    db = SessionLocal()

    # ---------------------
    # HEADER + ADD BUTTON
    # ---------------------

    col1, col2 = st.columns([8, 2])

    with col1:
        st.header("Charger Database")

    with col2:
        add = st.button("➕ Add Charger", use_container_width=True)

    # ---------------------
    # LOAD DATA
    # ---------------------

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

    # ---------------------
    # TABLE
    # ---------------------

    edited_df = st.data_editor(
        df,
        use_container_width=True,
        num_rows="dynamic"
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        save = st.button("💾 Save Changes")

    with col2:
        delete = st.button("🗑 Delete Selected")

    # ---------------------
    # ADD CHARGER
    # ---------------------

    if add:

        new_charger = ChargerDB(
            name="New Charger",
            type="Standalone",
            power_kw=120,
            current=200,
            price=500000,
            dispenser_price=300000,
        )

        db.add(new_charger)
        db.commit()

        st.success("New charger added")
        st.rerun()

    # ---------------------
    # SAVE EDIT
    # ---------------------

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

    # ---------------------
    # DELETE
    # ---------------------

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
