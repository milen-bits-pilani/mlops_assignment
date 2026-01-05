#!/bin/bash
# Prepare models for Kubernetes deployment
# This script copies models to a location accessible by kind

set -e

echo "Preparing models for Kubernetes deployment..."

# Check if models exist
if [ ! -f "models/best_model.pkl" ] || [ ! -f "models/preprocessor.pkl" ]; then
    echo "Error: Models not found. Please run training first."
    echo "Run: python src/models/train.py data/raw/heart_disease.csv"
    exit 1
fi

# Create directory on kind node
echo "Copying models to kind node..."
kind get nodes --name kind | head -1 | xargs -I {} docker exec {} mkdir -p /tmp/models

# Copy models
kind get nodes --name kind | head -1 | xargs -I {} docker cp models/best_model.pkl {}:/tmp/models/
kind get nodes --name kind | head -1 | xargs -I {} docker cp models/preprocessor.pkl {}:/tmp/models/

echo "Models prepared for Kubernetes deployment!"

