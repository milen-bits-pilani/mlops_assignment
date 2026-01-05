# Code Repository Information

## Repository Structure

```
mlops_project/
├── src/                          # Source code
│   ├── data/                     # Data acquisition & preprocessing
│   │   ├── download_data.py      # Dataset download
│   │   └── preprocess.py         # Preprocessing pipeline
│   ├── eda/                      # Exploratory Data Analysis
│   │   └── explore.py            # EDA script with visualizations
│   ├── models/                   # Model training
│   │   └── train.py              # Training with MLflow
│   └── api/                      # FastAPI application
│       └── app.py                # API endpoints
├── tests/                        # Unit tests
│   ├── test_preprocess.py        # Preprocessing tests
│   ├── test_models.py            # Model tests
│   └── test_api.py               # API tests
├── k8s/                         # Kubernetes manifests
│   ├── deployment.yaml           # API deployment
│   ├── monitoring.yaml           # Prometheus & Grafana
│   ├── mlflow-ui.yaml            # MLflow UI
│   └── prometheus-rbac.yaml      # RBAC for Prometheus
├── scripts/                      # Utility scripts
│   ├── run_pipeline.sh           # Complete pipeline
│   ├── deploy_k8s.sh             # K8s deployment
│   ├── build_and_load_k8s.sh    # Docker build & load
│   ├── copy_models_to_k8s.sh    # Copy models to pods
│   └── generate_metrics.sh       # Generate API metrics
├── .github/workflows/            # CI/CD pipeline
│   └── ci_cd.yml                 # GitHub Actions workflow
├── documentation/                # This documentation
├── Dockerfile                    # Container definition
├── requirements.txt              # Python dependencies
└── README.md                     # Project README
```

## Key Files

### Core Application
- `src/api/app.py` - FastAPI application with `/predict` endpoint
- `src/models/train.py` - Model training with MLflow
- `src/data/preprocess.py` - Preprocessing pipeline
- `src/eda/explore.py` - EDA with visualizations

### Configuration
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker image definition
- `k8s/*.yaml` - Kubernetes manifests
- `.github/workflows/ci_cd.yml` - CI/CD pipeline

### Scripts
- `scripts/run_pipeline.sh` - Complete pipeline execution
- `scripts/deploy_k8s.sh` - Kubernetes deployment
- `scripts/build_and_load_k8s.sh` - Docker image management

## Code Organization

### Modular Design
- **Data Layer:** Separate data acquisition and preprocessing
- **EDA Layer:** Independent EDA module
- **Model Layer:** Training with experiment tracking
- **API Layer:** RESTful API with metrics
- **Deployment Layer:** Kubernetes manifests

### Best Practices
- ✅ Type hints throughout
- ✅ Docstrings for all functions
- ✅ Error handling
- ✅ Logging
- ✅ Unit tests
- ✅ Code linting

## Dependencies

See `requirements.txt` for complete list. Key dependencies:

- **ML:** pandas, numpy, scikit-learn
- **Tracking:** mlflow
- **API:** fastapi, uvicorn
- **Testing:** pytest, pytest-cov
- **Monitoring:** prometheus-client
- **Visualization:** matplotlib, seaborn

## Version Control

### Git Setup (if using)

```bash
# Initialize repository
git init

# Add files
git add .

# Commit
git commit -m "Initial MLOps project commit"

# Add remote (if applicable)
git remote add origin <repository-url>
git push -u origin main
```

### .gitignore

The project includes `.gitignore` to exclude:
- Virtual environments
- Model files (*.pkl)
- MLflow runs (mlruns/)
- Data files (data/raw/, data/eda/)
- Docker images (*.tar)
- Python cache files

## Code Quality

### Linting
- **Black** - Code formatting
- **Flake8** - Style checking
- **Pylint** - Code analysis

### Testing
- **Pytest** - Test framework
- **Coverage** - Code coverage
- **Unit tests** - All modules tested

### CI/CD
- **GitHub Actions** - Automated testing
- **Docker** - Container testing
- **Kubernetes** - Deployment validation

## Reproducibility

### Fixed Seeds
- All random operations use `random_state=42`
- Ensures reproducible results

### Version Pinning
- All dependencies have specific versions
- `requirements.txt` ensures consistency

### Environment
- Virtual environment isolation
- Docker containerization
- Kubernetes namespace isolation

## Documentation

- **README.md** - Project overview
- **QUICKSTART.md** - Quick start guide
- **documentation/** - Complete documentation
- **Code comments** - Inline documentation
- **Docstrings** - Function documentation

## License

This project is for educational purposes as part of MLOps assignment.

## Contact

For questions or issues:
1. Check documentation in `documentation/` folder
2. Review README.md
3. Check code comments and docstrings

## Repository Link

**Note:** If this is a Git repository, provide the repository URL here:

```
Repository URL: <your-repository-url>
```

For local evaluation, the complete code is in this directory structure.

