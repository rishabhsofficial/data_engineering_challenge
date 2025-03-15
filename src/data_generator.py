import sqlite3
import random
import logging
from datetime import datetime, timedelta
from src.database import get_db_connection, cleanup_tables

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_random_date():
    """Generate a random date in 2024."""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

def generate_ratings(n=100000):
    """Generate and insert random ratings into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    logging.info(f"Generating {n} random ratings...")

    data = [
        (generate_random_date(), random.randint(1, 1000), random.randint(1, 1000), random.randint(1, 5))
        for _ in range(n)
    ]

    cursor.executemany("INSERT INTO Ratings (timestamp, user_id, product_id, rating) VALUES (?, ?, ?, ?);", data)
    conn.commit()

    # Log the total count of records inserted
    cursor.execute("SELECT COUNT(*) FROM Ratings;")
    total_records = cursor.fetchone()[0]
    logging.info(f"Total records in Ratings table: {total_records}")

    conn.close()

if __name__ == "__main__":
    cleanup_tables()  # Ensure we start with an empty table
    generate_ratings()
