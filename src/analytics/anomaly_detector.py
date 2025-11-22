"""
Anomaly Detection for Battery Systems

Detects abnormal behavior in battery telemetry using statistical methods.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy import stats
from sklearn.ensemble import IsolationForest


class BatteryAnomalyDetector:
    """
    Detects anomalies in battery operation data.
    """

    def __init__(self, contamination: float = 0.05):
        """
        Initialize anomaly detector.

        Args:
            contamination: Expected proportion of outliers (0.0 to 0.5)
        """
        self.contamination = contamination
        self.isolation_forest = None
        self.statistical_bounds = {}

    def detect_statistical_anomalies(
        self, 
        data: pd.DataFrame, 
        columns: Optional[List[str]] = None,
        std_threshold: float = 3.0
    ) -> pd.DataFrame:
        """
        Detect anomalies using statistical methods (z-score).

        Args:
            data: Input data
            columns: Columns to check (default: all numeric)
            std_threshold: Number of standard deviations for threshold

        Returns:
            DataFrame with anomaly flags
        """
        df = data.copy()

        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()

        # Calculate z-scores
        for col in columns:
            if col in df.columns:
                mean = df[col].mean()
                std = df[col].std()
                z_scores = np.abs((df[col] - mean) / std)
                df[f'{col}_anomaly'] = z_scores > std_threshold
                df[f'{col}_zscore'] = z_scores

        # Overall anomaly flag
        anomaly_cols = [f'{col}_anomaly' for col in columns if f'{col}_anomaly' in df.columns]
        df['is_anomaly'] = df[anomaly_cols].any(axis=1)

        return df

    def detect_isolation_forest(
        self, 
        data: pd.DataFrame,
        features: Optional[List[str]] = None
    ) -> np.ndarray:
        """
        Detect anomalies using Isolation Forest algorithm.

        Args:
            data: Input data
            features: Feature columns to use

        Returns:
            Array of anomaly predictions (-1 for anomaly, 1 for normal)
        """
        if features is None:
            features = data.select_dtypes(include=[np.number]).columns.tolist()

        X = data[features].fillna(data[features].mean())

        if self.isolation_forest is None:
            self.isolation_forest = IsolationForest(
                contamination=self.contamination,
                random_state=42
            )
            self.isolation_forest.fit(X)

        predictions = self.isolation_forest.predict(X)

        return predictions

    def detect_threshold_violations(
        self, 
        data: pd.DataFrame,
        thresholds: Dict[str, Tuple[float, float]]
    ) -> pd.DataFrame:
        """
        Detect violations of predefined operational thresholds.

        Args:
            data: Input data
            thresholds: Dict mapping column names to (min, max) tuples

        Returns:
            DataFrame with violation flags
        """
        df = data.copy()

        for col, (min_val, max_val) in thresholds.items():
            if col in df.columns:
                violations = (df[col] < min_val) | (df[col] > max_val)
                df[f'{col}_violation'] = violations

        # Overall violation flag
        violation_cols = [col for col in df.columns if col.endswith('_violation')]
        df['has_violation'] = df[violation_cols].any(axis=1)

        return df

    def detect_sudden_changes(
        self, 
        data: pd.DataFrame,
        column: str,
        change_threshold: float = 10.0
    ) -> pd.DataFrame:
        """
        Detect sudden changes in a metric (e.g., temperature spike).

        Args:
            data: Input data with timestamp
            column: Column to monitor
            change_threshold: Threshold for change detection

        Returns:
            DataFrame with change detection flags
        """
        df = data.copy()

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in data")

        # Calculate rate of change
        df[f'{column}_delta'] = df[column].diff()
        df[f'{column}_sudden_change'] = np.abs(df[f'{column}_delta']) > change_threshold

        return df

    def detect_pattern_deviations(
        self, 
        data: pd.DataFrame,
        column: str,
        window: int = 20
    ) -> pd.DataFrame:
        """
        Detect deviations from expected patterns using rolling statistics.

        Args:
            data: Input data
            column: Column to analyze
            window: Rolling window size

        Returns:
            DataFrame with pattern deviation flags
        """
        df = data.copy()

        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in data")

        # Rolling statistics
        df[f'{column}_rolling_mean'] = df[column].rolling(window=window).mean()
        df[f'{column}_rolling_std'] = df[column].rolling(window=window).std()

        # Deviation from rolling mean
        deviation = np.abs(df[column] - df[f'{column}_rolling_mean'])
        df[f'{column}_pattern_deviation'] = deviation > (3 * df[f'{column}_rolling_std'])

        return df

    def comprehensive_anomaly_detection(
        self, 
        data: pd.DataFrame,
        operational_thresholds: Optional[Dict[str, Tuple[float, float]]] = None
    ) -> pd.DataFrame:
        """
        Run comprehensive anomaly detection pipeline.

        Args:
            data: Input battery telemetry data
            operational_thresholds: Optional thresholds for specific metrics

        Returns:
            DataFrame with all anomaly detection results
        """
        df = data.copy()

        # Statistical anomalies
        df = self.detect_statistical_anomalies(df)

        # Isolation Forest
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            df['isolation_forest_anomaly'] = self.detect_isolation_forest(df, numeric_cols)
            df['isolation_forest_anomaly'] = df['isolation_forest_anomaly'] == -1

        # Threshold violations
        if operational_thresholds is None:
            operational_thresholds = {
                'voltage': (40.0, 60.0),
                'current': (-200.0, 200.0),
                'temperature': (0.0, 50.0)
            }
        df = self.detect_threshold_violations(df, operational_thresholds)

        # Sudden changes
        for col in ['temperature', 'voltage']:
            if col in df.columns:
                df = self.detect_sudden_changes(df, col)

        # Pattern deviations
        for col in ['voltage', 'current']:
            if col in df.columns:
                df = self.detect_pattern_deviations(df, col)

        # Composite anomaly score
        anomaly_indicators = [
            col for col in df.columns 
            if 'anomaly' in col or 'violation' in col or 'deviation' in col or 'change' in col
        ]
        if anomaly_indicators:
            df['anomaly_score'] = df[anomaly_indicators].sum(axis=1) / len(anomaly_indicators)

        return df

    def get_anomaly_summary(self, data: pd.DataFrame) -> Dict:
        """
        Generate summary of detected anomalies.

        Args:
            data: Data with anomaly detection results

        Returns:
            Dictionary with anomaly statistics
        """
        summary = {
            'total_records': len(data),
            'anomaly_count': 0,
            'anomaly_percentage': 0.0,
            'anomaly_types': {}
        }

        if 'is_anomaly' in data.columns:
            summary['anomaly_count'] = data['is_anomaly'].sum()
            summary['anomaly_percentage'] = (summary['anomaly_count'] / len(data)) * 100

        # Count anomalies by type
        anomaly_cols = [col for col in data.columns if 'anomaly' in col or 'violation' in col]
        for col in anomaly_cols:
            if col in data.columns:
                summary['anomaly_types'][col] = int(data[col].sum())

        return summary
