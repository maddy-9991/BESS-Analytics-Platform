"""Tests for data processor."""

import pytest
import pandas as pd
import numpy as np
from src.analytics.data_processor import BatteryDataProcessor


def test_validate_data():
    """Test data validation."""
    processor = BatteryDataProcessor()

    # Valid data
    data = pd.DataFrame({
        'timestamp': pd.date_range('2025-01-01', periods=10, freq='1min'),
        'voltage': np.random.uniform(45, 52, 10),
        'current': np.random.uniform(-10, 10, 10),
        'temperature': np.random.uniform(20, 30, 10)
    })

    results = processor.validate_data(data)

    assert results['has_required_columns'] is True
    assert results['has_valid_timestamps'] is True


def test_clean_data():
    """Test data cleaning."""
    processor = BatteryDataProcessor()

    # Data with duplicates and missing values
    data = pd.DataFrame({
        'timestamp': pd.date_range('2025-01-01', periods=10, freq='1min'),
        'voltage': [48.0, 48.5, np.nan, 49.0, 48.8, 48.8, 49.2, 48.5, 49.0, 48.7],
        'current': [10.0] * 10,
        'temperature': [25.0] * 10
    })

    cleaned = processor.clean_data(data)

    assert cleaned.isnull().sum().sum() == 0  # No missing values
    assert len(cleaned) <= len(data)  # Duplicates removed


def test_calculate_derived_features():
    """Test derived feature calculation."""
    processor = BatteryDataProcessor()

    data = pd.DataFrame({
        'timestamp': pd.date_range('2025-01-01', periods=10, freq='1min'),
        'voltage': [48.0] * 10,
        'current': [10.0] * 10,
        'temperature': np.arange(25, 35)
    })

    enhanced = processor.calculate_derived_features(data)

    assert 'power' in enhanced.columns
    assert 'temp_delta' in enhanced.columns


def test_process_pipeline():
    """Test full processing pipeline."""
    processor = BatteryDataProcessor()

    data = pd.DataFrame({
        'timestamp': pd.date_range('2025-01-01', periods=100, freq='1min'),
        'voltage': np.random.uniform(45, 52, 100),
        'current': np.random.uniform(-10, 10, 100),
        'temperature': np.random.uniform(20, 30, 100)
    })

    processed = processor.process_pipeline(data, clean=True, add_features=True)

    assert len(processed) > 0
    assert 'power' in processed.columns
