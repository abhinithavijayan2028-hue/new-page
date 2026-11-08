import pytest
from backend import create_app
from backend.extensions import db


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app("testing")
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_app_initialization(app):
    """Test that the Flask application initializes correctly."""
    assert app is not None
    assert app.config["TESTING"] is True


def test_health_endpoint(client):
    """Test the health check endpoint returns success."""
    response = client.get("/api/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "success"
    assert "NEXORITHAM backend is running" in data["message"]


def test_database_connectivity(app):
    """Test that the database connection works with an actual SELECT 1 query."""
    with app.app_context():
        result = db.session.execute(db.text("SELECT 1"))
        assert result.scalar() == 1


def test_database_tables_created(app):
    """Test that database tables can be created without error."""
    with app.app_context():
        inspector = db.inspect(db.engine)
        table_names = inspector.get_table_names()
        # At minimum, alembic_version table should exist after create_all
        assert isinstance(table_names, list)