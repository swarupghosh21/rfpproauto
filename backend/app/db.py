# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "postgresql://user:password@localhost:5432/rfpdb"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)

# Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./rfp.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()