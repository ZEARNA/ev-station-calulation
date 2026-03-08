import streamlit as st
from database import SessionLocal, ChargerDB, DispenserDB
from calculator import calculate_project


def user_dashboard():

    st.header("EV Station ROI Calculator")

    db = SessionLocal()

    chargers = db.query(ChargerDB).all()

    if len(chargers) == 0:
        st.warning("No chargers in database")
        db.close()
        return

    # =============================
    # SELECT CHARGER
    # =============================

    charger_names = [c.name for c in chargers]

    selected = st.selectbox("Select Charger", charger_names)

    charger = next(c for c in chargers if c.name == selected)

    st.divider()

    # =============================
    # DISPENSER SELECT
    # =============================

    dispensers = db.query(DispenserDB).filter(
        DispenserDB.charger_id == charger.id
    ).all()

    if len(dispensers) == 0:
        st.warning("No dispenser available for this charger")
        db.close()
        return

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

    # =============================
    # SESSION LIST
    # =============================

    if "disp_list" not in st.session_state:
        st.session_state.disp_list = []

    if st.button("➕ Add Dispenser"):

        st.session_state.disp_list.append({
            "type": disp.type,
            "connectors": disp.connectors,
            "count": disp_count
        })

        st.rerun()

    # =============================
    # SHOW DISPENSER LIST
    # =============================

    st.subheader("Selected Dispensers")

    total_connectors = 0

    for i, d in enumerate(st.session_state.disp_list):

        c1, c2, c3 = st.columns([5,2,1])

        c1.write(
            f"{d['type']} | {d['connectors']} connectors × {d['count']}"
        )

        connectors = d["connectors"] * d["count"]

        c2.write(f"{connectors} connectors")

        if c3.button("❌", key=f"del_disp_{i}"):

            st.session_state.disp_list.pop(i)

            st.rerun()

        total_connectors += connectors

    st.divider()

    st.write(f"Total connectors: **{total_connectors}**")

    st.write(f"Max connectors per power unit: **{charger.max_connectors}**")

    if total_connectors > charger.max_connectors:

        st.error("Exceeded max connectors of power unit")

        db.close()
        return

    st.divider()

    # =============================
    # ROI INPUT
    # =============================

    qty = st.number_input("Number of Chargers", value=2)

    utilization = st.slider("Utilization %", 0, 100, 20) / 100

    charge_price = st.number_input("Charging Price (THB/kWh)", value=8.0)

    electricity_cost = st.number_input("Electricity Cost (THB/kWh)", value=4.0)

    # =============================
    # CALCULATE ROI
    # =============================

    if st.button("Calculate ROI"):

        if total_connectors == 0:

            st.error("Please add at least one dispenser")

            db.close()
            return

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
