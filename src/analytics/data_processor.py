"""
Data Processor for Battery Telemetry

Handles data ingestion, validation, cleaning, and transformation for battery data.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta


class BatteryDataProcessor:
    """
    Processes and validates battery telemetry data.
    """

    REQUIRED_COLUMNS = ['timestamp', 'voltage', 'current', 'temperature']
    OPTIONAL_COLUMNS = ['soc', 'capacity', 'power']

    def __init__(self):
        self.data: Optional[pd.DataFrame] = None

    def load_data(self, data: Union[pd.DataFrame, str]) -> pd.DataFrame:
        """
        Load battery data from DataFrame or CSV file.

        Args:
            data: DataFrame or path to CSV file

        Returns:
            Loaded DataFrame
        """
        if isinstance(data, str):
            self.data = pd.read_csv(data, parse_dates=['timestamp'])
        else:
            self.data = data.copy()

        return self.data

    def validate_data(self, data: pd.DataFrame) -> Dict[str, bool]:
        """
        Validate battery data for completeness and correctness.

        Args:
            data: DataFrame to validate

        Returns:
            Dictionary of validation results
        """
        validation_results = {
            'has_required_columns': True,
            'has_valid_timestamps': True,
            'has_valid_ranges': True,
            'has_duplicates': False,
            'has_missing_values': False
        }

        # Check required columns
        missing_cols = set(self.REQUIRED_COLUMNS) - set(data.columns)
        validation_results['has_required_columns'] = len(missing_cols) == 0

        if 'timestamp' in data.columns:
            validation_results['has_valid_timestamps'] = pd.api.types.is_datetime64_any_dtype(data['timestamp'])

        # Check for duplicates
        validation_results['has_duplicates'] = data.duplicated().any()

        # Check for missing values
        validation_results['has_missing_values'] = data.isnull().any().any()

        # Check value ranges
        if 'voltage' in data.columns:
            validation_results['has_valid_ranges'] = (data['voltage'] >= 0).all()

        if 'temperature' in data.columns:
            temp_valid = (data['temperature'] >= -50) & (data['temperature'] <= 100)
            validation_results['has_valid_ranges'] &= temp_valid.all()

        return validation_results

    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean battery data by handling missing values and outliers.

        Args:
            data: DataFrame to clean

        Returns:
            Cleaned DataFrame
        """
        df = data.copy()

        # Remove duplicates
        df = df.drop_duplicates(subset=['timestamp'], keep='first')

        # Sort by timestamp
        if 'timestamp' in df.columns:
            df = df.sort_values('timestamp').reset_index(drop=True)

        # Handle missing values with forward fill
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(method='ffill').fillna(method='bfill')

        # Remove outliers using IQR method
        for col in ['voltage', 'current', 'temperature']:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR
                upper_bound = Q3 + 3 * IQR
                df[col] = df[col].clip(lower_bound, upper_bound)

        return df

    def resample_data(
        self, 
        data: pd.DataFrame, 
        frequency: str = '1min'
    ) -> pd.DataFrame:
        """
        Resample time-series data to specified frequency.

        Args:
            data: DataFrame with timestamp index
            frequency: Resampling frequency (e.g., '1min', '5min', '1H')

        Returns:
            Resampled DataFrame
        """
        df = data.copy()

        if 'timestamp' not in df.columns:
            raise ValueError("Data must have 'timestamp' column")

        df = df.set_index('timestamp')

        # Resample numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        resampled = df[numeric_cols].resample(frequency).mean()

        return resampled.reset_index()

    def calculate_derived_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate derived features from raw telemetry.

        Args:
            data: Raw battery data

        Returns:
            DataFrame with additional features
        """
        df = data.copy()

        # Calculate power if not present
        if 'power' not in df.columns and 'voltage' in df.columns and 'current' in df.columns:
            df['power'] = df['voltage'] * df['current']

        # Calculate energy (kWh) from power over time
        if 'power' in df.columns and 'timestamp' in df.columns:
            df = df.sort_values('timestamp')
            time_diff = df['timestamp'].diff().dt.total_seconds() / 3600  # hours
            df['energy_delta'] = df['power'] * time_diff / 1000  # kWh
            df['cumulative_energy'] = df['energy_delta'].cumsum()

        # Temperature rate of change
        if 'temperature' in df.columns:
            df['temp_delta'] = df['temperature'].diff()
            df['temp_rate'] = df['temp_delta'] / df['timestamp'].diff().dt.total_seconds()

        # Voltage variance over rolling window
        if 'voltage' in df.columns:
            df['voltage_rolling_std'] = df['voltage'].rolling(window=10, min_periods=1).std()

        return df

    def aggregate_by_period(
        self, 
        data: pd.DataFrame, 
        period: str = 'D'
    ) -> pd.DataFrame:
        """
        Aggregate data by time period.

        Args:
            data: Input data with timestamp
            period: Pandas period string ('D' for day, 'W' for week, 'M' for month)

        Returns:
            Aggregated DataFrame
        """
        if 'timestamp' not in data.columns:
            raise ValueError("Data must have 'timestamp' column")

        df = data.set_index('timestamp')

        # Define aggregation functions
        agg_dict = {}
        if 'voltage' in df.columns:
            agg_dict['voltage'] = ['mean', 'min', 'max', 'std']
        if 'current' in df.columns:
            agg_dict['current'] = ['mean', 'min', 'max']
        if 'temperature' in df.columns:
            agg_dict['temperature'] = ['mean', 'min', 'max']
        if 'power' in df.columns:
            agg_dict['power'] = ['mean', 'sum']
        if 'soc' in df.columns:
            agg_dict['soc'] = ['mean', 'min', 'max']

        aggregated = df.resample(period).agg(agg_dict)

        # Flatten column names
        aggregated.columns = ['_'.join(col).strip() for col in aggregated.columns.values]

        return aggregated.reset_index()

    def process_pipeline(
        self, 
        data: Union[pd.DataFrame, str],
        clean: bool = True,
        add_features: bool = True,
        resample_freq: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Complete processing pipeline for battery data.

        Args:
            data: Input data (DataFrame or CSV path)
            clean: Whether to clean data
            add_features: Whether to add derived features
            resample_freq: Resampling frequency (optional)

        Returns:
            Processed DataFrame
        """
        # Load data
        df = self.load_data(data)

        # Validate
        validation = self.validate_data(df)
        if not validation['has_required_columns']:
            raise ValueError(f"Missing required columns: {self.REQUIRED_COLUMNS}")

        # Clean
        if clean:
            df = self.clean_data(df)

        # Add derived features
        if add_features:
            df = self.calculate_derived_features(df)

        # Resample if requested
        if resample_freq:
            df = self.resample_data(df, resample_freq)

        return df
