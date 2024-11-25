import logging
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from models import Base, Data


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@db:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URI, future=True)
session = sessionmaker(bind=engine, expire_on_commit=False, class_=Session)


def init_db():
    Base.metadata.tables['data'].create(engine)


def save_data(data: list[dict[str, str]]):
    with session() as db:
        # logging.info("writing to db")
        for d in data:
            db.add(Data(**d))
        db.commit()
