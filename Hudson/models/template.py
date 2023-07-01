from datetime import datetime
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


class TemplateActions(): 
    @staticmethod   
    def list_templates(only_enabled: bool = False) -> list[Template]:
        """list all existing templates in the db. by default, shows only active templates

        Args:
            only_enabled (bool, optional): _description_. Defaults to False.

        Returns:
            list[Template]
        """
        with Session() as session:
            templates = session.query(Template)
            if only_enabled:
                templates = templates.filter(Template.state == "ENABLED")
            templates = templates.all()
        return templates

    @staticmethod
    def get_template(id: Optional[int]=None, name: Optional[str]=None) -> Optional[Template]:
        """get template info, either by id or by name

        Args:
            id (Optional[int], optional): template_id. Defaults to None.
            name (Optional[str], optional): template_name. Defaults to None.
        """
        if not (id or name):
            raise ValueError("Either 'id' or 'name' must be provided.")
    
        with Session() as session:
            query = session.query(Template)
            if id is not None:
                return query.filter(Template.id == id).first()
            elif name is not None:
                return query.filter(Template.name == name).first()
            return None

    @staticmethod
    def create_template(github_url: str, name: str) -> Optional[Template]:
        """create a new template by url and name (fetched from github-api)
        
        Args:
            github_url (int): github_url, accepted from the user
            name (Optional): repository name from github api
        """         
        with Session() as session:
            try:
                template = Template(name=name, url=github_url, state="ENABLED", creation_time=datetime.now())
                session.add(template)
                session.commit()
                session.refresh(template)
            except Exception as e:
                template = None
                session.rollback()
                raise
        return template
    
    @staticmethod
    def enable_template(id: Optional[int] = None, name: Optional[str] = None) -> bool:
        """enable a template by id or name. return True if succeeded and false if the template was already enabled
        Args:
            id (Optional[int], optional): template_id. Defaults to None.
            name (Optional[str], optional): template_name. Defaults to None.
        """
        with Session() as session:
            if (template := TemplateActions.get_template(id=id, name=name)) is None:
                raise ValueError("Template not found.")

            if template.state == "ENABLED":
                return False

            template.state = "ENABLED"
            session.commit()

        return True
    
    @staticmethod
    def disable_template(id: Optional[int] = None, name: Optional[str] = None) -> bool:
        """disable a template by id or name if no active environment is dependent on it. return True if succeeded and false if the template was already disabled
        Args:
            id (Optional[int], optional): template_id. Defaults to None.
            name (Optional[str], optional): template_name. Defaults to None.
        """
        with Session() as session:
            if (template := TemplateActions.get_template(id=id, name=name)) is None:
                raise ValueError("Template not found.")

            if template.state == "DISABLED":
                return False

            # to avoid circular import issue
            from .environment import Environment, StatusEnum
            if (active_env := session.query(Environment).filter(
                Environment.template_id == template.id,
                Environment.status.in_([StatusEnum.CREATING, StatusEnum.ACTIVE])
                ).first()):
                raise ValueError("Cannot disable template with an active environment.")

            template.state = "ENABLED"
            session.commit()

        return True