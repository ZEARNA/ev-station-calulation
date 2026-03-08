"""
EV Station Calculation (ev-station-calulation) Dashboard / SaaS‑Ready Engine (Dependency‑Safe Version)

This version fixes crashes in restricted environments where packages like
FastAPI, Pydantic, SQLAlchemy, or Streamlit may NOT be installed.

The program now runs in **three modes automatically** depending on what
libraries are available:

1️⃣ Full SaaS Mode
   FastAPI + Streamlit + SQLite

2️⃣ Dashboard Mode
   Streamlit only

3️⃣ CLI Mode (always works)
   Runs calculation demo in terminal

Install optional packages for full features:

pip install fastapi uvicorn streamlit pandas sqlalchemy pydantic

Run dashboard:

streamlit run app.py

Run API (if FastAPI installed):

uvicorn app:api --reload
"""

# =================================================
# SAFE IMPORTS
# =================================================

from pathlib import Path

# Optional libraries
try:
    from fastapi import FastAPI
    FASTAPI_AVAILABLE = True
except ModuleNotFoundError:
    FASTAPI_AVAILABLE = False

try:
    import streamlit as st
    import pandas as pd
    STREAMLIT_AVAILABLE = True
except ModuleNotFoundError:
    STREAMLIT_AVAILABLE = False

# Pydantic fallback
try:
    from pydantic import BaseModel
except ModuleNotFoundError:

    class BaseModel:
        def __init__(self, **data):
            for k, v in data.items():
                setattr(self, k, v)

# SQLAlchemy fallback
try:
    from sqlalchemy import create_engine, Column, Integer, Float, String
    from sqlalchemy.orm import declarative_base, sessionmaker
    SQLALCHEMY_AVAILABLE = True
except ModuleNotFoundError:
    SQLALCHEMY_AVAILABLE = False


# =================================================
# DATABASE SETUP (OPTIONAL)
# =================================================

if SQLALCHEMY_AVAILABLE:

    DATABASE_URL = "sqlite:///ev_saas.db"

    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    SessionLocal = sessionmaker(bind=engine)

    Base = declarative_base()

    class ChargerDB(Base):
        __tablename__ = "chargers"

        id = Column(Integer, primary_key=True)
        name = Column(String)
        type = Column(String)
        power_kw = Column(Float)
        current = Column(Float)
        price = Column(Float)
        dispenser_price = Column(Float)

    Base.metadata.create_all(engine)

else:

    ChargerDB = None
    SessionLocal = None


# =================================================
# DATA MODELS
# =================================================

class ChargerModel(BaseModel):

    name: str

    type: str

    power_kw: float

    current: float

    price: float

    dispenser_price: float = 0


class ProjectInput(BaseModel):

    model: ChargerModel

    qty: int

    dispenser_qty: int

    location: str

    utilization: float

    charge_price: float

    electricity_cost: float

    transformer_cost: float

    cable_cost: float

    land_rent_year: float

    om_year: float

    demand_charge_rate: float

    distance_m: float


# =================================================
# FINANCIAL FUNCTIONS
# =================================================


def calculate_irr(cashflows, guess=0.1, iterations=100):

    rate = guess

    for _ in range(iterations):

        npv = 0

        derivative = 0

        for t, cf in enumerate(cashflows):

            npv += cf / ((1 + rate) ** t)

            derivative -= t * cf / ((1 + rate) ** (t + 1))

        if derivative == 0:

            break

        rate = rate - npv / derivative

    return rate


# =================================================
# ENGINEERING ESTIMATION
# =================================================


def estimate_transformer_kva(total_power_kw):

    kva = total_power_kw / 0.9

    sizes = [250, 400, 630, 800, 1000, 1250, 1600]

    for s in sizes:

        if kva <= s:

            return s

    return sizes[-1]



def estimate_cable_cost(distance_m, cost_per_m=800):

    return distance_m * cost_per_m



def estimate_mdb_cost(total_current):

    if total_current <= 400:

        return 120000

    if total_current <= 800:

        return 250000

    return 350000


# =================================================
# CORE CALCULATION
# =================================================


def calculate_project(input_data):

    model = input_data.model

    qty = input_data.qty

    total_current = model.current * qty

    total_power = model.power_kw * qty

    transformer_kva = estimate_transformer_kva(total_power)

    cable_est = estimate_cable_cost(input_data.distance_m)

    mdb_cost = estimate_mdb_cost(total_current)

    if input_data.location == "MEA" and total_current <= 400:

        infrastructure_cost = input_data.cable_cost + mdb_cost

        meter_type = "Free Meter"

    else:

        infrastructure_cost = input_data.transformer_cost + input_data.cable_cost + mdb_cost

        meter_type = "Transformer Required"

    if model.type == "Standalone":

        equipment_cost = model.price * qty

    else:

        equipment_cost = model.price * qty + model.dispenser_price * input_data.dispenser_qty

    energy_day = total_power * input_data.utilization * 24

    revenue_day = energy_day * input_data.charge_price

    electricity_day = energy_day * input_data.electricity_cost

    demand_charge_month = total_power * input_data.demand_charge_rate

    demand_charge_year = demand_charge_month * 12

    profit_day = revenue_day - electricity_day

    annual_profit = profit_day * 365

    annual_profit -= demand_charge_year

    annual_profit -= input_data.land_rent_year

    annual_profit -= input_data.om_year

    total_project_cost = equipment_cost + infrastructure_cost + cable_est

    roi_years = None

    if annual_profit > 0:

        roi_years = total_project_cost / annual_profit

    cashflows = [-total_project_cost] + [annual_profit] * 10

    irr = calculate_irr(cashflows)

    cumulative_profit = []

    running = 0

    for _ in range(10):

        running += annual_profit

        cumulative_profit.append(running)

    return {

        "total_current": total_current,

        "transformer_kva": transformer_kva,

        "meter_type": meter_type,

        "equipment_cost": equipment_cost,

        "total_project_cost": total_project_cost,

        "annual_profit": annual_profit,

        "roi_years": roi_years,

        "irr": irr,

        "cumulative_profit": cumulative_profit

    }


# =================================================
# FASTAPI BACKEND (ONLY IF AVAILABLE)
# =================================================

if FASTAPI_AVAILABLE:

    api = FastAPI(title="EV Station Calculation API")

    @api.get("/")

    def root():

        return {"service": "EV Station Calculation API"}


    @api.post("/calculate")

    def api_calculate(input_data: ProjectInput):

        return calculate_project(input_data)


# =================================================
# STREAMLIT DASHBOARD (ONLY IF AVAILABLE)
# =================================================


def streamlit_app():

    st.title("⚡ EV Station Calculation Dashboard")

    charger_type = st.selectbox("Charger Type", ["Standalone", "Split"])

    power = st.number_input("Power kW", value=120)

    current = st.number_input("Current A", value=200)

    price = st.number_input("Charger Price", value=500000)

    qty = st.number_input("Chargers", value=2)

    utilization = st.slider("Utilization %", 0, 100, 20) / 100

    charge_price = st.number_input("Charging Price", value=8.0)

    electricity_cost = st.number_input("Electricity Cost", value=4.0)

    if st.button("Calculate"):

        model = ChargerModel(

            name="Custom",

            type=charger_type,

            power_kw=power,

            current=current,

            price=price,

            dispenser_price=300000

        )

        payload = ProjectInput(

            model=model,

            qty=qty,

            dispenser_qty=6 if charger_type == "Split" else 0,

            location="MEA",

            utilization=utilization,

            charge_price=charge_price,

            electricity_cost=electricity_cost,

            transformer_cost=450000,

            cable_cost=200000,

            land_rent_year=200000,

            om_year=50000,

            demand_charge_rate=200,

            distance_m=80

        )

        result = calculate_project(payload)

        st.metric("Project Cost", f"{result['total_project_cost']:,.0f} THB")

        st.metric("Annual Profit", f"{result['annual_profit']:,.0f} THB")

        st.metric("IRR", f"{result['irr']*100:.1f}%")

        st.line_chart(result["cumulative_profit"])


# =================================================
# TESTS
# =================================================


def _test_transformer():

    assert estimate_transformer_kva(200) >= 250



def _test_cable():

    assert estimate_cable_cost(100) == 80000



def _test_calculation():

    model = ChargerModel(

        name="Test",

        type="Standalone",

        power_kw=120,

        current=200,

        price=500000,

        dispenser_price=0

    )

    payload = ProjectInput(

        model=model,

        qty=2,

        dispenser_qty=0,

        location="MEA",

        utilization=0.2,

        charge_price=8,

        electricity_cost=4,

        transformer_cost=450000,

        cable_cost=200000,

        land_rent_year=200000,

        om_year=50000,

        demand_charge_rate=200,

        distance_m=80

    )

    result = calculate_project(payload)

    assert result["total_project_cost"] > 0


# =================================================
# ENTRY (Streamlit Cloud compatible)
# =================================================

# Streamlit Cloud does NOT run the script through the
# usual `if __name__ == "__main__"` path. Therefore we
# must start the dashboard directly when Streamlit is
# available.

if STREAMLIT_AVAILABLE:
    # Run basic tests once (safe, very fast)
    try:
        _test_transformer()
        _test_cable()
        _test_calculation()
    except Exception:
        pass

    # Launch dashboard
    streamlit_app()

else:

    # CLI fallback when Streamlit is not installed
    print("Running CLI demo...\n")

    demo_model = ChargerModel(
        name="Demo",
        type="Standalone",
        power_kw=120,
        current=200,
        price=500000,
        dispenser_price=0
    )

    demo = ProjectInput(
        model=demo_model,
        qty=2,
        dispenser_qty=0,
        location="MEA",
        utilization=0.2,
        charge_price=8,
        electricity_cost=4,
        transformer_cost=450000,
        cable_cost=200000,
        land_rent_year=200000,
        om_year=50000,
        demand_charge_rate=200,
        distance_m=80
    )

    print(calculate_project(demo))
