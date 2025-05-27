import yfinance as yf

def is_tradable(ticker: str) -> bool:
    try:
        stock = yf.Ticker(ticker)
        info = stock.fast_info  # Much faster than .info
        return info.get("lastPrice") is not None and info.get("marketCap") is not None
    except Exception:
        return False
