import pytest
from sqlalchemy import event
from fastapi.testclient import TestClient
from app.database import engine, Base, get_db
from app.main import app
from sqlalchemy.orm import Session

# Open DB connection, wraps in outer transaction, rolls back after test, DB stays uncommitted
@pytest.fixture
def connection():
    connection = engine.connect()
    transaction = connection.begin()
    yield connection
    transaction.rollback()
    connection.close()

# Bind session to connection, savepoint stops app commits from changing real DB
@pytest.fixture
def db_session(connection):
    session = Session(bind=connection)
    session.begin_nested()

    # After each savepoint ends, create a new one so that changes dont affect real DB
    @event.listens_for(Session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()
    
    yield session
    session.close()

# Wire TestClient to test DB session so requests hit rollback protected session, not actual DB
@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()