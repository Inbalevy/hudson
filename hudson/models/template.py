from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from typing import Optional
from hudson.database import db
from enum import Enum, IntEnum, StrEnum

class StateEnum(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    
    
class DependencyError(Exception):
    pass


class TemplateDisabledError(Exception):
    pass


class Template(db.Model):
    """Template model for the DB

    Args:
        db.Model: sqlalchemy model
    """
    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    url = db.Column(db.String(255), nullable=False)
    state = db.Column(db.Enum(StateEnum), default=StateEnum.ENABLED)
    creation_time = db.Column(db.String(255), nullable=False)
    
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

        templates = db.session.query(Template)
        if only_enabled:
            templates = templates.filter(Template.state == StateEnum.ENABLED)
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
    
        query = db.session.query(Template)
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
        try:
            template = Template(name=name, url=github_url, state=StateEnum.ENABLED, creation_time=datetime.now().isoformat())
            db.session.add(template)
            db.session.commit()
            db.session.refresh(template)
        except Exception as e:
            template = None
            raise
        return template
    
    @staticmethod
    def enable_template(id: Optional[int] = None, name: Optional[str] = None) -> Optional[bool]:
        """enable a template by id or name. return True if succeeded and false if the template was already enabled
        Args:
            id (Optional[int], optional): template_id. Defaults to None.
            name (Optional[str], optional): template_name. Defaults to None.
        """
        if (template := TemplateActions.get_template(id=id, name=name)) is None:
            return None

        if template.state == StateEnum.ENABLED:
            return False

        template.state = StateEnum.ENABLED
        db.session.commit()

        return True
    
    @staticmethod
    def disable_template(id: Optional[int] = None, name: Optional[str] = None) -> Optional[bool]:
        """disable a template by id or name if no active environment is dependent on it. return True if succeeded and false if the template was already disabled
        Args:
            id (Optional[int], optional): template_id. Defaults to None.
            name (Optional[str], optional): template_name. Defaults to None.
        """
        if (template := TemplateActions.get_template(id=id, name=name)) is None:
            return None

        if template.state == StateEnum.DISABLED:
            raise TemplateDisabledError("Template is already disabled")

        # to avoid circular import issue
        from .environment import Environment, StatusEnum
        if (active_env := db.session.query(Environment).filter(
            Environment.template_id == template.id,
            Environment.status.in_([StatusEnum.CREATING, StatusEnum.ACTIVE])
            ).first()):
            raise DependencyError("Cannot disable template with an active environment.")

        template.state = StateEnum.DISABLED
        db.session.commit()

        return True