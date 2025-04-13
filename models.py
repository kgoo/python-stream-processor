import faust
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, TIMESTAMP

Base = declarative_base()

# Faust message schema
class Event(faust.Record, serializer='json'):
    key: str
    value: str
    timestamp: int

# ORM model for Postgres
class Aggregate(Base):
    __tablename__ = 'aggregates'

    value = Column(String, primary_key=True)
    window_start = Column(TIMESTAMP, primary_key=True)
    count = Column(Integer)
