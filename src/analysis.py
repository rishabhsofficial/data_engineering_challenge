import sqlite3
import logging
from datetime import datetime
from src.database import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_top_rated_products():
    """Retrieve top 3 rated products for each month and format month names."""
    conn = get_db_connection()
    cursor = conn.cursor()

    logging.info("Fetching top-rated products for each month...")

    cursor.execute("""
        SELECT month, product_id, avg_rating
        FROM (
            SELECT 
                month,
                product_id,
                ROUND(avg_rating,2) as avg_rating,
                RANK() OVER (PARTITION BY month ORDER BY avg_rating DESC) AS rank
            FROM RatingsMonthlyAggregates
        ) 
        WHERE rank <= 3;
    """)

    results = cursor.fetchall()
    conn.close()

    logging.info(f"Total top-rated records found: {len(results)}")

    # Convert YYYY-MM format to full month name
    formatted_results = []
    for month, product_id, avg_rating in results:
        month_name = datetime.strptime(month, "%Y-%m").strftime("%B %Y")  # Convert to "January 2024"
        formatted_results.append((month_name, product_id, avg_rating))

    return formatted_results

if __name__ == "__main__":
    top_products = get_top_rated_products()
    for row in top_products:
        print(row)  # Prints ("January 2024", 432, 4.9)
