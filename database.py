from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base, sessionmaker

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


def init_db():
    Base.metadata.create_all(engine)
