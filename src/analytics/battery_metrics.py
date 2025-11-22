"""
Battery Metrics Calculator

Calculates key performance indicators for battery energy storage systems including:
- State of Health (SOH)
- State of Charge (SOC)
- Degradation metrics
- Cycle counting
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional, Tuple
from datetime import datetime


class BatteryMetricsCalculator:
    """
    Calculates battery performance metrics and health indicators.
    """

    def __init__(self, nominal_capacity: float = 100.0, nominal_voltage: float = 48.0):
        """
        Initialize calculator with battery specifications.

        Args:
            nominal_capacity: Nominal capacity in kWh
            nominal_voltage: Nominal voltage in V
        """
        self.nominal_capacity = nominal_capacity
        self.nominal_voltage = nominal_voltage

    def calculate_soh(self, current_capacity: float) -> float:
        """
        Calculate State of Health (SOH) as percentage of nominal capacity.

        Args:
            current_capacity: Current measured capacity in kWh

        Returns:
            SOH as percentage (0-100)
        """
        soh = (current_capacity / self.nominal_capacity) * 100
        return max(0.0, min(100.0, soh))

    def calculate_soc(self, current_charge: float, max_capacity: float) -> float:
        """
        Calculate State of Charge (SOC).

        Args:
            current_charge: Current charge level in kWh
            max_capacity: Maximum capacity in kWh

        Returns:
            SOC as percentage (0-100)
        """
        soc = (current_charge / max_capacity) * 100
        return max(0.0, min(100.0, soc))

    def calculate_degradation_rate(
        self, 
        capacity_history: pd.Series, 
        time_period_days: int = 30
    ) -> float:
        """
        Calculate capacity degradation rate over time period.

        Args:
            capacity_history: Time series of capacity measurements
            time_period_days: Period for calculation in days

        Returns:
            Degradation rate as percentage per month
        """
        if len(capacity_history) < 2:
            return 0.0

        initial_capacity = capacity_history.iloc[0]
        final_capacity = capacity_history.iloc[-1]

        degradation = ((initial_capacity - final_capacity) / initial_capacity) * 100

        # Normalize to per-month rate
        months = time_period_days / 30.0
        degradation_rate = degradation / months if months > 0 else 0.0

        return max(0.0, degradation_rate)

    def count_cycles(self, charge_data: pd.DataFrame) -> Tuple[int, float]:
        """
        Count charge/discharge cycles using rainflow counting algorithm.

        Args:
            charge_data: DataFrame with SOC values over time

        Returns:
            Tuple of (full_cycles, partial_cycles)
        """
        if 'soc' not in charge_data.columns:
            return 0, 0.0

        soc_values = charge_data['soc'].values

        # Simple cycle counting (full cycle = 0-100-0)
        full_cycles = 0
        partial_cycle_sum = 0.0

        # Track SOC changes
        for i in range(1, len(soc_values)):
            delta_soc = abs(soc_values[i] - soc_values[i-1])
            partial_cycle_sum += delta_soc / 100.0

        full_cycles = int(partial_cycle_sum // 2)
        partial_cycles = partial_cycle_sum % 2

        return full_cycles, partial_cycles

    def calculate_energy_efficiency(
        self, 
        energy_in: float, 
        energy_out: float
    ) -> float:
        """
        Calculate round-trip energy efficiency.

        Args:
            energy_in: Energy charged in kWh
            energy_out: Energy discharged in kWh

        Returns:
            Efficiency as percentage
        """
        if energy_in <= 0:
            return 0.0

        efficiency = (energy_out / energy_in) * 100
        return min(100.0, max(0.0, efficiency))

    def assess_health_status(self, soh: float, temperature: float) -> str:
        """
        Assess overall battery health status.

        Args:
            soh: State of Health percentage
            temperature: Current temperature in Celsius

        Returns:
            Health status: 'excellent', 'good', 'fair', 'poor', 'critical'
        """
        temp_normal = 15 <= temperature <= 35

        if soh >= 95 and temp_normal:
            return "excellent"
        elif soh >= 85 and temp_normal:
            return "good"
        elif soh >= 70:
            return "fair"
        elif soh >= 50:
            return "poor"
        else:
            return "critical"

    def calculate_comprehensive_metrics(
        self, 
        battery_data: pd.DataFrame
    ) -> Dict[str, float]:
        """
        Calculate all metrics from battery telemetry data.

        Args:
            battery_data: DataFrame with columns: voltage, current, temperature, capacity, soc

        Returns:
            Dictionary of calculated metrics
        """
        metrics = {}

        if 'capacity' in battery_data.columns:
            current_capacity = battery_data['capacity'].iloc[-1]
            metrics['soh'] = self.calculate_soh(current_capacity)
            metrics['degradation_rate'] = self.calculate_degradation_rate(
                battery_data['capacity']
            )

        if 'soc' in battery_data.columns:
            metrics['current_soc'] = battery_data['soc'].iloc[-1]
            full_cycles, partial = self.count_cycles(battery_data)
            metrics['full_cycles'] = full_cycles
            metrics['partial_cycles'] = partial

        if 'voltage' in battery_data.columns:
            metrics['avg_voltage'] = battery_data['voltage'].mean()
            metrics['voltage_std'] = battery_data['voltage'].std()

        if 'temperature' in battery_data.columns:
            metrics['avg_temperature'] = battery_data['temperature'].mean()
            metrics['max_temperature'] = battery_data['temperature'].max()

        if 'current' in battery_data.columns:
            metrics['avg_current'] = battery_data['current'].mean()

        # Health status
        if 'soh' in metrics and 'avg_temperature' in metrics:
            metrics['health_status'] = self.assess_health_status(
                metrics['soh'], 
                metrics['avg_temperature']
            )

        return metrics
