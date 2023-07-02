import pytest
from datetime import datetime

from hudson.models import Template, TemplateActions
from .db_fixtures import template, disabled_template, unused_template, environment, test_session, client
    

def test_add_template(template, test_session):
    # Query the Template from the database
    saved_template = test_session.query(Template).filter_by(id=template.id).first()

    # Assert that the saved data matches the desired values
    assert saved_template.name == 'Example Template'
    assert saved_template.url == 'https://example.com/template'
    assert saved_template.state == 'ENABLED'
    
def test_list_templates(template, disabled_template):
    assert len(TemplateActions.list_templates()) == 2
    filtered_templates = TemplateActions.list_templates(True)
    assert len(filtered_templates) == 1
    assert template in filtered_templates and disabled_template not in filtered_templates
    
    
def test_get_template_details(template):
    template_by_id = TemplateActions.get_template(id = template.id)
    assert template_by_id == template
    
    template_by_name = TemplateActions.get_template(name = template.name)
    assert template_by_name == template
    
    assert TemplateActions.get_template(name = "non_existing_name") is None
    

def test_create_template():
    new_tempalte = TemplateActions.create_template(github_url='https://example.com/created_template', name='Created Template')
    assert isinstance(new_tempalte, Template)
    assert TemplateActions.get_template(new_tempalte.id) == new_tempalte
    

def test_enable_template(template, disabled_template):
    assert TemplateActions.enable_template(disabled_template.id) == True
    assert TemplateActions.enable_template(template.id) == False


def test_disable_template(template, disabled_template, unused_template, environment):
    assert TemplateActions.disable_template(unused_template.id) == True
    assert TemplateActions.disable_template(disabled_template.id) == False
    with pytest.raises(ValueError):
        TemplateActions.disable_template(template.id)