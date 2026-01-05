                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            #!/bin/bash
# Complete pipeline script for MLOps assignment

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Set PYTHONPATH to project root
export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"

# Change to project root
cd "$PROJECT_ROOT"

echo "=========================================="
echo "MLOps Pipeline - Heart Disease Prediction"
echo "=========================================="

# Step 1: Download data
echo ""
echo "Step 1: Downloading dataset..."
python src/data/download_data.py

# Step 2: EDA
echo ""
echo "Step 2: Running Exploratory Data Analysis..."
python -c "from src.eda.explore import perform_eda; perform_eda('data/raw/heart_disease.csv')"

# Step 3: Train models
echo ""
echo "Step 3: Training models with MLflow tracking..."
python src/models/train.py data/raw/heart_disease.csv

echo ""
echo "=========================================="
echo "Pipeline completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Check MLflow UI: mlflow ui"
echo "2. Build Docker image: docker build -t heart-disease-api:latest ."
echo "3. Run locally: docker run -p 8000:8000 heart-disease-api:latest"
echo "4. Deploy to Kubernetes: kubectl apply -f k8s/"

