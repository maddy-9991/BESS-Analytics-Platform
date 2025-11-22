# BESS Analytics Platform

A cloud-based Battery Energy Storage System (BESS) analytics platform for processing, analyzing, and monitoring battery performance data at scale.

## 🎯 Overview

This platform provides real-time analytics and insights for battery energy storage systems, helping operators:
- Monitor battery health and performance metrics
- Detect anomalies and predict failures
- Optimize battery lifecycle and ROI
- Process large-scale time-series data efficiently

## 🏗️ Architecture

- **Data Processing Pipeline**: Ingests and processes battery telemetry data
- **Analytics Engine**: Calculates key performance indicators (State of Health, State of Charge, degradation metrics)
- **Anomaly Detection**: ML-based anomaly detection for early failure prediction
- **REST API**: FastAPI-based service for data access and analytics
- **Cloud-Ready**: Containerized with Docker, ready for AWS/Azure deployment

## 🚀 Features

- ⚡ Real-time battery metrics calculation
- 📊 State of Health (SOH) and State of Charge (SOC) tracking
- 🔍 Anomaly detection using statistical methods
- 📈 Degradation analysis and trend prediction
- 🔌 RESTful API for integration
- 🧪 Comprehensive test coverage with pytest
- 🐳 Docker containerization
- ☁️ Cloud-native architecture

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, FastAPI
- **Data Processing**: Pandas, NumPy
- **Analytics**: Scikit-learn, SciPy
- **Testing**: pytest, pytest-cov
- **Containerization**: Docker, Docker Compose
- **Database**: PostgreSQL (configurable)
- **Logging**: Structured logging with Python logging

## 📦 Installation

### Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/bess-analytics-platform.git
cd bess-analytics-platform

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run the application
python -m src.api.main
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access API at http://localhost:8000
# API Documentation at http://localhost:8000/docs
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_battery_metrics.py -v
```

## 📖 API Usage

### Get Battery Metrics

```bash
curl -X GET "http://localhost:8000/api/v1/metrics/battery-001"
```

### Process Battery Data

```bash
curl -X POST "http://localhost:8000/api/v1/process" \
  -H "Content-Type: application/json" \
  -F "file=@data/sample/battery_data_sample.csv"
```

### Detect Anomalies

```bash
curl -X POST "http://localhost:8000/api/v1/anomalies/detect" \
  -H "Content-Type: application/json" \
  -d '{"battery_id": "battery-001", "data": [...], "contamination": 0.05}'
```

## 📊 Example Analytics Output

```json
{
  "battery_id": "battery-001",
  "timestamp": "2025-11-22T08:00:00Z",
  "metrics": {
    "state_of_health": 94.5,
    "state_of_charge": 78.3,
    "voltage": 52.4,
    "current": 12.5,
    "temperature": 28.7,
    "cycle_count": 1245,
    "degradation_rate": 0.12
  },
  "anomalies": [],
  "health_status": "good"
}
```

## 🗂️ Project Structure

```
bess-analytics-platform/
├── src/
│   ├── analytics/          # Core analytics modules
│   │   ├── battery_metrics.py
│   │   ├── data_processor.py
│   │   └── anomaly_detector.py
│   ├── api/                # FastAPI application
│   │   ├── main.py
│   │   ├── routes.py
│   │   └── models.py
│   ├── data/               # Data handling
│   │   ├── data_loader.py
│   │   └── storage.py
│   └── utils/              # Utilities
│       ├── config.py
│       └── logger.py
├── tests/                  # Test suite
├── data/sample/            # Sample datasets
├── docs/                   # Documentation
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🌟 Key Components

### Battery Metrics Calculator
Calculates essential battery performance indicators:
- State of Health (SOH)
- State of Charge (SOC)
- Cycle counting
- Degradation analysis

### Data Processor
Handles large-scale time-series battery data:
- Data validation and cleaning
- Aggregation and resampling
- Feature engineering

### Anomaly Detector
ML-based anomaly detection:
- Statistical anomaly detection
- Threshold-based alerts
- Pattern recognition

## 🚀 Deployment

### AWS Deployment
```bash
# Configure AWS credentials
aws configure

# Deploy using Docker (example with ECS)
# See docs/ARCHITECTURE.md for detailed instructions
```

### Azure Deployment
```bash
# Configure Azure CLI
az login

# Deploy to Azure Container Instances
# See docs/ARCHITECTURE.md for detailed instructions
```

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 👤 Author

**Hammad Imran**
- GitHub: [@maddy-9991](https://github.com/maddy-9991)
- Email: hammadimran100@gmail.com

## 🙏 Acknowledgments

Built with modern Python best practices for battery energy storage analytics.
Designed for scalability, reliability, and real-world production use.
