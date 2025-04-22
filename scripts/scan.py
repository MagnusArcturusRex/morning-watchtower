# scripts/scan.py

import pandas as pd

# --- Configurable Filter Criteria ---
MIN_PRICE = 1.05
MAX_PRICE = 10.00
MIN_VOLUME = 1_000_000
MIN_PERCENT_CHANGE = 5.0
MIN_VOLUME_INDEX = 100  # Optional/custom metric

def mock_premarket_data():
    """Mock data simulating premarket movers. Replace with live data fetch later."""
    return pd.DataFrame([
        {'symbol': 'ABC', 'price': 2.10, 'volume': 2_500_000, 'percent_change': 8.5, 'volume_index': 120},
        {'symbol': 'XYZ', 'price': 0.98, 'volume': 3_000_000, 'percent_change': 15.2, 'volume_index': 180},
        {'symbol': 'DEF', 'price': 7.25, 'volume': 900_000,  'percent_change': 4.9, 'volume_index': 95},
        {'symbol': 'LMN', 'price': 9.60, 'volume': 1_500_000, 'percent_change': 5.1, 'volume_index': 110},
    ])

def filter_stocks(df):
    """Apply Morning Watchtower filters."""
    return df[
        (df['price'] >= MIN_PRICE) &
        (df['price'] <= MAX_PRICE) &
        (df['volume'] >= MIN_VOLUME) &
        (df['percent_change'] >= MIN_PERCENT_CHANGE) &
        (df['volume_index'] >= MIN_VOLUME_INDEX)
    ]

def save_filtered_data(df, path='data/filtered_watchlist.csv'):
    df.to_csv(path, index=False)
    print(f"Filtered data saved to: {path}")

def main():
    print("Fetching premarket data...")
    raw_data = mock_premarket_data()

    print("Filtering stocks based on criteria...")
    filtered = filter_stocks(raw_data)

    print(filtered)
    save_filtered_data(filtered)

if __name__ == "__main__":
    main()
