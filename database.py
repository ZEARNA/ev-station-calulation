from sqlalchemy import create_engine, Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import hashlib

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

    username = Column(String, unique=True)

    password = Column(String)

    role = Column(String)


# ==========================
# CHARGER TABLE
# ==========================

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
        ForeignKey("chargers.id")
    )

    type = Column(String)

    connectors = Column(Integer)

    amp_per_connector = Column(Float)

    charger = relationship(
        "ChargerDB",
        back_populates="dispensers"
    )


# ==========================
# TRANSFORMER TABLE
# ==========================

class TransformerDB(Base):

    __tablename__ = "transformers"

    id = Column(Integer, primary_key=True)

    brand = Column(String)

    kva = Column(Float)

    price = Column(Float)


# ==========================
# CABLE TABLE
# ==========================

class CableDB(Base):

    __tablename__ = "cables"

    id = Column(Integer, primary_key=True)

    type = Column(String)

    size = Column(Float)

    price_per_meter = Column(Float)

# ==========================
# INIT DATABASE
# ==========================

def init_db():

    Base.metadata.create_all(engine)

    db = SessionLocal()

    admin = db.query(UserDB).filter(UserDB.username == "admin").first()

    if not admin:

        password = hashlib.sha256("admin".encode()).hexdigest()

        admin_user = UserDB(
            username="admin",
            password=password,
            role="admin"
        )

        db.add(admin_user)
        db.commit()

    db.close()
