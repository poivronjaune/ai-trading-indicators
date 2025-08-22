# processor.py

import pandas as pd
import numpy as np
import talib
from pathlib import Path
from typing import List, Optional, Union

class IndicatorProcessor:
    """Processes financial time-series data and generates technical indicators."""
    
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.ticker: Optional[str] = None

    def load_data(self, file_path: str) -> None:
        """
        Load financial data from a CSV file into a pandas DataFrame.
        
        Args:
            file_path: Path to the input CSV file
        """
        try:
            # Read CSV, ignoring first column
            self.df = pd.read_csv(file_path, usecols=range(1, 8))
            self.df.columns = ["Datetime", "Adj Close", "Close", "High", "Low", "Open", "Volume"]
            
            # Convert Datetime to datetime type
            self.df["Datetime"] = pd.to_datetime(self.df["Datetime"])
            
            # Remove duplicate datetimes
            self.df = self.df.drop_duplicates(subset=["Datetime"], keep="last")
            
            # Sort by datetime
            self.df = self.df.sort_values("Datetime").reset_index(drop=True)
            
            # Extract ticker from filename
            self.ticker = Path(file_path).stem
            
        except Exception as e:
            raise ValueError(f"Failed to load {file_path}: {str(e)}")

    def add_indicator(self, indicator: str, **kwargs) -> None:
        """
        Add a specific technical indicator to the DataFrame.
        
        Args:
            indicator: Name of the indicator (SMA, EMA, BOLLINGER)
            **kwargs: Parameters for the indicator
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data first.")
        
        indicator = indicator.upper()
        
        if indicator == "SMA":
            periods = kwargs.get("periods", [20])
            for period in periods:
                self.df[f"SMA_{period}"] = talib.SMA(self.df["Close"], timeperiod=period)
        
        elif indicator == "EMA":
            periods = kwargs.get("periods", [20])
            for period in periods:
                self.df[f"EMA_{period}"] = talib.EMA(self.df["Close"], timeperiod=period)
        
        elif indicator == "BOLLINGER":
            period = kwargs.get("period", 20)
            std_dev = kwargs.get("std_dev", 2)
            upper, middle, lower = talib.BBANDS(
                self.df["Close"],
                timeperiod=period,
                nbdevup=std_dev,
                nbdevdn=std_dev,
                matype=0
            )
            self.df["BB_Upper"] = upper
            self.df["BB_Middle"] = middle
            self.df["BB_Lower"] = lower
        else:
            raise ValueError(f"Unsupported indicator: {indicator}")

    def add_default_indicators(self) -> None:
        """Add default set of indicators as specified in the PRD."""
        # Moving Averages
        periods = [5, 10, 14, 20, 50, 100, 200]
        self.add_indicator("SMA", periods=periods)
        self.add_indicator("EMA", periods=periods)
        
        # Bollinger Bands
        self.add_indicator("BOLLINGER", period=20, std_dev=2)

    def save_results(self, output_folder: str) -> None:
        """
        Save the processed DataFrame with indicators to a CSV file.
        
        Args:
            output_folder: Path to the output folder
        """
        if self.df is None or self.ticker is None:
            raise ValueError("No data loaded or ticker not set.")
        
        output_path = Path(output_folder) / f"{self.ticker}.csv"
        try:
            self.df.to_csv(output_path, index=False)
        except Exception as e:
            raise ValueError(f"Failed to save results to {output_path}: {str(e)}")
        
        