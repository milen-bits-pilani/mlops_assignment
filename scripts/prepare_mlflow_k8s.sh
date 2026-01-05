#!/bin/bash
# Prepare MLflow runs for Kubernetes deployment
# This script copies mlruns to a location accessible by kind

set -e

echo "Preparing MLflow runs for Kubernetes deployment..."

# Check if mlruns exists
if [ ! -d "mlruns" ]; then
    echo "Error: mlruns directory not found. Please run training first."
    echo "Run: python src/models/train.py data/raw/heart_disease.csv"
    exit 1
fi

# Create directory on kind node
echo "Copying mlruns to kind node..."
kind get nodes --name kind | head -1 | xargs -I {} docker exec {} mkdir -p /tmp/mlruns

# Copy mlruns directory
echo "Copying MLflow runs..."
kind get nodes --name kind | head -1 | xargs -I {} docker cp mlruns/. {}:/tmp/mlruns/

echo "MLflow runs prepared for Kubernetes deployment!"
echo "You can now deploy MLflow UI: kubectl apply -f k8s/mlflow-ui.yaml"

