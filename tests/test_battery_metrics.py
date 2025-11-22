"""Tests for battery metrics calculator."""

import pytest
import pandas as pd
import numpy as np
from src.analytics.battery_metrics import BatteryMetricsCalculator


def test_calculate_soh():
    """Test SOH calculation."""
    calculator = BatteryMetricsCalculator(nominal_capacity=100.0)

    # Test normal case
    soh = calculator.calculate_soh(95.0)
    assert soh == 95.0

    # Test boundary
    soh = calculator.calculate_soh(0)
    assert soh == 0.0

    soh = calculator.calculate_soh(120)
    assert soh == 100.0  # Capped at 100


def test_calculate_soc():
    """Test SOC calculation."""
    calculator = BatteryMetricsCalculator()

    soc = calculator.calculate_soc(50, 100)
    assert soc == 50.0

    soc = calculator.calculate_soc(100, 100)
    assert soh == 100.0


def test_calculate_degradation_rate():
    """Test degradation rate calculation."""
    calculator = BatteryMetricsCalculator()

    capacity_history = pd.Series([100, 99, 98, 97, 96])
    rate = calculator.calculate_degradation_rate(capacity_history, time_period_days=30)

    assert rate > 0
    assert isinstance(rate, float)


def test_assess_health_status():
    """Test health status assessment."""
    calculator = BatteryMetricsCalculator()

    status = calculator.assess_health_status(soh=96, temperature=25)
    assert status == "excellent"

    status = calculator.assess_health_status(soh=90, temperature=25)
    assert status == "good"

    status = calculator.assess_health_status(soh=75, temperature=25)
    assert status == "fair"

    status = calculator.assess_health_status(soh=45, temperature=25)
    assert status == "critical"


def test_comprehensive_metrics():
    """Test comprehensive metrics calculation."""
    calculator = BatteryMetricsCalculator()

    # Create sample data
    data = pd.DataFrame({
        'voltage': [48.0, 48.5, 49.0],
        'current': [10.0, 12.0, 11.0],
        'temperature': [25.0, 26.0, 25.5],
        'capacity': [100.0, 99.9, 99.8],
        'soc': [80.0, 75.0, 70.0]
    })

    metrics = calculator.calculate_comprehensive_metrics(data)

    assert 'soh' in metrics
    assert 'current_soc' in metrics
    assert 'avg_voltage' in metrics
    assert 'health_status' in metrics
