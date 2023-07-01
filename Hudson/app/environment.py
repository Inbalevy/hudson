from datetime import datetime
import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum
from typing import Optional
from .base import Base, Session

class StatusEnum(enum.Enum):
    CREATING = 1
    ACTIVE = 2
    DESTROYING = 3
    DESTROYED = 4


class Environment(Base):
    __tablename__ = 'environments'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    template_id = Column(Integer, nullable=False)
    status = Column(Enum(StatusEnum), default=StatusEnum.CREATING)
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
        with Session() as session:
            environments = session.query(Environment)
            
            # Assuming that if a user has chosen a specific filter it should override the default filter
            if not (status or name) and exclude_destroyed:
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
    
        with Session() as session:
            query = session.query(Environment)
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
        with Session() as session:
            try:
                # to avoid circular import 
                from .template import TemplateActions
                
                template = TemplateActions.get_template(name=template_name)
                if not template or template.state == "DISABLED":
                    raise ValueError("the requested template is disabled or not found")
                env = Environment(name=environment_name, template_id=template.id, status=StatusEnum.CREATING, creation_time=datetime.now())
                
                session.add(env)
                session.commit()
                session.refresh(env)
            
            except Exception as e:
                env = None
                session.rollback()
                raise
        return env
        
    @staticmethod
    def update_environment_status(id: Optional[int] = None, name: Optional[str] = None) -> StatusEnum:
        """update an environment by id or name. return True if succeeded and false if the template was already enabled
        Args:
            id (Optional[int], optional): template_id. Defaults to None.
            name (Optional[str], optional): template_name. Defaults to None.
        """
        if (env := EnvironmentActions.get_environment(id=id, name=name)) is None:
            raise ValueError("Environment not found")
        
        with Session() as session:
            update_env = session.query(Environment).filter(Environment.id == env.id).one()
            current_status = update_env.status
            
            if current_status == StatusEnum.DESTROYED:
                raise ValueError("Destroyed environment cannot be updated")

            update_env.status = StatusEnum(current_status.value + 1)
            session.commit()
            session.refresh(update_env)
            
            return update_env.status