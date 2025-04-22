# scripts/scan.py
from watchlist_sources.finviz import get_finviz_gainers
from watchlist_sources.stocktwits import get_stocktwits_trending
import yfinance as yf
import pandas as pd
from datetime import datetime
from tqdm import tqdm


# --- Configurable Filter Criteria ---
MIN_PRICE = 1.05
MAX_PRICE = 10.00
MIN_VOLUME = 1_000_000
MIN_PERCENT_CHANGE = 5.0

# Watchlist to scan — replace or load from CSV later
# default_watchlist = ["TTOO", "HOLO", "SNTI"]

def is_valid_ticker(ticker):
    try:
        info = yf.Ticker(ticker).info
        return info.get("regularMarketPrice") is not None
    except Exception:
        return False
        
def build_master_watchlist():
    try:
        finviz = get_finviz_gainers()
    except Exception as e:
        print("Finviz error:", e)
        finviz = []

    try:
        stocktwits = get_stocktwits_trending()
    except Exception as e:
        print("StockTwits error:", e)
        stocktwits = []

    combined = list(set(default_watchlist + finviz + stocktwits))
    return combined


def fetch_realtime_data(tickers):
    print(f"Fetching real-time data for {len(tickers)} symbols...")
    data = []

    for symbol in tickers:
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            price = info.get("regularMarketPrice")
            prev_close = info.get("regularMarketPreviousClose")
            volume = info.get("regularMarketVolume")

            if not price or not prev_close or not volume:
                continue

            percent_change = ((price - prev_close) / prev_close) * 100

            data.append({
                "symbol": symbol,
                "price": price,
                "volume": volume,
                "percent_change": round(percent_change, 2),
            })
        except Exception as e:
            print(f"Error fetching {symbol}: {e}")

    return pd.DataFrame(data)

def filter_stocks(df):
    """Apply Morning Watchtower filters."""
    return df[
        (df['price'] >= MIN_PRICE) &
        (df['price'] <= MAX_PRICE) &
        (df['volume'] >= MIN_VOLUME) &
        (df['percent_change'] >= MIN_PERCENT_CHANGE)
    ]

def save_filtered_data(df):
    today = datetime.now().strftime("%Y-%m-%d")
    path = f"data/filtered_watchlist_{today}.csv"
    df.to_csv(path, index=False)
    print(f"Filtered data saved to: {path}")

def main():
    # STEP 1: Gather hot stocks from sources
    stocktwits_list = get_stocktwits_trending()
    finviz_list = get_finviz_gainers()

    # Combine them (you can add ThinkorSwim or other sources here too)
    raw_symbols = list(set(stocktwits_list + finviz_list))
    WATCHLIST = [symbol for symbol in tqdm(raw_symbols, desc="Validating tickers") if is_valid_ticker(symbol)]

    if not WATCHLIST:
        print("⚠️ No stocks found from any source.")
        return

    print(f"📊 Master Watchlist: {WATCHLIST}")
    raw_data = fetch_realtime_data(WATCHLIST)
    print("Raw data:")
    print(raw_data)

    filtered = filter_stocks(raw_data)
    print("\nFiltered Watchlist:")
    print(filtered)

    save_filtered_data(filtered)
    save_markdown(filtered)

def save_markdown(df):
    today = datetime.now().strftime("%Y-%m-%d")
    md_path = f"data/filtered_watchlist_{today}.md"
    
    with open(md_path, "w") as f:
        f.write(f"# Morning Watchtower – {today}\n\n")
        f.write("| Symbol | Price | Volume | % Change |\n")
        f.write("|--------|-------|--------|----------|\n")
        for _, row in df.iterrows():
            f.write(f"| {row['symbol']} | ${row['price']:.2f} | {row['volume']:,} | {row['percent_change']}% |\n")
    
    print(f"Markdown file saved to: {md_path}")

if __name__ == "__main__":
    main()
