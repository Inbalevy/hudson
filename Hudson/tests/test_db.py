import pytest
import sqlalchemy
from sqlalchemy.exc import IntegrityError
from app import Template, Environment, Base

# Set up the database connection
@pytest.fixture(autouse=True)
def engine():
    engine = sqlalchemy.create_engine('postgresql://hudsondb:HouseOfTemplates@db:5432/hudsondb')
Session = sqlalchemy.orm.sessionmaker(bind=engine)
session = Session()

@pytest.fixture(autouse=True)
def setup():
    # Create the database tables
    Base.metadata.create_all(engine)
    yield
    # Drop the tables after each test
    Base.metadata.drop_all(engine)

def test_add_template_and_environment():
    # Create a new Template
    template = Template(name='Example Template', url='https://example.com/template', state=True)
    session.add(template)
    session.commit()

    # Create a new Environment associated with the Template
    environment = Environment(name='Example Environment', template_id=template.id, status='ACTIVE')
    session.add(environment)
    session.commit()

    # Query the Template and Environment from the database
    saved_template = session.query(Template).filter_by(id=template.id).first()
    saved_environment = session.query(Environment).filter_by(id=environment.id).first()

    # Assert that the saved data matches the desired values
    assert saved_template.name == 'Example Template'
    assert saved_template.url == 'https://example.com/template'
    assert saved_template.state == True

    assert saved_environment.name == 'Example Environment'
    assert saved_environment.template_id == template.id
    assert saved_environment.status == 'ACTIVE'