"""Data storage utilities."""

import pandas as pd
from typing import Optional
from pathlib import Path


class DataStorage:
    """Handle data persistence."""

    def __init__(self, base_path: str = "data"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)

    def save_processed_data(self, data: pd.DataFrame, filename: str):
        """Save processed data to CSV."""
        filepath = self.base_path / "processed" / filename
        filepath.parent.mkdir(exist_ok=True)
        data.to_csv(filepath, index=False)

    def load_processed_data(self, filename: str) -> pd.DataFrame:
        """Load processed data from CSV."""
        filepath = self.base_path / "processed" / filename
        return pd.read_csv(filepath, parse_dates=['timestamp'])
