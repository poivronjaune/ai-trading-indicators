# src/ind/processor.py
import pandas as pd
from .config import (
    DEFAULT_SMA_PERIOD,
    DEFAULT_EMA_PERIOD,
    DEFAULT_BB_PERIOD,
    DEFAULT_BB_STD,
)
from .types import IndicatorResults


def sma(df: pd.DataFrame, period: int = DEFAULT_SMA_PERIOD) -> float:
    """Simple Moving Average of the 'close' column."""
    return df["close"].tail(period).mean()


def ema(df: pd.DataFrame, period: int = DEFAULT_EMA_PERIOD) -> float:
    """Exponential Moving Average of the 'close' column."""
    return df["close"].ewm(span=period, adjust=False).mean().iloc[-1]


def bollinger_bands(df: pd.DataFrame, period: int = DEFAULT_BB_PERIOD, num_std: float = DEFAULT_BB_STD):
    """
    Calculate Bollinger Bands on the 'close' column.

    Returns:
        tuple: (upper_band, middle_band, lower_band)
    """
    rolling = df["close"].rolling(window=period)
    middle_band = rolling.mean().iloc[-1]
    std = rolling.std().iloc[-1]

    upper_band = middle_band + num_std * std
    lower_band = middle_band - num_std * std
    return upper_band, middle_band, lower_band


def run_default_indicators(df: pd.DataFrame) -> IndicatorResults:
    """
    Run a default set of indicators on OHLCV data.

    Returns:
        IndicatorResults: Indicator names mapped to their latest values.
    """
    results: IndicatorResults = {}

    # SMA
    results[f"SMA({DEFAULT_SMA_PERIOD})"] = round(sma(df), 4)

    # EMA
    results[f"EMA({DEFAULT_EMA_PERIOD})"] = round(ema(df), 4)

    # Bollinger Bands
    upper, middle, lower = bollinger_bands(df)
    results["Bollinger Upper"] = round(upper, 4)
    results["Bollinger Middle"] = round(middle, 4)
    results["Bollinger Lower"] = round(lower, 4)

    return results
