#!/bin/bash
# Kubernetes deployment script for kind

set -e

echo "=========================================="
echo "Deploying to Kubernetes (kind)"
echo "=========================================="

# Check if kind cluster exists
KIND_CLUSTER="local-k8s-1"
if ! kind get clusters | grep -q "${KIND_CLUSTER}"; then
    echo "Creating kind cluster..."
    kind create cluster --name ${KIND_CLUSTER}
fi

# Build, save, and load Docker image into kind
echo "Building and loading Docker image into kind..."
if [ -f "scripts/build_and_load_k8s.sh" ]; then
    ./scripts/build_and_load_k8s.sh
else
    echo "Building Docker image..."
    docker build -t heart-disease-api:latest .
    echo "Saving image to tar..."
    docker save heart-disease-api:latest -o heart-disease-api.tar
    echo "Loading image into kind..."
    sudo kind load image-archive heart-disease-api.tar --name ${KIND_CLUSTER}
fi

# Prepare models
echo "Preparing models for deployment..."
if [ -f "scripts/prepare_k8s_models.sh" ]; then
    ./scripts/prepare_k8s_models.sh
else
    echo "Warning: prepare_k8s_models.sh not found. Models may not be available."
fi

# Apply Kubernetes manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f k8s/deployment.yaml

# Wait for deployment
echo "Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/heart-disease-api

# Apply monitoring
echo "Applying monitoring stack..."
kubectl apply -f k8s/monitoring.yaml

# Apply MLflow UI (optional)
echo "Applying MLflow UI..."
kubectl apply -f k8s/mlflow-ui.yaml
kubectl wait --for=condition=ready pod -l app=mlflow-ui --timeout=120s || true

# Copy MLflow data
if [ -d "mlruns" ]; then
    echo "Copying MLflow data to pod..."
    ./scripts/copy_mlflow_to_k8s.sh || echo "Warning: Could not copy MLflow data"
fi

# Get service info
echo ""
echo "=========================================="
echo "Deployment Status:"
echo "=========================================="
kubectl get pods -l app=heart-disease-api
kubectl get services

echo ""
echo "To access the API:"
echo "  kubectl port-forward service/heart-disease-api-service 8000:80"
echo ""
echo "To access Prometheus:"
echo "  kubectl port-forward service/prometheus-service 9090:9090"
echo ""
echo "To access Grafana:"
echo "  kubectl port-forward service/grafana-service 3000:3000"
echo "  Default credentials: admin/admin"
echo ""
echo "To access MLflow UI:"
echo "  kubectl port-forward service/mlflow-ui-service 5000:5000"
echo "  Or access via NodePort: http://<node-ip>:30050"

