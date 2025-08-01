import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import ta

def find_ticker_column(df, base_name, ticker):
    suffix = f"_{ticker}"
    for col in df.columns:
        if col.lower().startswith(base_name.lower()) and col.endswith(ticker):
            return col
    if base_name in df.columns:
        return base_name
    raise ValueError(f"Could not find column '{base_name}' with ticker suffix '{ticker}'")

def prepare_features(df: pd.DataFrame, ticker: str):
    df = df.copy()

    close_col = find_ticker_column(df, 'Close', ticker)
    volume_col = find_ticker_column(df, 'Volume', ticker)

    close_series = df[close_col]
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]
    close_series = pd.Series(close_series.to_numpy().flatten(), index=close_series.index)

    df['RSI'] = ta.momentum.RSIIndicator(close_series, window=14).rsi()
    macd_obj = ta.trend.MACD(close_series)
    df['MACD'] = macd_obj.macd()
    df['MACD_signal'] = macd_obj.macd_signal()

    df['VolumeFeature'] = df[volume_col]

    df['Target'] = (close_series.shift(-1) > close_series).astype(int)

    df = df.dropna(subset=['RSI', 'MACD', 'MACD_signal', 'VolumeFeature', 'Target'])
    return df

def train_predict_model(df: pd.DataFrame):
    features = ['RSI', 'MACD', 'MACD_signal', 'VolumeFeature']
    X = df[features]
    y = df['Target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"ML model accuracy (Logistic Regression, test set): {accuracy:.2%}")

    return model, accuracy
