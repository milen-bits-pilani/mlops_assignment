# System Architecture

## Overview

This document describes the architecture of the Heart Disease Prediction MLOps pipeline, including data flow, components, and deployment architecture.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        MLOps Pipeline                            │
└─────────────────────────────────────────────────────────────────┘

Data Flow:
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│   Data   │───▶│   EDA    │───▶│ Training │───▶│  Model   │
│Download  │    │          │    │          │    │ Packaging│
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                      │                │                │
                      ▼                ▼                ▼
                ┌──────────┐    ┌──────────┐    ┌──────────┐
                │Visual-   │    │ MLflow   │    │  Docker  │
                │izations  │    │Tracking  │    │  Image   │
                └──────────┘    └──────────┘    └──────────┘
                                                      │
                                                      ▼
                                            ┌──────────────────┐
                                            │  Kubernetes      │
                                            │  Deployment      │
                                            └──────────────────┘
                                                      │
                    ┌─────────────────────────────────┼─────────────────┐
                    ▼                                 ▼                 ▼
            ┌──────────────┐                  ┌──────────────┐  ┌──────────────┐
            │   FastAPI    │                  │  Prometheus  │  │   Grafana    │
            │   Service    │◀─────────────────│  (Metrics)   │─▶│ (Dashboards) │
            └──────────────┘                  └──────────────┘  └──────────────┘
```

## Component Architecture

### 1. Data Layer

**Components:**
- Data download script (`src/data/download_data.py`)
- Data preprocessing (`src/data/preprocess.py`)
- Data storage (`data/raw/`, `data/eda/`)

**Responsibilities:**
- Dataset acquisition from UCI ML Repository
- Data cleaning and preprocessing
- Feature engineering
- Data validation

### 2. EDA Layer

**Components:**
- EDA script (`src/eda/explore.py`)
- Visualization generation
- Statistical analysis

**Outputs:**
- Class distribution charts
- Feature histograms
- Correlation heatmaps
- Feature distributions by class
- Box plots

### 3. Model Training Layer

**Components:**
- Training script (`src/models/train.py`)
- MLflow integration
- Model evaluation

**Responsibilities:**
- Model training (Logistic Regression, Random Forest)
- Cross-validation
- Metric calculation
- Model persistence
- Experiment tracking

### 4. Model Packaging Layer

**Components:**
- Model serialization (pickle)
- Preprocessor serialization
- Requirements management

**Outputs:**
- `models/best_model.pkl`
- `models/preprocessor.pkl`
- `requirements.txt`

### 5. API Layer

**Components:**
- FastAPI application (`src/api/app.py`)
- Prediction endpoint
- Health check endpoint
- Metrics endpoint

**Features:**
- RESTful API
- Input validation (Pydantic)
- Error handling
- Prometheus metrics
- Request logging

### 6. Containerization Layer

**Components:**
- Dockerfile
- Docker image
- Container orchestration

**Features:**
- Multi-stage build (optional)
- Dependency management
- Health checks
- Port exposure

### 7. Deployment Layer

**Components:**
- Kubernetes manifests (`k8s/`)
- Deployment scripts
- Service definitions

**Services:**
- API deployment (2 replicas)
- Prometheus deployment
- Grafana deployment
- MLflow UI deployment

### 8. Monitoring Layer

**Components:**
- Prometheus (metrics collection)
- Grafana (visualization)
- API metrics (Prometheus client)

**Metrics:**
- Request count
- Request duration
- Prediction counts
- Error rates

## Data Flow Architecture

### Training Pipeline

```
1. Data Download
   └─▶ UCI Repository
       └─▶ data/raw/heart_disease.csv

2. Data Preprocessing
   └─▶ Load & Clean
       └─▶ Handle Missing Values
           └─▶ Feature Scaling
               └─▶ Train/Test Split

3. Model Training
   └─▶ Train Models
       └─▶ Cross-Validation
           └─▶ Evaluate Metrics
               └─▶ Save Best Model

4. Experiment Tracking
   └─▶ Log to MLflow
       └─▶ Save Artifacts
           └─▶ Store in mlruns/
```

### Inference Pipeline

```
1. API Request
   └─▶ FastAPI Endpoint
       └─▶ Input Validation

2. Preprocessing
   └─▶ Load Preprocessor
       └─▶ Transform Input
           └─▶ Feature Scaling

3. Prediction
   └─▶ Load Model
       └─▶ Predict
           └─▶ Calculate Probability
               └─▶ Return Response

4. Monitoring
   └─▶ Log Request
       └─▶ Update Metrics
           └─▶ Prometheus Scraping
```

## Deployment Architecture

### Kubernetes Cluster (kind)

```
┌─────────────────────────────────────────────────────────┐
│              Kubernetes Cluster (kind)                  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              API Deployment                      │  │
│  │  ┌────────────┐  ┌────────────┐                │  │
│  │  │ API Pod 1  │  │ API Pod 2  │                │  │
│  │  │ (Replica)  │  │ (Replica)  │                │  │
│  │  └────────────┘  └────────────┘                │  │
│  │         │              │                        │  │
│  │         └──────┬───────┘                        │  │
│  │                ▼                                 │  │
│  │         ┌──────────────┐                        │  │
│  │         │ LoadBalancer │                        │  │
│  │         │   Service     │                        │  │
│  │         └──────────────┘                        │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Monitoring Stack                       │  │
│  │  ┌────────────┐         ┌────────────┐          │  │
│  │  │ Prometheus │◀────────│   Grafana  │          │  │
│  │  │  (Scrape)  │         │(Dashboard) │          │  │
│  │  └────────────┘         └────────────┘          │  │
│  │       │                                            │  │
│  │       └────────── Scrape Metrics ──────────┐      │  │
│  │                                             ▼      │  │
│  │                                        API Pods    │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              MLflow UI                            │  │
│  │  ┌────────────────────────────────────────────┐  │  │
│  │  │         MLflow UI Pod                       │  │  │
│  │  │  (Experiment Tracking & Visualization)     │  │  │
│  │  └────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack

### Data & ML
- **Python 3.12** - Programming language
- **Pandas** - Data manipulation
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning
- **MLflow** - Experiment tracking

### API & Web
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Containerization
- **Docker** - Containerization
- **Kubernetes (kind)** - Orchestration

### Monitoring
- **Prometheus** - Metrics collection
- **Grafana** - Visualization
- **Prometheus Client** - Metrics export

### CI/CD
- **GitHub Actions** - CI/CD pipeline
- **Pytest** - Testing framework

## Security Considerations

1. **API Security:**
   - Input validation (Pydantic)
   - Error handling (no sensitive data leakage)
   - Health checks for monitoring

2. **Kubernetes Security:**
   - RBAC for Prometheus
   - Service accounts
   - Resource limits

3. **Model Security:**
   - Model files not in version control
   - Secure model storage
   - Access control via Kubernetes

## Scalability

### Horizontal Scaling
- API pods can be scaled: `kubectl scale deployment heart-disease-api --replicas=5`
- LoadBalancer distributes traffic

### Vertical Scaling
- Resource limits defined in deployment
- Can adjust CPU/memory limits

### Monitoring Scalability
- Prometheus handles multiple targets
- Grafana supports multiple dashboards
- Metrics aggregation automatic

## High Availability

1. **API Replicas:** 2+ pods for redundancy
2. **Health Checks:** Liveness and readiness probes
3. **Service Discovery:** Automatic pod discovery
4. **Load Balancing:** Kubernetes service load balancing

## Architecture Diagrams

### Text-Based Diagrams

See above for ASCII diagrams. For visual diagrams:
1. Use tools like draw.io, Lucidchart, or PlantUML
2. Export as PNG/SVG
3. Store in `documentation/architecture/` folder

### Recommended Tools
- **draw.io** - Free diagramming tool
- **Lucidchart** - Professional diagrams
- **PlantUML** - Code-based diagrams

## Future Enhancements

1. **Model Serving:**
   - MLflow model serving
   - Model versioning API
   - A/B testing framework

2. **Advanced Monitoring:**
   - Alerting rules
   - Custom dashboards
   - Anomaly detection

3. **CI/CD Improvements:**
   - Automated model retraining
   - Model performance monitoring
   - Automated rollbacks

## Summary

✅ **Modular Architecture** - Clear separation of concerns
✅ **Scalable Design** - Horizontal and vertical scaling
✅ **Monitoring Integrated** - Full observability
✅ **Reproducible** - Version controlled and documented
✅ **Production Ready** - Kubernetes deployment with HA

