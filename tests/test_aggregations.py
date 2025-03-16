from src.database import get_db_connection, create_tables, cleanup_tables
from src.data_generator import generate_ratings
from src.aggregations import compute_monthly_aggregates

def test_compute_monthly_aggregates():
    conn = get_db_connection()
    create_tables()
    cleanup_tables()
    generate_ratings(n=1000)
    compute_monthly_aggregates()

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM RatingsMonthlyAggregates;")
    count = cursor.fetchone()[0]

    assert count > 0  # Should have some aggregated data

    conn.close()
