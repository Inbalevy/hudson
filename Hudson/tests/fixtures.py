import pytest
from hudson.models import Template, Environment, StatusEnum
from datetime import datetime
import pytest
from hudson.app import db, create_app


@pytest.fixture(scope='session', autouse=True)
def test_session(app): 
    with app.app_context():
        try:
            db.create_all()
            yield db.session   
        finally:
            db.drop_all()
            db.session.remove


@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
            

@pytest.fixture()
def template(test_session):
    # Create a new Template
    template = Template(name='Example Template', url='https://example.com/template', state="ENABLED", creation_time=datetime.now())
    test_session.add(template)
    test_session.commit()
    yield template
    test_session.delete(template)
    test_session.commit()

    
@pytest.fixture()
def disabled_template(test_session):
    # Create a new desabled Template
    template = Template(name='Example Disabled Template', url='https://example.com/disabled_template', state="DISABLED", creation_time=datetime.now())
    test_session.add(template)
    test_session.commit()
    yield template
    test_session.delete(template)
    test_session.commit()

    
@pytest.fixture()
def unused_template(test_session):
    # Create a new desabled Template
    template = Template(name='Example Unused Template', url='https://example.com/unused_template', state="ENABLED", creation_time=datetime.now())
    test_session.add(template)
    test_session.commit()
    yield template
    test_session.delete(template)
    test_session.commit()
        
    
@pytest.fixture()
def environment(test_session, template):
    # Create a new Environment associated with the Template
    environment = Environment(name='Example Environment', template_id=template.id, status=StatusEnum.CREATING, creation_time=datetime.now())
    test_session.add(environment)
    test_session.commit()
    yield environment
    test_session.delete(environment)
    test_session.commit()
        
    
@pytest.fixture()
def destroyed_environment(test_session, template):
    # Create a new Environment associated with the Template
    environment = Environment(name='Example Destroyed Environment', template_id=template.id, status=StatusEnum.DESTROYED, creation_time=datetime.now())
    test_session.add(environment)
    test_session.commit()
    yield environment
    test_session.delete(environment)
    test_session.commit()