# ind/core.py

import pandas as pd
import talib
from pathlib import Path
from typing import List

class IndicatorProcessor:
    """
    Processes financial time-series data to generate technical indicators.

    Reads a specifically formatted CSV file, calculates a suite of indicators,
    and saves the enriched data to a new file.
    """
    # Expected column structure as per PRD
    _COLUMN_NAMES = [
        "NotUsed", "Datetime", "Adj Close", "Close", "High", "Low", "Open", "Volume"
    ]

    def __init__(self, filepath: Path | str):
        """
        Initializes the processor and loads data from the given CSV file.

        Args:
            filepath: Path to the input CSV file.
        """
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"No file found at {self.filepath}")

        self.df = self._load_data()
        self.ticker = self.filepath.stem # Get ticker from filename (e.g., 'AAPL')

    def _load_data(self) -> pd.DataFrame:
        """
        Loads and preprocesses the financial data from the CSV file.
        - Ignores the first column.
        - Sets Datetime as the index and removes duplicates.
        - Ensures data is sorted chronologically for accurate calculations.
        - Verifies and converts data types for TA-Lib compatibility.
        """
        try:
            # Load data, skipping the first column as required
            df = pd.read_csv(
                self.filepath,
                header=None,
                names=self._COLUMN_NAMES,
                usecols=self._COLUMN_NAMES[1:]
            )
            df['Datetime'] = pd.to_datetime(df['Datetime'])
            df = df.drop_duplicates(subset=['Datetime']).set_index('Datetime')

            # TA-Lib requires data to be sorted from oldest to newest
            if not df.index.is_monotonic_increasing:
                df.sort_index(inplace=True)

            # Ensure numeric types for calculation columns
            for col in ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            df.dropna(inplace=True)

            return df
        except Exception as e:
            raise ValueError(f"Failed to load or process CSV file {self.filepath}. Error: {e}")

    def add_sma(self, periods: List[int] = [5, 10, 14, 20, 50, 100, 200]):
        """Calculates and adds Simple Moving Averages (SMA)."""
        for period in periods:
            self.df[f'SMA_{period}'] = talib.SMA(self.df['Close'], timeperiod=period)
        return self

    def add_ema(self, periods: List[int] = [5, 10, 14, 20, 50, 100, 200]):
        """Calculates and adds Exponential Moving Averages (EMA)."""
        for period in periods:
            self.df[f'EMA_{period}'] = talib.EMA(self.df['Close'], timeperiod=period)
        return self

    def add_bollinger_bands(self, period: int = 20, std_dev: float = 2.0):
        """Calculates and adds Bollinger Bands (BB_Upper, BB_Middle, BB_Lower)."""
        upper, middle, lower = talib.BBANDS(
            self.df['Close'],
            timeperiod=period,
            nbdevup=std_dev,
            nbdevdn=std_dev
        )
        self.df['BB_Upper'] = upper
        self.df['BB_Middle'] = middle
        self.df['BB_Lower'] = lower
        return self

    def add_all_default_indicators(self):
        """A convenience method to add all default indicators from the PRD."""
        print("  - Calculating Simple Moving Averages (SMA)...")
        self.add_sma()
        print("  - Calculating Exponential Moving Averages (EMA)...")
        self.add_ema()
        print("  - Calculating Bollinger Bands (BB)...")
        self.add_bollinger_bands()
        return self

    def save_results(self, output_folder: Path | str):
        """
        Saves the DataFrame with appended indicators to a new CSV file.

        Args:
            output_folder: The directory where the output file will be saved.
        """
        output_path = Path(output_folder) / self.filepath.name
        # Reset index to move Datetime from an index back to a column for the CSV
        self.df.reset_index().to_csv(output_path, index=False)
        