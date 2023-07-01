from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Template(Base):
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    state = Column(Enum('ENABLED', 'DISABLED', name='state_enum'), default='ENABLED')
    creation_time = Column(DateTime, nullable=False)

class Environment(Base):
    __tablename__ = 'environments'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    template_id = Column(Integer, nullable=False)
    status = Column(Enum('CREATING', 'ACTIVE', 'DESTROYING', 'DESTROYED', name='status_enum'), default='CREATING')
    creation_time = Column(DateTime, nullable=False)