"""
Pydantic models for API request/response validation.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


class BatteryMetricsResponse(BaseModel):
    """Response model for battery metrics."""
    battery_id: str
    timestamp: str
    soh: float = Field(..., description="State of Health (%)")
    current_soc: float = Field(..., description="State of Charge (%)")
    avg_voltage: float = Field(..., description="Average voltage (V)")
    avg_current: float = Field(..., description="Average current (A)")
    avg_temperature: float = Field(..., description="Average temperature (°C)")
    full_cycles: int = Field(..., description="Number of full charge cycles")
    degradation_rate: float = Field(..., description="Degradation rate (% per month)")
    health_status: str = Field(..., description="Health status category")


class ProcessDataRequest(BaseModel):
    """Request model for data processing."""
    battery_id: str
    data: List[Dict[str, Any]]
    clean: bool = True
    add_features: bool = True


class ProcessDataResponse(BaseModel):
    """Response model for data processing."""
    status: str
    records_processed: int
    metrics: Dict[str, Any]
    message: str


class AnomalyDetectionRequest(BaseModel):
    """Request model for anomaly detection."""
    battery_id: str
    data: List[Dict[str, Any]]
    contamination: float = Field(default=0.05, ge=0.0, le=0.5)
    thresholds: Optional[Dict[str, tuple]] = None


class AnomalyDetectionResponse(BaseModel):
    """Response model for anomaly detection."""
    battery_id: str
    anomaly_count: int
    anomaly_percentage: float
    anomalies: List[Dict[str, Any]]
    summary: Dict[str, Any]


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str
    timestamp: str
    version: str
