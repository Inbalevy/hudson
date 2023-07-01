import pytest
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from hudson.app import Template, Environment, Base
from datetime import datetime

# Set up the database connection (with logging)

engine = sqlalchemy.create_engine('postgresql://hudsondb:HouseOfTemplates@db:5432/hudsondb', echo=True)
    
@pytest.fixture(scope='session')
def template(db):
    # Create a new Template
    template = Template(name='Example Template', url='https://example.com/template', state="ENABLED", creation_time=datetime.now())
    db.add(template)
    db.commit()
    yield template
    db.delete(template)
    db.commit()


@pytest.fixture
def environment(db, template):
    # Create a new Environment associated with the Template
    environment = Environment(name='Example Environment', template_id=template.id, status='CREATING', creation_time=datetime.now())
    db.add(environment)
    db.commit()
    yield environment
    db.delete(environment)
    db.commit()


def test_add_template_and_environment(db, template, environment):
    # Query the Template and Environment from the database
    saved_template = db.query(Template).filter_by(id=template.id).first()
    saved_environment = db.query(Environment).filter_by(id=environment.id).first()

    # Assert that the saved data matches the desired values
    assert saved_template.name == 'Example Template'
    assert saved_template.url == 'https://example.com/template'
    assert saved_template.state == 'ENABLED'

    assert saved_environment.name == 'Example Environment'
    assert saved_environment.template_id == template.id
    assert saved_environment.status == 'CREATING'
    
    
def test_list_templates(template):
    templates = Template.list_templates()
    print(templates)
    assert len(templates) == 1
    assert template in templates