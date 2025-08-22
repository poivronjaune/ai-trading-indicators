# src/ind/config.py
from pathlib import Path
from typing import Final

# Default parameters
DEFAULT_SMA_PERIOD: Final[int] = 14
DEFAULT_EMA_PERIOD: Final[int] = 14
DEFAULT_BB_PERIOD: Final[int] = 20
DEFAULT_BB_STD: Final[float] = 2.0

# Default data folder
DEFAULT_DATA_FOLDER: Path = Path("data")

# Required OHLCV columns
REQUIRED_COLUMNS: Final[list[str]] = [
    "datetime", "open", "high", "low", "close", "volume"
]


def validate_columns(columns: list[str]) -> None:
    """Ensure all required columns are present."""
    missing = [c for c in REQUIRED_COLUMNS if c not in columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
