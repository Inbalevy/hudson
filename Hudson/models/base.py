from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, CheckConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
ENGINE = create_engine('postgresql://hudsondb:HouseOfTemplates@db:5432/hudsondb', echo=False)
Session = sessionmaker(bind=ENGINE)
