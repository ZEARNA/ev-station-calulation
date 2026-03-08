import streamlit as st
from database import SessionLocal, ChargerDB


def list_chargers():

    db = SessionLocal()

    chargers = db.query(ChargerDB).all()

    db.close()

    return chargers
