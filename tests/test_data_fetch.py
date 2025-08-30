from aerialview.core.data_fetch import fetch_stock_data

def test_fetch_stock_data():
    df = fetch_stock_data("AAPL", "2023-01-01", "2023-02-01")
    assert df is not None
    assert "close" in df.columns