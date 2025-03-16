from src.database import get_db_connection, create_tables

def test_create_tables():
    # Connection Setup
    conn = get_db_connection()
    create_tables()

    # Test
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    assert 'Ratings' in tables
    assert 'RatingsMonthlyAggregates' in tables

    conn.close()
