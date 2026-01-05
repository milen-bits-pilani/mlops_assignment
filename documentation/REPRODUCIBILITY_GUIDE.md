# Reproducibility Guide

This guide enables anyone to reproduce the entire MLOps pipeline from scratch.

## Quick Start

Follow these steps in order to reproduce the complete project:

```bash
# 1. Setup (5 minutes)
# 2. Run Pipeline (10 minutes)
# 3. Deploy (10 minutes)
# 4. Verify (5 minutes)

Total Time: ~30 minutes
```

## Prerequisites Check

```bash
# Check Python
python3 --version  # Should be 3.12+

# Check Docker
docker --version

# Check kind
kind --version

# Check kubectl
kubectl version --client
```

If any are missing, see [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md).

## Step 1: Environment Setup

### 1.1 Clone/Extract Project

```bash
# Navigate to project directory
cd mlops_project
```

### 1.2 Create Virtual Environment

```bash
# Create venv
python3.12 -m venv venv

# Activate
source venv/bin/activate  # Linux/macOS
```

### 1.3 Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### 1.4 Initialize Directories

```bash
# Run init script
./scripts/init_project.sh

# Or manually
mkdir -p data/raw data/eda models mlruns screenshots logs
```

### 1.5 Verify Setup

```bash
python verify_setup.py
# Should show all ✅
```

## Step 2: Run Complete Pipeline

### 2.1 Run Automated Pipeline

```bash
# Run complete pipeline (download → EDA → train)
./scripts/run_pipeline.sh
```

**Expected Output:**
- Dataset downloaded to `data/raw/heart_disease.csv`
- EDA visualizations in `data/eda/`
- Models trained and saved to `models/`
- MLflow experiments in `mlruns/`

### 2.2 Verify Pipeline Results

```bash
# Check data
ls -lh data/raw/
ls -lh data/eda/

# Check models
ls -lh models/

# Check MLflow
ls -lh mlruns/
```

## Step 3: View MLflow Experiments

### 3.1 Start MLflow UI

```bash
# Option 1: Use script
./scripts/start_mlflow_ui.sh

# Option 2: Manual
mlflow ui
```

### 3.2 Access MLflow

- Open: http://localhost:5000
- View experiments, metrics, and artifacts

## Step 4: Run Tests

### 4.1 Run All Tests

```bash
# Run tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=src --cov-report=html
```

**Expected:** All tests pass ✅

## Step 5: Build Docker Image

### 5.1 Build Image

```bash
# Build
docker build -t heart-disease-api:latest .

# Verify
docker images | grep heart-disease-api
```

### 5.2 Test Locally

```bash
# Run container
docker run -d -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  --name test-api \
  heart-disease-api:latest

# Wait for startup
sleep 10

# Test health
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
    "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
    "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
  }'

# Cleanup
docker stop test-api
docker rm test-api
```

## Step 6: Deploy to Kubernetes

### 6.1 Setup Kubernetes (kind)

```bash
# Check if cluster exists
kind get clusters

# Create if needed
kind create cluster --name local-k8s-1
```

### 6.2 Build and Load Image

```bash
# Build, save, and load to kind
./scripts/build_and_load_k8s.sh
```

### 6.3 Deploy Everything

```bash
# Deploy complete stack
./scripts/deploy_k8s.sh
```

This deploys:
- API (2 replicas)
- Prometheus
- Grafana
- MLflow UI

### 6.4 Copy Models and Data

```bash
# Copy models to API pods
./scripts/copy_models_to_k8s.sh

# Copy MLflow data
./scripts/copy_mlflow_to_k8s.sh
```

## Step 7: Verify Deployment

### 7.1 Check API

```bash
# Port forward
kubectl port-forward service/heart-disease-api-service 8000:80

# Test
curl http://localhost:8000/health
curl http://localhost:8000/metrics | grep api_requests_total
```

### 7.2 Check Prometheus

```bash
# Port forward
kubectl port-forward service/prometheus-service 9090:9090

# Open: http://localhost:9090/targets
# Should see API targets as UP
```

### 7.3 Check Grafana

```bash
# Port forward
kubectl port-forward service/grafana-service 3000:3000

# Open: http://localhost:3000
# Login: admin/admin
# Verify Prometheus data source is working
```

### 7.4 Check MLflow UI

```bash
# Port forward
kubectl port-forward service/mlflow-ui-service 5000:5000

# Open: http://localhost:5000
# Should see "heart_disease" experiment
```

## Step 8: Generate Metrics

### 8.1 Generate API Traffic

```bash
# Generate metrics
./scripts/generate_metrics.sh
```

### 8.2 Verify in Prometheus

- Wait 15-20 seconds
- Query: `api_requests_total`
- Should see data

### 8.3 Create Grafana Dashboard

- Follow [GRAFANA_QUICK_START.md](../GRAFANA_QUICK_START.md)
- Create dashboard with API metrics
- Visualize request rates, latency, predictions

## Expected Results

### Files Created

```
mlops_project/
├── data/
│   ├── raw/heart_disease.csv          ✅ Dataset
│   └── eda/*.png                       ✅ Visualizations
├── models/
│   ├── best_model.pkl                  ✅ Trained model
│   └── preprocessor.pkl                ✅ Preprocessor
├── mlruns/                             ✅ MLflow experiments
└── documentation/                      ✅ This folder
```

### Services Running

- ✅ API: http://localhost:8000
- ✅ Prometheus: http://localhost:9090
- ✅ Grafana: http://localhost:3000
- ✅ MLflow UI: http://localhost:5000

### Metrics Available

- ✅ `api_requests_total`
- ✅ `api_request_duration_seconds`
- ✅ `predictions_total`

## Troubleshooting

### Pipeline Fails

**Issue:** Import errors
```bash
# Solution: Check PYTHONPATH
export PYTHONPATH=$(pwd):$PYTHONPATH
# Or use the pipeline script which sets it
```

**Issue:** Dataset download fails
```bash
# Solution: Check internet connection
# Or manually download from UCI repository
```

### Models Not Training

**Issue:** MLflow errors
```bash
# Solution: Check mlruns directory permissions
chmod -R 755 mlruns/
```

### Docker Build Fails

**Issue:** Build errors
```bash
# Solution: Check Dockerfile syntax
docker build -t heart-disease-api:latest . --no-cache
```

### Kubernetes Deployment Fails

**Issue:** Pods not starting
```bash
# Solution: Check logs
kubectl logs -l app=heart-disease-api
kubectl describe pod <pod-name>
```

**Issue:** Models not found
```bash
# Solution: Copy models again
./scripts/copy_models_to_k8s.sh
```

## Verification Checklist

- [ ] Python environment set up
- [ ] Dependencies installed
- [ ] Pipeline runs successfully
- [ ] Models trained and saved
- [ ] MLflow experiments visible
- [ ] Tests pass
- [ ] Docker image builds
- [ ] Kubernetes cluster created
- [ ] API deployed and running
- [ ] Models copied to pods
- [ ] Prometheus scraping metrics
- [ ] Grafana connected
- [ ] MLflow UI accessible
- [ ] All endpoints working

## Reproducibility Guarantees

### Fixed Random Seeds

- **Python:** `random.seed(42)`
- **NumPy:** `np.random.seed(42)`
- **Scikit-learn:** `random_state=42`
- **Train/test split:** `random_state=42`

### Version Pinning

- All dependencies in `requirements.txt`
- Specific versions for reproducibility
- Python 3.12 specified

### Environment Isolation

- Virtual environment
- Docker containerization
- Kubernetes namespaces

## Time Estimates

| Step | Time |
|------|------|
| Setup | 5 min |
| Pipeline | 10 min |
| Testing | 2 min |
| Docker Build | 3 min |
| K8s Deploy | 10 min |
| Verification | 5 min |
| **Total** | **~35 min** |

## Summary

✅ **Complete reproduction guide** - Step-by-step
✅ **Automated scripts** - Minimal manual work
✅ **Verification steps** - Ensure everything works
✅ **Troubleshooting** - Common issues covered
✅ **Time estimates** - Know what to expect

**Anyone can reproduce this project in ~30-35 minutes!**

## Next Steps

After reproduction:
1. Review [EDA_AND_MODELING.md](EDA_AND_MODELING.md) for analysis
2. Check [EXPERIMENT_TRACKING.md](EXPERIMENT_TRACKING.md) for MLflow
3. Explore [ARCHITECTURE.md](ARCHITECTURE.md) for design
4. Review [CI_CD_WORKFLOW.md](CI_CD_WORKFLOW.md) for automation

