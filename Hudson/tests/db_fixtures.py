import pytest
from hudson.models import Template, Environment, StatusEnum
from datetime import datetime


@pytest.fixture()
def template(db):
    # Create a new Template
    template = Template(name='Example Template', url='https://example.com/template', state="ENABLED", creation_time=datetime.now())
    db.add(template)
    db.commit()
    yield template
    db.delete(template)
    db.commit()

    
@pytest.fixture()
def disabled_template(db):
    # Create a new desabled Template
    template = Template(name='Example Disabled Template', url='https://example.com/disabled_template', state="DISABLED", creation_time=datetime.now())
    db.add(template)
    db.commit()
    yield template
    db.delete(template)
    db.commit()

    
@pytest.fixture()
def unused_template(db):
    # Create a new desabled Template
    template = Template(name='Example Unused Template', url='https://example.com/unused_template', state="ENABLED", creation_time=datetime.now())
    db.add(template)
    db.commit()
    yield template
    db.delete(template)
    db.commit()
        
    
@pytest.fixture()
def environment(db, template):
    # Create a new Environment associated with the Template
    environment = Environment(name='Example Environment', template_id=template.id, status=StatusEnum.CREATING, creation_time=datetime.now())
    db.add(environment)
    db.commit()
    yield environment
    db.delete(environment)
    db.commit()
        
    
@pytest.fixture()
def destroyed_environment(db, template):
    # Create a new Environment associated with the Template
    environment = Environment(name='Example Destroyed Environment', template_id=template.id, status=StatusEnum.DESTROYED, creation_time=datetime.now())
    db.add(environment)
    db.commit()
    yield environment
    db.delete(environment)
    db.commit()

