from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import secrets

Base = declarative_base()
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)


class Oreht(Base):
    __tablename__ = secrets.secret.DATABASE_NAME

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    photo = Column(String)
    item_code = Column(Integer)
    price = Column(Float)

    def __init__(self, name, url, photo, item_code, price):
        self.name = name
        self.url = url
        self.photo = photo
        self.item_code = item_code
        self.price = price


Base.metadata.create_all(engine)
