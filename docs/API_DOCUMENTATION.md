# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Endpoints

### 1. Process Battery Data

**POST** `/process`

Upload and process battery telemetry data.

**Request**: Multipart form with CSV file

**Response**:
```json
{
  "status": "success",
  "records_processed": 1000,
  "metrics": {
    "soh": 94.5,
    "avg_temperature": 28.7,
    ...
  },
  "message": "Data processed successfully"
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/process" \
  -F "file=@battery_data.csv"
```

---

### 2. Get Battery Metrics

**GET** `/metrics/{battery_id}`

Retrieve calculated metrics for a specific battery.

**Parameters**:
- `battery_id` (path): Battery identifier
- `start_date` (query, optional): Start date (ISO format)
- `end_date` (query, optional): End date (ISO format)

**Response**:
```json
{
  "battery_id": "battery-001",
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
```

**cURL Example**:
```bash
curl -X GET "http://localhost:8000/api/v1/metrics/battery-001"
```

---

### 3. Detect Anomalies

**POST** `/anomalies/detect`

Run anomaly detection on battery data.

**Request Body**:
```json
{
  "battery_id": "battery-001",
  "data": [
    {"timestamp": "2025-11-22T10:00:00Z", "voltage": 48.5, "current": 12.0, "temperature": 28.0},
    ...
  ],
  "contamination": 0.05,
  "thresholds": {
    "voltage": [40.0, 60.0],
    "temperature": [0.0, 50.0]
  }
}
```

**Response**:
```json
{
  "battery_id": "battery-001",
  "anomaly_count": 12,
  "anomaly_percentage": 1.2,
  "anomalies": [...],
  "summary": {
    "total_records": 1000,
    "anomaly_types": {
      "temperature_anomaly": 5,
      "voltage_anomaly": 7
    }
  }
}
```

---

### 4. System Status

**GET** `/status`

Get system operational status.

**Response**:
```json
{
  "status": "operational",
  "version": "1.0.0",
  "features": {
    "metrics_calculation": true,
    "anomaly_detection": true,
    "data_processing": true
  }
}
```

---

### 5. Health Check

**GET** `/health`

Simple health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "service": "bess-analytics-platform"
}
```

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive Swagger UI documentation.

Visit `http://localhost:8000/redoc` for ReDoc documentation.

## Error Responses

All errors follow this format:

```json
{
  "detail": "Error message description"
}
```

Common status codes:
- `200`: Success
- `400`: Bad Request (validation error)
- `404`: Not Found
- `500`: Internal Server Error

## Authentication

*Note: Authentication not implemented in v1.0. Add JWT/OAuth2 for production.*
