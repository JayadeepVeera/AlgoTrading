import pandas as pd

def backtest_signals(df: pd.DataFrame, entry_col='Signal', hold_period=5):
    """
    Simple backtest: enters on buy signal, holds for hold_period days, then exits.

    Args:
        df: DataFrame with price data indexed by date and 'Signal' column.
        entry_col: column name with buy/sell signals (1=buy).
        hold_period: days to hold after entry.

    Returns:
        results_df: DataFrame with equity curve, trades, returns.
        summary: dict with performance summary.
    """
    df = df.copy()
    df['Position'] = 0  # 1 when holding, 0 when not
    trade_entries = []
    trade_exits = []
    entry_price = None

    for i in range(len(df)):
        if df.iloc[i][entry_col] == 1 and df['Position'].iloc[i-1] == 0:
            # Enter trade next day open if available
            if i+1 < len(df):
                entry_price = df.iloc[i+1]['Open']
                entry_idx = df.index[i+1]
                df.at[entry_idx, 'Position'] = 1
                trade_entries.append((entry_idx, entry_price))

                # Set exit day
                exit_idx_pos = i+1 + hold_period
                if exit_idx_pos < len(df):
                    exit_idx = df.index[exit_idx_pos]
                    exit_price = df.iloc[exit_idx_pos]['Open']
                    trade_exits.append((exit_idx, exit_price))

                    # Mark position 0 after exit day
                    for j in range(i+2, exit_idx_pos+1):
                        idx_j = df.index[j]
                        df.at[idx_j, 'Position'] = 1
                    if exit_idx_pos+1 < len(df):
                        df.at[df.index[exit_idx_pos+1], 'Position'] = 0

    # Build equity curve
    returns = []
    for (entry_date, entry_p), (exit_date, exit_p) in zip(trade_entries, trade_exits):
        ret = (exit_p - entry_p) / entry_p
        returns.append({'Entry': entry_date, 'Exit': exit_date, 'Return': ret})

    results_df = pd.DataFrame(returns)

    # Summary metrics
    total_return = (results_df['Return'] + 1).prod() - 1 if not results_df.empty else 0
    avg_return = results_df['Return'].mean() if not results_df.empty else 0
    num_trades = len(results_df)

    summary = {
        'Total Return': total_return,
        'Average Trade Return': avg_return,
        'Number of Trades': num_trades,
    }

    return results_df, summary
