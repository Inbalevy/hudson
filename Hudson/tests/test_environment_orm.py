import pytest
from datetime import datetime
from requests import get, post, put, patch, delete

from hudson.models import Template, Environment, EnvironmentActions, StatusEnum
from .fixtures import template, disabled_template, environment, destroyed_environment, test_session
    

def test_add_environment(environment, test_session):
    saved_environment = test_session.query(Environment).filter_by(id=environment.id).first()
    assert saved_environment.name == 'Example Environment'
    assert saved_environment.id == environment.id
    assert saved_environment.status == StatusEnum.CREATING
    
    
def test_list_environments(environment, destroyed_environment):
    assert len(EnvironmentActions.list_environments(exclude_destroyed=False)) == 2
    
    filtered_envs = EnvironmentActions.list_environments(exclude_destroyed=True)
    assert len(filtered_envs) == 1
    assert environment in filtered_envs and destroyed_environment not in filtered_envs
    
    assert len(EnvironmentActions.list_environments(name='Example Environment')) == 1
    assert len(EnvironmentActions.list_environments(status=[StatusEnum.CREATING, StatusEnum.ACTIVE])) == 1
    
    
def test_get_environment_details(environment):
    environment_by_id = EnvironmentActions.get_environment(id = environment.id)
    assert environment_by_id == environment
    
    environment_by_name = EnvironmentActions.get_environment(name = environment.name)
    assert environment_by_name == environment
    
    assert EnvironmentActions.get_environment(name = "non_existing_name") is None
    
    
def test_create_environment(template, disabled_template, test_session):
    new_env = EnvironmentActions.create_environment(template_name=template.name, environment_name='Created Env')
    assert isinstance(new_env, Environment)
    assert EnvironmentActions.get_environment(new_env.id) == new_env
    with pytest.raises(ValueError):
        EnvironmentActions.create_environment(template_name=disabled_template.name, environment_name='Bad Env')
    test_session.delete(new_env)
    test_session.commit()


def test_update_env_status(environment):
    assert environment.status == StatusEnum.CREATING
    assert EnvironmentActions.update_environment_status(environment.id) == StatusEnum.ACTIVE
    assert EnvironmentActions.update_environment_status(environment.id) == StatusEnum.DESTROYING
    assert EnvironmentActions.update_environment_status(environment.id) == StatusEnum.DESTROYED
    with pytest.raises(ValueError):
        EnvironmentActions.update_environment_status(environment.id)
