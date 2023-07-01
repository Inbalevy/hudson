import pytest
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from hudson.app import Template, Environment, Base
from datetime import datetime

# Set up the database connection (with logging)
engine = sqlalchemy.create_engine('postgresql://hudsondb:HouseOfTemplates@db:5432/hudsondb', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


@pytest.fixture(autouse=True)
def setup_db():
    try:
        # Create the database tables
        Base.metadata.create_all(engine)
        yield
    finally:
        # Drop the tables after each test
        Base.metadata.drop_all(engine)
  
    
@pytest.fixture
def template():
    # Create a new Template
    template = Template(name='Example Template', url='https://example.com/template', state="ENABLED", creation_time=datetime.now())
    session.add(template)
    session.commit()
    yield template


@pytest.fixture
def environment(template):
    # Create a new Environment associated with the Template
    environment = Environment(name='Example Environment', template_id=template.id, status='CREATING', creation_time=datetime.now())
    session.add(environment)
    session.commit()
    yield environment


def test_add_template_and_environment(template, environment):
    # Query the Template and Environment from the database
    saved_template = session.query(Template).filter_by(id=template.id).first()
    saved_environment = session.query(Environment).filter_by(id=environment.id).first()

    # Assert that the saved data matches the desired values
    assert saved_template.name == 'Example Template'
    assert saved_template.url == 'https://example.com/template'
    assert saved_template.state == 'ENABLED'

    assert saved_environment.name == 'Example Environment'
    assert saved_environment.template_id == template.id
    assert saved_environment.status == 'CREATING'