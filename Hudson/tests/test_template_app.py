from .fixtures import template, disabled_template, unused_template, environment, test_session, client
from hudson.models import Template, TemplateActions, StateEnum
from hudson.models.template import BadStateError, DependencyError
    
def test_list_templates(template, disabled_template, client):
    no_filter = client.get('/templates')
    assert no_filter.status_code == 200
    assert len(no_filter.json) == 2
    
    filtered = client.get("/templates?only_enabled=true")
    assert filtered.status_code == 200
    assert len(filtered.json) == 1
    assert filtered.json[0]['state'] == "ENABLED"
    
    
def test_get_template_details(template, client):
    response = client.get(f'/template?name={template.name}')
    assert response.status_code == 200
    assert response.json['id'] == template.id

    assert client.get(f'/template?name=nonExistingName').status_code == 404
    

# def test_create_template():
#     new_tempalte = TemplateActions.create_template(github_url='https://example.com/created_template', name='Created Template')
#     assert isinstance(new_tempalte, Template)
#     assert TemplateActions.get_template(new_tempalte.id) == new_tempalte
    

def test_enable_template(template, disabled_template, unused_template, client):
    response = client.put(f'/template?name={template.name}')
    assert response.status_code == 400
    response = client.put(f'/template?name={disabled_template.name}')
    assert response.status_code == 200
    assert template.state == StateEnum.ENABLED
    assert client.put(f'/template?name=nonExistingName').status_code == 404


def test_disable_template(template, disabled_template, unused_template, environment, client):
    response = client.patch(f'/template?name={unused_template.name}')
    assert response.status_code == 200
    assert unused_template.state == StateEnum.DISABLED
    assert client.patch(f'/template?name={disabled_template.name}').status_code == 400
    assert client.patch(f'/template?name={template.name}').status_code == 409
