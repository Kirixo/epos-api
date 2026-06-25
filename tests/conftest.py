import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.infra.db.models.base import Base
from app.infra.db.models.models import User, UserSettings, RevokedToken, AuditLog  # Ensure models are imported
from app.di.dependencies import get_uow_factory
from app.infra.db.guow import GeneralUnitOfWorkFactory

# Create in-memory SQLite database with StaticPool for testing
from sqlalchemy.pool import StaticPool
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function", autouse=True)
def clean_db() -> None:
    # Clean up database tables before each test
    connection = engine.connect()
    transaction = connection.begin()
    
    # Delete data from all tables
    for table in reversed(Base.metadata.sorted_tables):
        connection.execute(table.delete())
        
    transaction.commit()
    connection.close()

def override_get_uow_factory() -> GeneralUnitOfWorkFactory:
    return GeneralUnitOfWorkFactory(TestingSessionFactory)

# Override the dependency in the app
app.dependency_overrides[get_uow_factory] = override_get_uow_factory

from typing import Generator
@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
