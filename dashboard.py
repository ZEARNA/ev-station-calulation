import streamlit as st
from database import SessionLocal, ChargerDB, DispenserDB
from calculator import calculate_project


def user_dashboard():

    st.header("EV Station ROI Calculator")

    db = SessionLocal()

    chargers = db.query(ChargerDB).all()

    charger_names = [c.name for c in chargers]

    selected_name = st.selectbox("Select Charger", charger_names)

    charger = next(c for c in chargers if c.name == selected_name)

    dispensers = db.query(DispenserDB).filter(
        DispenserDB.charger_id == charger.id
    ).all()

    if dispensers:

        disp_options = [
            f"{d.type} | {d.connectors} connectors"
            for d in dispensers
        ]

        selected_disp = st.selectbox("Select Dispenser", disp_options)

    qty = st.number_input("Number of Chargers", value=2)

    utilization = st.slider("Utilization %", 0, 100, 20)/100

    charge_price = st.number_input("Charging Price", value=8.0)

    electricity_cost = st.number_input("Electricity Cost", value=4.0)

    if st.button("Calculate ROI"):

        cost,profit,roi = calculate_project(
            charger.power_kw,
            charger.price,
            qty,
            utilization,
            charge_price,
            electricity_cost
        )

        st.metric("Project Cost", f"{cost:,.0f} THB")

        st.metric("Annual Profit", f"{profit:,.0f} THB")

        if roi:
            st.metric("ROI Years", f"{roi:.2f}")

    db.close()
