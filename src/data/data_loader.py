"""Data loading utilities."""

import pandas as pd
from typing import Union, Optional
from pathlib import Path


def load_battery_data(source: Union[str, Path]) -> pd.DataFrame:
    """
    Load battery data from CSV file.

    Args:
        source: Path to CSV file

    Returns:
        DataFrame with battery data
    """
    df = pd.read_csv(source, parse_dates=['timestamp'])
    return df
