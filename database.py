import streamlit as st
from database import SessionLocal, ChargerDB, DispenserDB
from calculator import calculate_project


def user_dashboard():

    st.header("EV Station ROI Calculator")

    db = SessionLocal()

    chargers = db.query(ChargerDB).all()

    if len(chargers) == 0:
        st.warning("No charger models created")
        db.close()
        return

    names = [c.name for c in chargers]

    selected = st.selectbox("Charger", names)

    charger = next(c for c in chargers if c.name == selected)

    dispensers = db.query(DispenserDB).filter(
        DispenserDB.charger_id == charger.id
    ).all()

    disp_options = {
        f"{d.type} | {d.connectors} connectors": d
        for d in dispensers
    }

    disp_label = st.selectbox(
        "Select Dispenser",
        list(disp_options.keys())
    )

    disp = disp_options[disp_label]

    disp_count = st.number_input(
        "Number of Dispensers",
        min_value=1,
        value=1
    )

    qty = st.number_input("Number of Chargers", value=2)

    utilization = st.slider("Utilization %", 0, 100, 20) / 100

    charge_price = st.number_input("Charging Price", value=8.0)

    electricity_cost = st.number_input("Electricity Cost", value=4.0)

    if st.button("Calculate ROI"):

        total_connectors = disp.connectors * disp_count

        power_per_connector = charger.power_kw / total_connectors

        cost, profit, roi = calculate_project(
            charger.power_kw,
            charger.price,
            qty,
            utilization,
            charge_price,
            electricity_cost,
        )

        st.metric("Project Cost", f"{cost:,.0f} THB")
        st.metric("Annual Profit", f"{profit:,.0f} THB")
        st.metric("Power per Connector", f"{power_per_connector:.1f} kW")

        if roi:
            st.metric("ROI Years", f"{roi:.2f}")

    db.close()
