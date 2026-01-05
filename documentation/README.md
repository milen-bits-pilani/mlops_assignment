# MLOps Assignment - Complete Documentation

This folder contains all documentation required for Task 9: Documentation & Reporting.

## Contents

1. **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Complete setup and installation guide
2. **[EDA_AND_MODELING.md](EDA_AND_MODELING.md)** - EDA findings and modeling choices
3. **[EXPERIMENT_TRACKING.md](EXPERIMENT_TRACKING.md)** - MLflow experiment tracking summary
4. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design
5. **[CI_CD_WORKFLOW.md](CI_CD_WORKFLOW.md)** - CI/CD pipeline documentation
6. **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Kubernetes deployment instructions
7. **[REPRODUCIBILITY_GUIDE.md](REPRODUCIBILITY_GUIDE.md)** - Step-by-step reproduction guide
8. **[screenshots/](screenshots/)** - Screenshots folder for visual documentation

## Quick Start for Evaluators

To reproduce this project from scratch:

1. **Read:** [REPRODUCIBILITY_GUIDE.md](REPRODUCIBILITY_GUIDE.md)
2. **Follow:** [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)
3. **Run:** Complete pipeline as documented

## Project Overview

**Project:** Heart Disease Prediction MLOps Pipeline
**Dataset:** Heart Disease UCI Dataset
**Objective:** End-to-end ML model development, CI/CD, and production deployment

## Key Components

- ✅ Data Acquisition & EDA
- ✅ Feature Engineering & Model Development
- ✅ Experiment Tracking (MLflow)
- ✅ Model Packaging & Reproducibility
- ✅ CI/CD Pipeline & Automated Testing
- ✅ Model Containerization (Docker)
- ✅ Production Deployment (Kubernetes/kind)
- ✅ Monitoring & Logging (Prometheus + Grafana)

## Repository Structure

```
mlops_project/
├── src/                    # Source code
│   ├── data/              # Data acquisition & preprocessing
│   ├── eda/               # Exploratory Data Analysis
│   ├── models/            # Model training
│   └── api/               # FastAPI application
├── tests/                 # Unit tests
├── k8s/                   # Kubernetes manifests
├── scripts/               # Utility scripts
├── .github/workflows/     # CI/CD pipeline
├── documentation/         # This folder
└── requirements.txt       # Python dependencies
```

## Contact & Support

For questions or issues, refer to the individual documentation files or the main [README.md](../README.md) in the project root.

