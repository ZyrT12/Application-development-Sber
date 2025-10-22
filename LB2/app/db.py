from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql+psycopg2://app:app@localhost:5433/lab2",
    echo=True,
    future=True,
)

session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)
