from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Data(Base):
    __tablename__ = "data"
    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    link = Column(String(256))
    sale_price = Column(Float)
    full_price = Column(Float)
    count = Column(Integer, nullable=True)
