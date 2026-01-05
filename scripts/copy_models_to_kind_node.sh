#!/bin/bash
# Copy models to kind node's /tmp/models directory

set -e

KIND_CLUSTER="local-k8s-1"

echo "Copying models to kind node..."

# Check if models exist
if [ ! -f "models/best_model.pkl" ] || [ ! -f "models/preprocessor.pkl" ]; then
    echo "Error: Models not found. Please run training first."
    echo "Run: python src/models/train.py data/raw/heart_disease.csv"
    exit 1
fi

# Get kind node name
NODE_NAME=$(kind get nodes --name ${KIND_CLUSTER} 2>/dev/null | head -1)

if [ -z "$NODE_NAME" ]; then
    echo "Error: Kind cluster '${KIND_CLUSTER}' not found"
    echo "Available clusters:"
    kind get clusters
    exit 1
fi

echo "Found kind node: $NODE_NAME"

# Create directory on kind node
echo "Creating /tmp/models directory on kind node..."
docker exec $NODE_NAME mkdir -p /tmp/models

# Copy models
echo "Copying best_model.pkl..."
docker cp models/best_model.pkl $NODE_NAME:/tmp/models/best_model.pkl

echo "Copying preprocessor.pkl..."
docker cp models/preprocessor.pkl $NODE_NAME:/tmp/models/preprocessor.pkl

# Verify
echo "Verifying models on kind node..."
docker exec $NODE_NAME ls -lh /tmp/models/

echo ""
echo "✓ Models copied successfully to kind node!"
echo ""
echo "You can now deploy or restart the API:"
echo "  kubectl apply -f k8s/deployment.yaml"
echo "  kubectl rollout restart deployment/heart-disease-api"

