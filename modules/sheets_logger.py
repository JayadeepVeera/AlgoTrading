import gspread
import pandas as pd
import numpy as np
from google.oauth2.service_account import Credentials

def log_signals_to_sheet(signals_df, sheet_url, tab_name="Signals", creds_file="creds.json"):
    df_to_write = signals_df.copy()

    # Reset index if named (e.g., Date)
    if df_to_write.index.name is not None:
        df_to_write = df_to_write.reset_index()

    # FLATTEN MultiIndex columns to strings if needed
    if isinstance(df_to_write.columns, pd.MultiIndex):
        df_to_write.columns = [
            '_'.join([str(level) for level in col if str(level).strip() != ''])
            for col in df_to_write.columns.values
        ]

    # Remove empty/blank column names
    df_to_write = df_to_write.loc[:, [bool(str(col).strip()) for col in df_to_write.columns]]
    df_to_write.columns = [
        col if str(col).strip() != "" else f"Column_{i}" for i, col in enumerate(df_to_write.columns)
    ]

    # Convert datetime columns to string
    for col in df_to_write.columns:
        if pd.api.types.is_datetime64_any_dtype(df_to_write[col]):
            df_to_write[col] = df_to_write[col].dt.strftime('%Y-%m-%d')
        elif df_to_write[col].apply(lambda x: hasattr(x, 'isoformat')).any():
            df_to_write[col] = df_to_write[col].apply(lambda x: x.isoformat() if hasattr(x, 'isoformat') else x)

    # Replace infinite/NaN values with empty strings
    df_to_write = df_to_write.replace([np.inf, -np.inf], np.nan).fillna('')

    scopes = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(creds_file, scopes=scopes)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url)

    try:
        worksheet = sheet.worksheet(tab_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title=tab_name, rows="1000", cols="20")

    worksheet.clear()
    values = [df_to_write.columns.tolist()] + df_to_write.values.tolist()
    worksheet.update(values)
    print(f"Logged signals successfully to tab '{tab_name}' in the Google Sheet.")
