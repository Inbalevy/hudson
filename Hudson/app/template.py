from sqlalchemy import Column, Integer, String, DateTime, Enum
from typing import Optional

from .base import Base, Session


class Template(Base):
    __tablename__ = 'templates'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    state = Column(Enum('ENABLED', 'DISABLED', name='state_enum'), default='ENABLED')
    creation_time = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f"Template(id={self.id}, name='{self.name}', url='{self.url}', state={self.state}, creation_time='{self.creation_time}')"

    def __eq__(self, other):
        if isinstance(other, Template):
            return self.id == other.id

    @staticmethod
    def list_templates(only_enabled: bool = True):
        """list all existing templates in the db. by default, shows only active templates

        Args:
            only_enabled (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        with Session() as session:
            templates = session.query(Template)
            if only_enabled:
                templates.filter(Template.state == "ENABLED")
            templates = templates.all()
        return templates
    
    @staticmethod
    def get_template_details(id: Optional[int]=None, name: Optional[str]=None):
        """get template info, either by id or by name

        Args:
            id (Optional[int], optional): template_id. Defaults to None.
            name (Optional[str], optional): template_name. Defaults to None.
        """
        with Session() as session:
            query = session.query(Template)
            if id is not None:
                template = query.filter(Template.id == id).first()
            elif name is not None:
                template = query.filter(Template.name == name).first()
            else:
                template = None
        return template