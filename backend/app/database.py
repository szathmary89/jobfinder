
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite adatbázis elérési útja
DATABASE_URL = "sqlite:///./jobfinder.db"

# Adatbázis-kapcsolat létrehozása
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Adatbázis-munkamenetek kezelése
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Közös ősosztály az adatbázismodellekhez
class Base(DeclarativeBase):
    pass


# Adatbázis-kapcsolat biztosítása a végpontoknak
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
