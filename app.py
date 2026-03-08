"""
EV Station Calculation (ev-station-calulation)

Features
- Login system
- Admin can create users
- Admin can create charger models with price
- Users can calculate EV charging station ROI
- Works on Streamlit Cloud

Default admin login
username: admin
password: admin
"""

from pathlib import Path
import hashlib

# =================================================
# SAFE IMPORTS
# =================================================

try:
    import streamlit as st
    import pandas as pd
    STREAMLIT_AVAILABLE = True
except ModuleNotFoundError:
    STREAMLIT_AVAILABLE = False

try:
    from sqlalchemy import create_engine, Column, Integer, Float, String
    from sqlalchemy.orm import declarative_base, sessionmaker
    SQLALCHEMY_AVAILABLE = True
except ModuleNotFoundError:
    SQLALCHEMY_AVAILABLE = False


# =================================================
# DATABASE
# =================================================

if SQLALCHEMY_AVAILABLE:

    DATABASE_URL = "sqlite:///ev_saas.db"

    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    SessionLocal = sessionmaker(bind=engine)

    Base = declarative_base()


    class UserDB(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True)
        username = Column(String)
        password = Column(String)
        role = Column(String)


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


    # create default admin if not exists
    db = SessionLocal()

    if db.query(UserDB).count() == 0:

        admin = UserDB(
            username="admin",
            password=hashlib.sha256("admin".encode()).hexdigest(),
            role="admin",
        )

        db.add(admin)
        db.commit()

    db.close()


# =================================================
# UTILS
# =================================================


def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()


# =================================================
# CALCULATION ENGINE
# =================================================


def calculate_project(power, price, qty, utilization, charge_price, electricity_cost):

    energy_day = power * qty * utilization * 24

    revenue_day = energy_day * charge_price

    electricity_day = energy_day * electricity_cost

    annual_profit = (revenue_day - electricity_day) * 365

    project_cost = price * qty

    roi = None

    if annual_profit > 0:
        roi = project_cost / annual_profit

    return project_cost, annual_profit, roi


# =================================================
# LOGIN SYSTEM
# =================================================


def login_screen():

    st.title("EV Station Calculation Login")

    username = st.text_input("Username")

    password = st.text_input("Password", type="password")

    if st.button("Login"):

        db = SessionLocal()

        user = (
            db.query(UserDB)
            .filter(
                UserDB.username == username,
                UserDB.password == hash_password(password),
            )
            .first()
        )

        db.close()

        if user:

            st.session_state.user = username
            st.session_state.role = user.role

            st.rerun()

        else:

            st.error("Invalid login")


# =================================================
# ADMIN PANEL
# =================================================


def admin_panel():

    st.header("Admin Panel")

    db = SessionLocal()

    tab1, tab2 = st.tabs(["Create User", "Create Charger"])

    with tab1:

        st.subheader("Create User")

        u = st.text_input("Username")

        p = st.text_input("Password")

        role = st.selectbox("Role", ["user", "admin"])

        if st.button("Create User"):

            user = UserDB(
                username=u,
                password=hash_password(p),
                role=role,
            )

            db.add(user)
            db.commit()

            st.success("User created")

    with tab2:

        st.subheader("Create Charger")

        name = st.text_input("Name")

        ctype = st.selectbox("Type", ["Standalone", "Split"])

        power = st.number_input("Power kW", value=120)

        current = st.number_input("Current A", value=200)

        price = st.number_input("Price", value=500000)

        dispenser = st.number_input("Dispenser Price", value=300000)

        if st.button("Create Charger"):

            c = ChargerDB(
                name=name,
                type=ctype,
                power_kw=power,
                current=current,
                price=price,
                dispenser_price=dispenser,
            )

            db.add(c)
            db.commit()

            st.success("Charger created")

    db.close()


# =================================================
# USER DASHBOARD
# =================================================


def user_dashboard():

    st.header("EV Station ROI Calculator")

    db = SessionLocal()

    chargers = db.query(ChargerDB).all()

    if len(chargers) == 0:
        st.warning("No charger models created by admin")
        return

    charger_names = [c.name for c in chargers]

    selected = st.selectbox("Charger", charger_names)

    charger = next(c for c in chargers if c.name == selected)

    qty = st.number_input("Number of Chargers", value=2)

    utilization = st.slider("Utilization %", 0, 100, 20) / 100

    charge_price = st.number_input("Charging Price", value=8.0)

    electricity_cost = st.number_input("Electricity Cost", value=4.0)

    if st.button("Calculate"):

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

        if roi:
            st.metric("ROI Years", f"{roi:.2f}")

    db.close()


# =================================================
# MAIN STREAMLIT APP
# =================================================


def streamlit_app():

    if "user" not in st.session_state:
        login_screen()
        return

    st.sidebar.write(f"Logged in as: {st.session_state.user}")

    if st.sidebar.button("Logout"):
        del st.session_state.user
        del st.session_state.role
        st.rerun()

    if st.session_state.role == "admin":

        page = st.sidebar.selectbox("Menu", ["Dashboard", "Admin"])

        if page == "Admin":
            admin_panel()
        else:
            user_dashboard()

    else:

        user_dashboard()


# =================================================
# RUN APP
# =================================================

if STREAMLIT_AVAILABLE:

    streamlit_app()

else:

    print("Install streamlit to run the dashboard")
