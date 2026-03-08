import streamlit as st
import pandas as pd
from database import SessionLocal, ChargerDB


def charger_data_page():

    st.header("Charger Database")

    db = SessionLocal()

    chargers = db.query(ChargerDB).all()

    if len(chargers) == 0:
        st.info("No chargers in database")
        db.close()
        return

    data = []

    for c in chargers:

        data.append(
            {
                "Name": c.name,
                "Type": c.type,
                "Power kW": c.power_kw,
                "Current A": c.current,
                "Price": c.price,
                "Dispenser": c.dispenser_price,
            }
        )

    df = pd.DataFrame(data)

    st.dataframe(df, use_container_width=True)

    db.close()
