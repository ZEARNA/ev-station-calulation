from database import SessionLocal, ChargerDB


def get_chargers():

    db = SessionLocal()

    chargers = db.query(ChargerDB).all()

    db.close()

    return chargers
