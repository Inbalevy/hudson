import pytest
from datetime import datetime

from hudson.models import Template, TemplateActions, StateEnum
from .fixtures import template, disabled_template, unused_template, environment, test_session, client
    
    
def test_list_templates(template, disabled_template, client):
    no_filter = client.get('/templates')
    assert no_filter.status_code == 200
    assert len(no_filter.json) == 2
    
    filtered = client.get("/templates?only_enabled=true")
    assert filtered.status_code == 200
    assert len(filtered.json) == 1
    assert filtered.json[0]['state'] == "ENABLED"
    
    
# def test_get_template_details(template):
#     template_by_id = TemplateActions.get_template(id = template.id)
#     assert template_by_id == template
    
#     template_by_name = TemplateActions.get_template(name = template.name)
#     assert template_by_name == template
    
#     assert TemplateActions.get_template(name = "non_existing_name") is None
    

# def test_create_template():
#     new_tempalte = TemplateActions.create_template(github_url='https://example.com/created_template', name='Created Template')
#     assert isinstance(new_tempalte, Template)
#     assert TemplateActions.get_template(new_tempalte.id) == new_tempalte
    

# def test_enable_template(template, disabled_template):
#     assert TemplateActions.enable_template(disabled_template.id) == True
#     assert TemplateActions.enable_template(template.id) == False


# def test_disable_template(template, disabled_template, unused_template, environment):
#     assert TemplateActions.disable_template(unused_template.id) == True
#     assert TemplateActions.disable_template(disabled_template.id) == False
#     with pytest.raises(ValueError):
#         TemplateActions.disable_template(template.id)