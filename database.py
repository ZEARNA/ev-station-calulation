from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///ev_saas.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class ChargerDB(Base):

    __tablename__ = "chargers"

    id = Column(Integer, primary_key=True)

    name = Column(String)
    type = Column(String)

    power_kw = Column(Float)

    price = Column(Float)

    max_connectors = Column(Integer)

    dispensers = relationship(
        "DispenserDB",
        back_populates="charger"
    )


class DispenserDB(Base):

    __tablename__ = "dispensers"

    id = Column(Integer, primary_key=True)

    charger_id = Column(Integer, ForeignKey("chargers.id"))

    type = Column(String)

    connectors = Column(Integer)

    amp_per_connector = Column(Float)

    charger = relationship(
        "ChargerDB",
        back_populates="dispensers"
    )


def init_db():

    Base.metadata.create_all(engine)
