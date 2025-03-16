from src.analysis import get_top_rated_products

def test_get_top_rated_products():
    results = get_top_rated_products()
    # Check that results return top 3 products per month
    assert len(results) > 0
    for row in results:
        assert len(row) == 3  # (month_name, product_id, avg_rating)
