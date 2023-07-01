from sqlalchemy import Column, Integer, String, DateTime, Enum
from typing import Optional

from .base import Base, Session

class Environment(Base):
    __tablename__ = 'environments'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    template_id = Column(Integer, nullable=False)
    status = Column(Enum('CREATING', 'ACTIVE', 'DESTROYING', 'DESTROYED', name='status_enum'), server_default='CREATING')
    creation_time = Column(DateTime, nullable=False)
    
    # __table_args__ = (
    #     CheckConstraint(
    #         "CASE WHEN status = 'CREATING' THEN TRUE "
    #         "WHEN status = 'ACTIVE' AND (SELECT status FROM environments WHERE id = old.id) = 'CREATING' THEN TRUE "
    #         "WHEN status = 'DESTROYING' AND (SELECT status FROM environments WHERE id = old.id) = 'ACTIVE' THEN TRUE "
    #         "WHEN status = 'DESTROYED' THEN TRUE ELSE FALSE END",
    #         name='check_status_order'
    #     ),
    # )
    
    def __repr__(self):
        return f"Environment(id={self.id}, name='{self.name}', template='{self.template_id}', status={self.status}, creation_time='{self.creation_time}')"
    
    def __eq__(self, other):
        if isinstance(other, Environment):
            return self.id == other.id