import pytest
from src.database import create_tables, get_db_connection
from src.data_generator import generate_ratings, cleanup_tables
from src.aggregations import compute_monthly_aggregates
from src.analysis import get_top_rated_products

@pytest.fixture(scope="module")
def setup_database():
    """Setup the test database and return connection."""
    conn = get_db_connection()
    create_tables()
    yield conn
    conn.close()

def test_generate_ratings(setup_database):
    """Test if data is inserted correctly."""
    cleanup_tables()
    generate_ratings(1000)  # Generate a smaller dataset
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Ratings;")
    count = cursor.fetchone()[0]
    assert count == 1000

def test_compute_monthly_aggregates(setup_database):
    """Test if aggregates are computed correctly."""
    compute_monthly_aggregates()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM RatingsMonthlyAggregates;")
    count = cursor.fetchone()[0]
    assert count > 0

def test_get_top_rated_products(setup_database):
    """Test if top products retrieval works."""
    top_products = get_top_rated_products()
    assert len(top_products) > 0
