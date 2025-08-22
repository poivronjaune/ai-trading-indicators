# src/ind/types.py
from typing import TypedDict, Dict, Any
import pandas as pd


# Type alias for our indicator result dictionary
IndicatorResults = Dict[str, float]


class OHLCVRow(TypedDict):
    datetime: str
    open: float
    high: float
    low: float
    close: float
    volume: float


# Convenience type for a DataFrame
PriceDataFrame = pd.DataFrame
