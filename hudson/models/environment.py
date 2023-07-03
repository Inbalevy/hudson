from datetime import datetime
import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from typing import Optional
from hudson.database import db
from hudson.models.template import StateEnum

class StatusEnum(enum.IntEnum):
    CREATING = 1
    ACTIVE = 2
    DESTROYING = 3
    DESTROYED = 4


class EnvironmentDestroyedError(Exception):
    pass


class TemplateDisabledError(Exception):
    pass


class EnvironmentNameUnavailable(Exception):
    pass


class Environment(db.Model):
    """Environment model for the DB

    Args:
        Base: sqlalchemy declarative_base
    """
    __tablename__ = 'environments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'), nullable=False)
    status = db.Column(db.Enum(StatusEnum), default=StatusEnum.CREATING)
    creation_time = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Environment(id={self.id}, name='{self.name}', template='{self.template_id}', status={self.status}, creation_time='{self.creation_time}')"
    
    def __eq__(self, other):
        if isinstance(other, Environment):
            return self.id == other.id
        
class EnvironmentActions(): 
    @staticmethod   
    def list_environments(exclude_destroyed: bool = True, name: Optional[str] = None, status: Optional[list[StatusEnum]] = None) -> list[Environment]:
        """list all existing environments in the db. by default, shows only non-destroyed environments. 
        if one or more specific filter is applied, it will override the default filter

        Args:
            exclude_destroyed (bool, optional): apply default filter exclude_destroyed envs. Defaults to True.
            name (str, optional): filter by name. Defaults to None.
            status (list[StatusEnum], optional): filter by status. Defaults to None.

        Returns:
            list: Environment
        """
        environments = db.session.query(Environment)
        
        # Assuming that if a user has chosen a specific filter it should override the default filter
        if exclude_destroyed and not (status or name):
            return environments.filter(Environment.status != StatusEnum.DESTROYED).all()
        
        if status:
            environments = environments.filter(Environment.status.in_(status))
        if name:
            environments = environments.filter(Environment.name == name) 
        return environments.all()
        
    
    @staticmethod
    def get_environment(id: Optional[int]=None, name: Optional[str]=None) -> Optional[Environment]:
        """get environment info, either by id or by name

        Args:
            id (Optional[int], optional): environment_id. Defaults to None.
            name (Optional[str], optional): environment_name. Defaults to None.
        """
        if not (id or name):
            raise ValueError("Either 'id' or 'name' must be provided.")
    
        query = db.session.query(Environment)
        if id is not None:
            return query.filter(Environment.id == id).first()
        elif name is not None:
            return query.filter(Environment.name == name).first()
        return None

    @staticmethod
    def create_environment(template_name: str, environment_name: str) -> Optional[Environment]:
        """create a new environment by template_name and name
        
        Args:
            template_name (str): a valid template ID
            environment_name (Optional): a new unique name
        """         
        try:
            # to avoid circular import 
            from .template import TemplateActions
            
            template = TemplateActions.get_template(name=template_name)
            if not template or template.state == StateEnum.DISABLED:
                raise TemplateDisabledError("the requested template is disabled or not found")
            if EnvironmentActions.get_environment(name=environment_name) is not None:
                raise EnvironmentNameUnavailable("Looks like there is already an existing environment with that name.")
            env = Environment(name=environment_name, template_id=template.id, status=StatusEnum.CREATING, creation_time=datetime.now().isoformat())
            
            db.session.add(env)
            db.session.commit()
            db.session.refresh(env)
        
        except Exception as e:
            env = None
            raise
        return env
        
    @staticmethod
    def update_environment_status(id: Optional[int] = None, name: Optional[str] = None) -> StatusEnum:
        """update an environment by id or name. return the new environment status and raise if the environment was already destroyed
        Args:
            id (Optional[int], optional): template_id. Defaults to None.
            name (Optional[str], optional): template_name. Defaults to None.
        """
        if (env := EnvironmentActions.get_environment(id=id, name=name)) is None:
            return None
        
        update_env = db.session.query(Environment).filter(Environment.id == env.id).one()
        current_status = update_env.status
        
        if current_status == StatusEnum.DESTROYED:
            raise EnvironmentDestroyedError("Destroyed environment cannot be updated")

        update_env.status = StatusEnum(current_status.value + 1)
        db.session.commit()
        db.session.refresh(update_env)
        
        return update_env.status