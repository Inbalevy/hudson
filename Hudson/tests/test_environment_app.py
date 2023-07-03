from hudson.models.template import TemplateActions
from .fixtures import template, disabled_template, environment, destroyed_environment, test_session, client
from hudson.models import Template, Environment, EnvironmentActions, StatusEnum
    
    
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
    
    
def test_create_environment(template, disabled_template, test_session, client):
    data = {
        'template_name': 'Example Template',
        'environment_name': 'test create env',
    }
    response = client.post('/environment', data=data)
    assert response.status_code == 201
    assert response.json['name'] == 'test create env'
    assert response.json['template_id'] == TemplateActions.get_template(name='Example Template').id
    assert response.json['status'] == StatusEnum.CREATING.value
    
    bad_data = {'template_name': disabled_template.name, 'environment_name': "test create env"}
    assert client.post('/environment', data=bad_data).status_code == 500
    test_session.delete(EnvironmentActions.get_environment(name='test create env'))
    test_session.commit()
    

def test_update_env_status(environment, client):
    assert environment.status == StatusEnum.CREATING
    assert client.put(f'/environment?name={environment.name}').status_code == 200
    assert environment.status == StatusEnum.ACTIVE
    assert client.put(f'/environment?name={environment.name}').status_code == 200
    assert environment.status == StatusEnum.DESTROYING
    assert client.put(f'/environment?name={environment.name}').status_code == 200
    assert environment.status == StatusEnum.DESTROYED
    assert client.put(f'/environment?name={environment.name}').status_code == 400
