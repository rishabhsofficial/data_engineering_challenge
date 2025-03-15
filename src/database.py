import sqlite3
import logging
from src.config import DATABASE_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

def create_tables():
    """Create required tables in SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    logging.info("Creating tables...")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ratings (
            timestamp TEXT,
            user_id INTEGER,
            product_id INTEGER,
            rating INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS RatingsMonthlyAggregates (
            month TEXT,
            product_id INTEGER,
            avg_rating FLOAT
        );
    """)

    conn.commit()
    conn.close()
    logging.info("Tables created successfully!")

def cleanup_tables():
    """Cleanup tables before inserting new records to avoid duplicates."""
    conn = get_db_connection()
    cursor = conn.cursor()

    logging.warning("Cleaning up tables before inserting new records...")

    cursor.execute("DELETE FROM Ratings;")
    cursor.execute("DELETE FROM RatingsMonthlyAggregates;")
    conn.commit()
    conn.close()

    logging.info("Tables cleaned up successfully!")

if __name__ == "__main__":
    create_tables()
    cleanup_tables()
