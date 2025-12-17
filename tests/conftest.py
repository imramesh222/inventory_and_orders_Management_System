import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from inventoryordersapi.core.database import get_db
from inventoryordersapi.model.item_record import Base as ItemBase
from inventoryordersapi.model.order_record import Base as OrderBase
from inventoryordersapi.main import app

# Get test DB URL from environment variable, fallback to default
SQLALCHEMY_TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:ramesh@localhost:5432/inventory_db"
)

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize database: drop all tables and recreate for a clean state
def init_db():
    ItemBase.metadata.drop_all(bind=engine)
    OrderBase.metadata.drop_all(bind=engine)
    ItemBase.metadata.create_all(bind=engine)
    OrderBase.metadata.create_all(bind=engine)

# Fixture for engine scoped to session
@pytest.fixture(scope="session")
def db_engine():
    init_db()
    yield engine

# Fixture for a clean db session for each test function
@pytest.fixture(scope="function")
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# Fixture for TestClient with dependency override
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

