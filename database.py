from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os

# ==========================
# DATABASE CONFIG
# ==========================

DATABASE_URL = "sqlite:///ev_saas.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


# ==========================
# USER TABLE
# ==========================

class UserDB(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String, nullable=False)

    password = Column(String, nullable=False)

    role = Column(String, nullable=False)


# ==========================
# CHARGER TABLE
# ==========================

class ChargerDB(Base):

    __tablename__ = "chargers"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)

    type = Column(String, nullable=False)

    power_kw = Column(Float, nullable=False)

    price = Column(Float, nullable=False)

    # max connectors allowed for split charger
    max_connectors = Column(Integer, nullable=False)

    dispensers = relationship(
        "DispenserDB",
        back_populates="charger",
        cascade="all, delete"
    )


# ==========================
# DISPENSER TABLE
# ==========================

class DispenserDB(Base):

    __tablename__ = "dispensers"

    id = Column(Integer, primary_key=True)

    charger_id = Column(
        Integer,
        ForeignKey("chargers.id"),
        nullable=False
    )

    type = Column(String, nullable=False)

    connectors = Column(Integer, nullable=False)

    amp_per_connector = Column(Float, nullable=False)

    charger = relationship(
        "ChargerDB",
        back_populates="dispensers"
    )


# ==========================
# INITIALIZE DATABASE
# ==========================

def init_db():

    Base.metadata.create_all(engine)
