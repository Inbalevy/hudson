from .fixtures import template, disabled_template, environment, destroyed_environment, test_session, client
from hudson.models import Template, Environment, EnvironmentActions, StatusEnum
    

# def test_add_environment(environment, test_session):
#     saved_environment = test_session.query(Environment).filter_by(id=environment.id).first()
#     assert saved_environment.name == 'Example Environment'
#     assert saved_environment.id == environment.id
#     assert saved_environment.status == StatusEnum.CREATING
    
    
def test_list_environments(environment, destroyed_environment, client):
    no_filter = client.get('/environments?exclude_destroyed=false')
    assert no_filter.status_code == 200
    assert len(no_filter.json) == 2
    
    default_filter = client.get('/environments')
    assert default_filter.status_code == 200
    assert len(default_filter.json) == 1
    
    assert len(client.get('/environments?name=Example Environment').json) == 1
    assert len(client.get('/environments?status=[1, 2]').json) == 1
    
    
def test_get_environment_details(environment, client):
    response = client.get(f'/environment?name={environment.name}')
    assert response.status_code == 200
    assert response.json['id'] == environment.id

    assert client.get(f'/environment?name=nonExistingName').status_code == 404
    
    
# def test_create_environment(template, disabled_template, test_session):
#     new_env = EnvironmentActions.create_environment(template_name=template.name, environment_name='Created Env')
#     assert isinstance(new_env, Environment)
#     assert EnvironmentActions.get_environment(new_env.id) == new_env
#     with pytest.raises(ValueError):
#         EnvironmentActions.create_environment(template_name=disabled_template.name, environment_name='Bad Env')
#     test_session.delete(new_env)
#     test_session.commit()


def test_update_env_status(environment):
    assert environment.status == StatusEnum.CREATING

    assert EnvironmentActions.update_environment_status(environment.id) == StatusEnum.ACTIVE
    assert EnvironmentActions.update_environment_status(environment.id) == StatusEnum.DESTROYING
    assert EnvironmentActions.update_environment_status(environment.id) == StatusEnum.DESTROYED
    with pytest.raises(ValueError):
        EnvironmentActions.update_environment_status(environment.id)
