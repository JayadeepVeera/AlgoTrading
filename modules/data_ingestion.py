import yfinance as yf
import pandas as pd

def fetch_data(symbol: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical stock data from Yahoo Finance.

    Args:
        symbol (str): Stock ticker symbol (e.g. "RELIANCE.NS")
        period (str): Duration string like "6mo", "1y", "2y"
        interval (str): Data frequency like "1d" (daily), "1m" (1 minute)

    Returns:
        pd.DataFrame: Stock OHLCV data indexed by Date
    """
    try:
        df = yf.download(symbol, period=period, interval=interval)
        df.dropna(inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return pd.DataFrame()

if __name__ == "__main__":
    # Test your data ingestion for a sample ticker
    ticker = "RELIANCE.NS"
    data = fetch_data(ticker, period="6mo")
    print(f"Fetched {len(data)} rows for {ticker}")
    print(data.head())
