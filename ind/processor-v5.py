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
            indicator: Name of the indicator (SMA, EMA, BOLLINGER, VWAP, etc.)
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
        
        elif indicator == "VWAP":
            # Intraday VWAP, reset daily
            self.df['Date'] = self.df['Datetime'].dt.date
            tp = (self.df['High'] + self.df['Low'] + self.df['Close']) / 3
            self.df['TPV'] = tp * self.df['Volume']   # ✅ Added TPV column
            self.df['cum_TPV'] = self.df.groupby('Date')['TPV'].cumsum()
            self.df['cum_Vol'] = self.df.groupby('Date')['Volume'].cumsum()
            self.df['VWAP'] = self.df['cum_TPV'] / self.df['cum_Vol']
        
        elif indicator == "PIVOT_POINTS":
            # Calculate daily pivot points based on previous day
            self.df['Date'] = self.df['Datetime'].dt.date
            daily = self.df.groupby('Date').agg({
                'High': 'max',
                'Low': 'min',
                'Close': 'last'
            }).reset_index()

            # Calculate pivots
            daily['PP'] = (daily['High'] + daily['Low'] + daily['Close']) / 3
            daily['R1'] = 2 * daily['PP'] - daily['Low']
            daily['S1'] = 2 * daily['PP'] - daily['High']
            daily['R2'] = daily['PP'] + (daily['High'] - daily['Low'])
            daily['S2'] = daily['PP'] - (daily['High'] - daily['Low'])

            # Shift to apply previous day's pivots to the current day
            daily[['PP','R1','S1','R2','S2']] = daily[['PP','R1','S1','R2','S2']].shift(1)

            # Merge back to original df
            self.df = self.df.merge(daily[['Date','PP','R1','S1','R2','S2']], on='Date', how='left')
        
        elif indicator == "ATR":
            period = kwargs.get("period", 14)
            self.df[f"ATR_{period}"] = talib.ATR(self.df["High"], self.df["Low"], self.df["Close"], timeperiod=period)
        
        elif indicator == "RSI":
            periods = kwargs.get("periods", [5, 14])
            for period in periods:
                self.df[f"RSI_{period}"] = talib.RSI(self.df["Close"], timeperiod=period)
        
        elif indicator == "MACD":
            fast = kwargs.get("fast", 5)
            slow = kwargs.get("slow", 13)
            signal = kwargs.get("signal", 9)
            macd, signal_line, hist = talib.MACD(self.df["Close"], fastperiod=fast, slowperiod=slow, signalperiod=signal)
            self.df[f"MACD_{fast}_{slow}_{signal}"] = macd
            self.df[f"MACD_Signal_{fast}_{slow}_{signal}"] = signal_line
            self.df[f"MACD_Hist_{fast}_{slow}_{signal}"] = hist
        
        elif indicator == "STOCH":
            fastk = kwargs.get("fastk", 5)
            slowk = kwargs.get("slowk", 3)
            slowd = kwargs.get("slowd", 3)
            slowk_line, slowd_line = talib.STOCH(self.df["High"], self.df["Low"], self.df["Close"],
                                                 fastk_period=fastk, slowk_period=slowk, slowd_period=slowd)
            self.df[f"Stoch_K_{fastk}_{slowk}_{slowd}"] = slowk_line
            self.df[f"Stoch_D_{fastk}_{slowk}_{slowd}"] = slowd_line
        
        elif indicator == "VOLUME_PROFILE":
            # Simple daily POC (Price of Control)
            self.df['Date'] = self.df['Datetime'].dt.date
            def calculate_poc(group):
                price_bins = pd.cut(group['Close'], bins=50)
                vp = group.groupby(price_bins)['Volume'].sum()
                poc = vp.idxmax().mid if not vp.empty else np.nan
                return poc
            daily_poc = self.df.groupby('Date', group_keys=False).apply(lambda g: calculate_poc(g)).reset_index(name='POC')
            self.df = self.df.merge(daily_poc, on='Date', how='left')
        
        elif indicator == "FVG":
            # Simple FVG detection (bullish and bearish)
            self.df['FVG'] = 0.0
            for i in range(2, len(self.df)):
                if self.df.loc[i, 'Low'] > self.df.loc[i-2, 'High']:
                    self.df.loc[i, 'FVG'] = self.df.loc[i, 'Low'] - self.df.loc[i-2, 'High']  # Bullish FVG
                elif self.df.loc[i, 'High'] < self.df.loc[i-2, 'Low']:
                    self.df.loc[i, 'FVG'] = self.df.loc[i, 'High'] - self.df.loc[i-2, 'Low']  # Bearish FVG (negative)
        
        elif indicator == "GAPS":
            # Daily gap detection
            self.df['Date'] = self.df['Datetime'].dt.date
            daily = self.df.groupby('Date').agg({'Open': 'first', 'Close': 'last'}).reset_index()
            daily['Gap'] = daily['Open'] - daily['Close'].shift(1)
            # Simple classification (example, can be enhanced)
            daily['Gap_Type'] = 'Common'
            daily.loc[(daily['Gap'].abs() > daily['Gap'].std()) & (daily['Gap'] > 0), 'Gap_Type'] = 'Breakaway'  # Example logic
            # Merge back
            self.df = self.df.merge(daily[['Date', 'Gap', 'Gap_Type']], on='Date', how='left')
        
        else:
            raise ValueError(f"Unsupported indicator: {indicator}")

    def add_default_indicators(self) -> None:
        """Add default set of indicators as specified in the PRD."""
        # Original defaults
        periods = [5, 10, 14, 20, 50, 100, 200]
        self.add_indicator("SMA", periods=periods)
        self.add_indicator("EMA", periods=periods)
        self.add_indicator("BOLLINGER", period=20, std_dev=2)
        
        # New indicators
        self.add_indicator("VWAP")
        self.add_indicator("PIVOT_POINTS")
        self.add_indicator("ATR")
        self.add_indicator("RSI")
        self.add_indicator("MACD")
        self.add_indicator("STOCH")
        self.add_indicator("VOLUME_PROFILE")
        self.add_indicator("FVG")
        self.add_indicator("GAPS")

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
