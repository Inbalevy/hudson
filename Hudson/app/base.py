from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, CheckConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import Optional

Base = declarative_base()
ENGINE = create_engine('postgresql://hudsondb:HouseOfTemplates@db:5432/hudsondb', echo=True)
Session = sessionmaker(bind=ENGINE)


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