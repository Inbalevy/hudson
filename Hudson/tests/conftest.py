import pytest
from hudson.models.base import Base, ENGINE, Session

@pytest.fixture(scope='session')
def db():
    try:
        with Session() as session:
            Base.metadata.create_all(bind=ENGINE)
            yield session
    finally:
        Base.metadata.drop_all(bind=ENGINE)