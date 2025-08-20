# src/ind/io.py
import pandas as pd
import os
from .config import REQUIRED_COLUMNS, validate_columns
from .types import PriceDataFrame

REQUIRED_COLUMNS = ["datetime", "open", "high", "low", "close", "volume"]


def load_csv(filepath: str) -> pd.DataFrame:
    """
    Load OHLCV data from a CSV file into a pandas DataFrame.

    The CSV must contain the columns defined in config.REQUIRED_COLUMNS.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        PriceDataFrame: A DataFrame indexed by datetime.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    df = pd.read_csv(filepath)

    # Validate required columns
    validate_columns(df.columns.tolist())

    # Ensure required columns are present
    #missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    #if missing:
    #    raise ValueError(f"Missing required columns in {filepath}: {missing}")

    # Convert datetime
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")

    # Drop rows with invalid datetime
    df = df.dropna(subset=["datetime"])

    # Ensure sorted by datetime
    df = df.sort_values("datetime").reset_index(drop=True)

    # Set datetime as index
    df = df.set_index("datetime")

    return df
