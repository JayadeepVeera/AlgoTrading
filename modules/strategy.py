import pandas as pd
import ta

def generate_signals(df: pd.DataFrame, close_col: str = "Close") -> pd.DataFrame:
    df = df.copy()

    close_prices = df[close_col]
    if isinstance(close_prices, pd.DataFrame):
        close_prices = close_prices.iloc[:, 0]
    close_prices = pd.Series(close_prices.to_numpy().flatten(), index=close_prices.index)

    df['RSI'] = ta.momentum.RSIIndicator(close_prices, window=14).rsi()
    df['20DMA'] = close_prices.rolling(window=20).mean()
    df['50DMA'] = close_prices.rolling(window=50).mean()

    df['Signal'] = 0
    crossover = (df['20DMA'].shift(1) < df['50DMA'].shift(1)) & (df['20DMA'] >= df['50DMA'])
    df.loc[(df['RSI'] < 30) & crossover, 'Signal'] = 1

    return df
