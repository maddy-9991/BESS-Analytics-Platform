"""
API Routes for BESS Analytics Platform
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
import pandas as pd
from io import StringIO

from src.api.models import (
    BatteryMetricsResponse,
    AnomalyDetectionRequest,
    AnomalyDetectionResponse,
    ProcessDataRequest,
    ProcessDataResponse
)
from src.analytics.battery_metrics import BatteryMetricsCalculator
from src.analytics.data_processor import BatteryDataProcessor
from src.analytics.anomaly_detector import BatteryAnomalyDetector
from src.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/process", response_model=ProcessDataResponse)
async def process_battery_data(file: UploadFile = File(...)):
    """
    Process uploaded battery data CSV file.

    Args:
        file: CSV file with battery telemetry data

    Returns:
        Processed data summary
    """
    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))

        # Process data
        processor = BatteryDataProcessor()
        processed_df = processor.process_pipeline(df)

        # Calculate metrics
        calculator = BatteryMetricsCalculator()
        metrics = calculator.calculate_comprehensive_metrics(processed_df)

        return ProcessDataResponse(
            status="success",
            records_processed=len(processed_df),
            metrics=metrics,
            message="Data processed successfully"
        )

    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/metrics/{battery_id}", response_model=BatteryMetricsResponse)
async def get_battery_metrics(
    battery_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    """
    Get calculated metrics for a specific battery.

    Args:
        battery_id: Battery identifier
        start_date: Start date for metrics (ISO format)
        end_date: End date for metrics (ISO format)

    Returns:
        Battery metrics and health status
    """
    try:
        # In production, this would query from database
        # For demo, return sample metrics
        calculator = BatteryMetricsCalculator()

        sample_metrics = {
            "battery_id": battery_id,
            "timestamp": "2025-11-22T08:00:00Z",
            "soh": 94.5,
            "current_soc": 78.3,
            "avg_voltage": 52.4,
            "avg_current": 12.5,
            "avg_temperature": 28.7,
            "full_cycles": 1245,
            "degradation_rate": 0.12,
            "health_status": "good"
        }

        return BatteryMetricsResponse(**sample_metrics)

    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        raise HTTPException(status_code=404, detail=f"Battery {battery_id} not found")


@router.post("/anomalies/detect", response_model=AnomalyDetectionResponse)
async def detect_anomalies(request: AnomalyDetectionRequest):
    """
    Detect anomalies in battery data.

    Args:
        request: Anomaly detection request with battery data

    Returns:
        Anomaly detection results
    """
    try:
        # Convert request data to DataFrame
        df = pd.DataFrame(request.data)

        # Run anomaly detection
        detector = BatteryAnomalyDetector(contamination=request.contamination)
        results = detector.comprehensive_anomaly_detection(df)

        # Get summary
        summary = detector.get_anomaly_summary(results)

        # Extract anomalies
        if 'is_anomaly' in results.columns:
            anomalies = results[results['is_anomaly']].to_dict('records')
        else:
            anomalies = []

        return AnomalyDetectionResponse(
            battery_id=request.battery_id,
            anomaly_count=summary['anomaly_count'],
            anomaly_percentage=summary['anomaly_percentage'],
            anomalies=anomalies[:10],  # Return top 10
            summary=summary
        )

    except Exception as e:
        logger.error(f"Error detecting anomalies: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/status")
async def get_system_status():
    """Get system status and statistics."""
    return {
        "status": "operational",
        "version": "1.0.0",
        "features": {
            "metrics_calculation": True,
            "anomaly_detection": True,
            "data_processing": True
        }
    }
