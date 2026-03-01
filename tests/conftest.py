"""
Pytest configuration and fixtures
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from src.config.database import Base
from src.main import app


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session"""
    TestingSessionLocal = sessionmaker(bind=test_engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="module")
def test_client():
    """Create test client"""
    return TestClient(app)
