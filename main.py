from modules.data_ingestion import fetch_data
from modules.strategy import generate_signals
from modules.sheets_logger import log_signals_to_sheet
from modules.notifier import TelegramNotifier
from modules.ml_model import prepare_features, train_predict_model


def flatten_multiindex_columns(df):
    if hasattr(df.columns, 'levels') and df.columns.nlevels > 1:
        df.columns = ['_'.join(map(str, col)).strip() for col in df.columns.values]
    return df


def rename_cols_for_ticker(df, ticker):
    suffix = f"_{ticker}"
    new_cols = {}
    for col in df.columns:
        col_str = '_'.join(col) if isinstance(col, tuple) else str(col)
        if col_str.endswith(suffix):
            new_cols[col] = col_str.replace(suffix, "")
    return df.rename(columns=new_cols)


def main():
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1Pam4-VEaxi5R2so8FYpLIFjXRU9OAdEZzJWvkgCyeCw/edit?gid=793332340#gid=793332340"
    TELEGRAM_TOKEN = "7598066219:AAHodnOrEbh3W3IInst1xWrEwQRDuj68tQc"   # Replace with your actual bot token
    TELEGRAM_CHAT_ID = 5610343610     # Replace with your actual numeric chat ID

    notifier = TelegramNotifier(token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID)

    print("Sending test Telegram alert...")
    notifier.send_message("🚀 Test alert: Telegram notifications are working! 🚀")

    tickers = ["RELIANCE.NS", "HDFCBANK.NS", "INFY.NS"]

    for ticker in tickers:
        print(f"\nFetching data for {ticker}...")
        df = fetch_data(ticker, period="6mo", interval="1d")

        if df.empty:
            print(f"No data fetched for {ticker}, skipping.")
            continue

        df = flatten_multiindex_columns(df)
        df_renamed = rename_cols_for_ticker(df, ticker)

        close_col = "Close"
        if close_col not in df_renamed.columns and "Adj Close" in df_renamed.columns:
            close_col = "Adj Close"

        signals_df = generate_signals(df_renamed, close_col=close_col)
        signals_df["Script"] = ticker

        buy_signals = signals_df[signals_df["Signal"] == 1]

        messages_to_send = []

        if buy_signals.empty:
            print(f"No buy signals for {ticker} in last 6 months.")
        else:
            print(f"Buy signals for {ticker} found. Preparing message...")
            print(buy_signals[["RSI", "20DMA", "50DMA", "Signal"]])
            msg = f"Buy signal(s) for {ticker}:\n"
            for idx, row in buy_signals.iterrows():
                date_str = idx.strftime("%Y-%m-%d") if hasattr(idx, "strftime") else str(idx)
                try:
                    rsi_val = float(row['RSI'])
                    dma20_val = float(row['20DMA'])
                    dma50_val = float(row['50DMA'])
                except Exception:
                    rsi_val, dma20_val, dma50_val = row['RSI'], row['20DMA'], row['50DMA']
                msg_line = f"- {date_str}: RSI={rsi_val:.2f}, 20DMA={dma20_val:.2f}, 50DMA={dma50_val:.2f}"
                print(f"Will send alert: {msg_line}")
                msg += msg_line + "\n"
            messages_to_send.append(msg)

        tab_name = ticker.replace(".NS", "") + "_signals"
        try:
            log_signals_to_sheet(signals_df, SHEET_URL, tab_name=tab_name)
            print(f"Logged signals successfully to tab '{tab_name}'")
        except Exception as e:
            print(f"Failed to log signals for {ticker} to Google Sheets: {e}")

        # ML model
        try:
            ml_data = prepare_features(df, ticker)
            if ml_data.empty:
                print(f"[ML] Not enough data to train ML model for {ticker}")
            else:
                _, accuracy = train_predict_model(ml_data)
                ml_msg = f"ML model accuracy for {ticker}: {accuracy:.2%}"
                print(f"[ML] {ml_msg}")
                messages_to_send.append(ml_msg)
        except Exception as e:
            print(f"[ML] ML model training failed for {ticker}: {e}")

        if messages_to_send:
            print(f"Sending {len(messages_to_send)} message(s) to Telegram for {ticker}...")
            for message in messages_to_send:
                print(f"Sending message:\n{message}")
            notifier.send_messages(messages_to_send, delay=1.0)  # 1 second delay between sends


if __name__ == "__main__":
    main()
