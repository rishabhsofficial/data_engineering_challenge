from src.database import get_db_connection, create_tables, cleanup_tables
from src.data_generator import generate_ratings

def test_generate_ratings():
    conn = get_db_connection()
    create_tables()
    cleanup_tables()

    generate_ratings(n=1000)

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Ratings;")
    count = cursor.fetchone()[0]

    assert count == 1000

    conn.close()
