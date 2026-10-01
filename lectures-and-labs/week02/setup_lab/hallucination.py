import pandas as pd


def load_spreadsheet(path: str) -> pd.DataFrame:
    """Load an Excel spreadsheet into a pandas DataFrame using the fast reader."""
    return pd.read_excel_fast(path)


spreadsheet = load_spreadsheet("data.xlsx")
print(spreadsheet)