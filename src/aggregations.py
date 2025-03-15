import sqlite3
import logging
from src.database import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def truncate_aggregates_table():
    """Truncate only the RatingsMonthlyAggregates table before inserting new aggregates."""
    conn = get_db_connection()
    cursor = conn.cursor()

    logging.warning("Truncating RatingsMonthlyAggregates table before inserting new aggregates...")
    cursor.execute("DELETE FROM RatingsMonthlyAggregates;")
    conn.commit()
    conn.close()

    logging.info("RatingsMonthlyAggregates table truncated successfully!")

def compute_monthly_aggregates():
    """Compute monthly average ratings per product."""
    conn = get_db_connection()
    cursor = conn.cursor()

    logging.info("Computing monthly aggregates...")

    cursor.execute("""
        INSERT INTO RatingsMonthlyAggregates (month, product_id, avg_rating)
        SELECT 
            strftime('%Y-%m', timestamp) AS month,
            product_id,
            AVG(rating) AS avg_rating
        FROM Ratings
        GROUP BY month, product_id;
    """)

    conn.commit()

    # Log the total count of records inserted
    cursor.execute("SELECT COUNT(*) FROM RatingsMonthlyAggregates;")
    total_records = cursor.fetchone()[0]
    logging.info(f"Total records in RatingsMonthlyAggregates table: {total_records}")

    conn.close()

if __name__ == "__main__":
    truncate_aggregates_table()  # Only truncate the aggregate table
    compute_monthly_aggregates()
