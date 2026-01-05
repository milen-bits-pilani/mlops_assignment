# CI/CD Pipeline Documentation

## Overview

This project uses **GitHub Actions** for continuous integration and continuous deployment (CI/CD). The pipeline automates testing, linting, model training, and Docker image building.

## Pipeline Location

**File:** `.github/workflows/ci_cd.yml`

## Pipeline Stages

### Stage 1: Code Linting

**Purpose:** Ensure code quality and consistency

**Steps:**
1. Checkout code
2. Set up Python 3.12
3. Install linting tools:
   - Black (code formatting)
   - Flake8 (style checking)
   - Pylint (code analysis)

**Checks:**
- ✅ Black formatting check
- ✅ Flake8 style check
- ✅ Pylint code analysis

**Failure Action:** Pipeline fails if code doesn't meet standards

### Stage 2: Unit Testing

**Purpose:** Verify code correctness

**Steps:**
1. Install dependencies
2. Run pytest with coverage
3. Generate coverage reports

**Tests:**
- `tests/test_preprocess.py` - Preprocessing tests
- `tests/test_models.py` - Model training tests
- `tests/test_api.py` - API endpoint tests

**Outputs:**
- Coverage report (XML)
- HTML coverage report
- Test results

**Failure Action:** Pipeline fails if tests fail

### Stage 3: Model Training

**Purpose:** Train models and verify training pipeline

**Steps:**
1. Install dependencies
2. Download dataset
3. Run EDA
4. Train models with MLflow
5. Upload artifacts:
   - Trained models
   - EDA visualizations
   - MLflow runs

**Artifacts:**
- `models/` directory
- `data/eda/` visualizations
- `mlruns/` experiment data

**Failure Action:** Pipeline fails if training fails

### Stage 4: Docker Build

**Purpose:** Build and test Docker image

**Steps:**
1. Download model artifacts
2. Set up Docker Buildx
3. Build Docker image
4. Test Docker image:
   - Run container
   - Health check
   - Cleanup

**Image:** `heart-disease-api:latest`

**Failure Action:** Pipeline fails if build or test fails

## Pipeline Triggers

### Automatic Triggers

1. **Push to main/develop:**
   - Runs full pipeline
   - All stages executed

2. **Pull Request:**
   - Runs linting and testing
   - Skips deployment stages

### Manual Triggers

- Can be triggered manually from GitHub Actions UI
- Useful for testing pipeline changes

## Workflow Dependencies

```
Lint ──┐
       ├──▶ Test ──▶ Train ──▶ Build
       └──┘
```

- **Lint** and **Test** run in parallel
- **Train** depends on Test
- **Build** depends on Train

## Artifacts Management

### Uploaded Artifacts

1. **Models:**
   - Retention: 7 days
   - Location: `models/` directory

2. **MLflow Runs:**
   - Retention: 7 days
   - Location: `mlruns/` directory

3. **Coverage Reports:**
   - Uploaded to Codecov
   - HTML reports generated

## Environment Variables

No secrets required for this pipeline (all public resources).

## Pipeline Output

### Success Output

```
✅ Lint: Code passes all checks
✅ Test: All tests pass
✅ Train: Models trained successfully
✅ Build: Docker image built and tested
```

### Failure Output

Pipeline stops at first failure with:
- Error message
- Logs for debugging
- Artifact uploads (if available)

## Local CI/CD Testing

### Run Linting Locally

```bash
# Black
black --check src/ tests/

# Flake8
flake8 src/ tests/ --max-line-length=120

# Pylint
pylint src/ tests/
```

### Run Tests Locally

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=src --cov-report=html
```

### Run Training Locally

```bash
# Download data
python src/data/download_data.py

# Train models
python src/models/train.py data/raw/heart_disease.csv
```

### Build Docker Locally

```bash
# Build image
docker build -t heart-disease-api:latest .

# Test image
docker run -d -p 8000:8000 --name test-api heart-disease-api:latest
sleep 10
curl http://localhost:8000/health
docker stop test-api && docker rm test-api
```

## CI/CD Best Practices

### ✅ Implemented

1. **Automated Testing** - All code changes tested
2. **Code Quality Checks** - Linting enforced
3. **Artifact Management** - Models and data saved
4. **Docker Testing** - Images tested before use
5. **Parallel Execution** - Lint and test run in parallel

### 🔄 Future Improvements

1. **Automated Deployment** - Deploy to staging/production
2. **Model Performance Checks** - Validate model metrics
3. **Security Scanning** - Dependency vulnerability checks
4. **Notification System** - Slack/email on failures
5. **Rollback Mechanism** - Automatic rollback on failure

## Pipeline Screenshots

### Where to Capture

1. **GitHub Actions UI:**
   - Pipeline execution view
   - Individual job logs
   - Artifact downloads

2. **Test Results:**
   - Coverage reports
   - Test output

3. **Docker Build:**
   - Build logs
   - Test results

**Store in:** `documentation/screenshots/ci_cd/`

## Troubleshooting

### Common Issues

1. **Linting Failures:**
   - Run `black src/ tests/` to auto-format
   - Fix Flake8 warnings
   - Address Pylint suggestions

2. **Test Failures:**
   - Run tests locally first
   - Check test logs
   - Verify dependencies

3. **Training Failures:**
   - Check data availability
   - Verify MLflow setup
   - Check disk space

4. **Docker Build Failures:**
   - Test Dockerfile locally
   - Check base image availability
   - Verify build context

## Pipeline Configuration

### Key Settings

- **Python Version:** 3.12
- **OS:** ubuntu-latest
- **Timeout:** Default (no explicit timeout)
- **Concurrency:** One run per branch

### Resource Usage

- **Lint Job:** ~2 minutes
- **Test Job:** ~3-5 minutes
- **Train Job:** ~5-10 minutes
- **Build Job:** ~3-5 minutes

**Total:** ~15-25 minutes

## Summary

✅ **Automated Pipeline** - Runs on every push/PR
✅ **Quality Checks** - Linting and testing enforced
✅ **Model Training** - Automated training in CI
✅ **Docker Testing** - Images validated
✅ **Artifact Management** - Models and data preserved

**Pipeline Status:** Fully functional and tested

