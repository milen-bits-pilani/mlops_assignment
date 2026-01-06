# MLOps Assignment - Heart Disease Prediction

End-to-end MLOps solution for predicting heart disease risk using patient health data.

## Project Structure

```
mlops_project/
├── src/
│   ├── data/           # Data acquisition and preprocessing
│   ├── eda/            # Exploratory Data Analysis
│   ├── models/         # Model training and evaluation
│   └── api/            # FastAPI application
├── tests/              # Unit tests
├── k8s/                # Kubernetes manifests
├── scripts/            # Utility scripts
├── models/             # Trained models (generated)
├── data/               # Dataset (generated)
├── mlruns/             # MLflow runs (generated)
└── requirements.txt    # Python dependencies
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
python3.12 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Run Complete Pipeline

```bash
chmod +x scripts/run_pipeline.sh
./scripts/run_pipeline.sh
```

Or run steps individually:

```bash
# Download data
python src/data/download_data.py

# Run EDA
python -c "from src.eda.explore import perform_eda; perform_eda('data/raw/heart_disease.csv')"

# Train models
python src/models/train.py data/raw/heart_disease.csv
```

### 4. View MLflow Experiments

**Quick Start:**
```bash
# Option 1: Use the script
./scripts/start_mlflow_ui.sh

# Option 2: Manual start
mlflow ui
```

**Access MLflow UI:**
- Open your browser and go to: **http://localhost:5000**
- View all experiments, metrics, parameters, and model artifacts

**For detailed instructions, see:** [MLFLOW_GUIDE.md](MLFLOW_GUIDE.md)

## Model Training

The training script:
- Trains Logistic Regression and Random Forest models
- Performs 5-fold cross-validation
- Logs all experiments to MLflow
- Saves the best model based on ROC-AUC score

## API Deployment

### Local Docker Deployment

```bash
# Build Docker image
docker build -t heart-disease-api:latest .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  heart-disease-api:latest

# Test API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63,
    "sex": 1,
    "cp": 3,
    "trestbps": 145,
    "chol": 233,
    "fbs": 1,
    "restecg": 0,
    "thalach": 150,
    "exang": 0,
    "oldpeak": 2.3,
    "slope": 0,
    "ca": 0,
    "thal": 1
  }'
```

### Kubernetes Deployment (kind)

```bash
# Ensure kind cluster is running
kind get clusters

# Build and load image
docker build -t heart-disease-api:latest .
kind load docker-image heart-disease-api:latest --name kind

# Deploy
chmod +x scripts/deploy_k8s.sh
./scripts/deploy_k8s.sh

# Or manually:
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/monitoring.yaml

# Port forward to access API
kubectl port-forward service/heart-disease-api-service 8000:80
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `POST /predict` - Make predictions
- `GET /metrics` - Prometheus metrics
- `GET /docs` - Interactive API documentation

## Monitoring

### Prometheus

```bash
# Port forward Prometheus
kubectl port-forward service/prometheus-service 9090:9090
# Access at http://localhost:9090
```

### Grafana

```bash
# Port forward Grafana
kubectl port-forward service/grafana-service 3000:3000
# Access at http://localhost:3000
# Default credentials: admin/admin
```

## Testing

Run unit tests:

```bash
pytest tests/ -v --cov=src --cov-report=html
```

## CI/CD

GitHub Actions workflow (`.github/workflows/ci_cd.yml`) includes:
- Code linting (Black, Flake8, Pylint)
- Unit tests with coverage
- Model training
- Docker image build and test

## Model Performance

Models are evaluated using:
- Accuracy
- Precision
- Recall
- ROC-AUC
- 5-fold Cross-Validation

All metrics are logged to MLflow for experiment tracking.

## Requirements

- Python 3.12+
- Docker
- Kubernetes (kind)
- 4GB+ RAM recommended

## License

This project is for educational purposes as part of MLOps assignment.

