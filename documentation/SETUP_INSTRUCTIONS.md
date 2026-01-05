# Setup and Installation Instructions

## Prerequisites

### Required Software

1. **Python 3.12+**
   ```bash
   python3 --version  # Should be 3.12 or higher
   ```

2. **Docker**
   ```bash
   docker --version
   ```

3. **Kubernetes (kind)**
   ```bash
   kind --version
   ```

4. **kubectl**
   ```bash
   kubectl version --client
   ```

### System Requirements

- **OS:** Linux (Ubuntu/Debian recommended) or macOS
- **RAM:** Minimum 4GB (8GB recommended)
- **Disk Space:** At least 5GB free
- **CPU:** 2+ cores recommended

## Installation Steps

### 1. Clone/Download the Repository

```bash
# If using git
git clone <repository-url>
cd mlops_project

# Or extract the project folder
cd mlops_project
```

### 2. Create Python Virtual Environment

```bash
# Create virtual environment
python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows
```

### 3. Install Python Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

### 4. Initialize Project Directories

```bash
# Run initialization script
./scripts/init_project.sh

# Or manually create directories
mkdir -p data/raw data/eda models mlruns screenshots logs
```

### 5. Verify Installation

```bash
# Run verification script
python verify_setup.py

# Should show all components as ✅
```

## Environment Setup

### Python Environment

The project uses Python 3.12 with the following key packages:
- `pandas`, `numpy`, `scikit-learn` - Data processing and ML
- `mlflow` - Experiment tracking
- `fastapi`, `uvicorn` - API framework
- `pytest` - Testing
- `prometheus-client` - Metrics

### Docker Setup

Ensure Docker is running:
```bash
docker ps  # Should not error
```

### Kubernetes (kind) Setup

Create a kind cluster (if not exists):
```bash
kind get clusters  # Check existing clusters

# Create new cluster if needed
kind create cluster --name local-k8s-1
```

## Quick Verification

### Test Python Environment

```bash
python -c "import pandas, sklearn, mlflow, fastapi; print('All imports successful')"
```

### Test Docker

```bash
docker run hello-world
```

### Test Kubernetes

```bash
kubectl cluster-info
```

## Troubleshooting

### Python Issues

**Problem:** `pip install` fails
- **Solution:** Upgrade pip: `pip install --upgrade pip`
- **Solution:** Use Python 3.12 specifically

**Problem:** Import errors
- **Solution:** Ensure virtual environment is activated
- **Solution:** Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

### Docker Issues

**Problem:** Permission denied
- **Solution:** Add user to docker group: `sudo usermod -aG docker $USER`
- **Solution:** Restart terminal or logout/login

### Kubernetes Issues

**Problem:** `kubectl` not found
- **Solution:** Install kubectl: https://kubernetes.io/docs/tasks/tools/
- **Solution:** Configure kubeconfig for kind: `kind get kubeconfig --name local-k8s-1 > ~/.kube/config`

**Problem:** Kind cluster not found
- **Solution:** Create cluster: `kind create cluster --name local-k8s-1`

## Next Steps

After setup, proceed to:
1. **[REPRODUCIBILITY_GUIDE.md](REPRODUCIBILITY_GUIDE.md)** - Run the complete pipeline
2. **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Deploy to Kubernetes

## Additional Resources

- Project README: [../README.md](../README.md)
- Quick Start: [../QUICKSTART.md](../QUICKSTART.md)
- Requirements file: [../requirements.txt](../requirements.txt)

