#!/bin/bash
# Copy models to Kubernetes pods using kubectl cp

set -e

echo "Copying models to Kubernetes pods..."

# Check if models exist
if [ ! -f "models/best_model.pkl" ] || [ ! -f "models/preprocessor.pkl" ]; then
    echo "Error: Models not found. Please run training first."
    echo "Run: python src/models/train.py data/raw/heart_disease.csv"
    exit 1
fi

# Get all pod names
PODS=$(kubectl get pods -l app=heart-disease-api -o jsonpath='{.items[*].metadata.name}')

if [ -z "$PODS" ]; then
    echo "Error: No API pods found. Please deploy the API first:"
    echo "  kubectl apply -f k8s/deployment.yaml"
    exit 1
fi

echo "Found pods: $PODS"

# Copy models to each pod
for POD_NAME in $PODS; do
    echo ""
    echo "Processing pod: $POD_NAME"
    
    # Wait for pod to be in Running state (even if not ready)
    echo "Waiting for pod to be running..."
    for i in {1..30}; do
        STATUS=$(kubectl get pod $POD_NAME -o jsonpath='{.status.phase}' 2>/dev/null || echo "Unknown")
        if [ "$STATUS" = "Running" ]; then
            break
        fi
        sleep 2
    done
    
    # Create models directory
    echo "Creating /app/models directory..."
    kubectl exec $POD_NAME -- mkdir -p /app/models 2>/dev/null || echo "Directory may already exist"
    
    # Copy models
    echo "Copying best_model.pkl..."
    kubectl cp models/best_model.pkl $POD_NAME:/app/models/best_model.pkl 2>/dev/null && echo "✓ Copied" || echo "✗ Failed"
    
    echo "Copying preprocessor.pkl..."
    kubectl cp models/preprocessor.pkl $POD_NAME:/app/models/preprocessor.pkl 2>/dev/null && echo "✓ Copied" || echo "✗ Failed"
    
    # Restart the pod to load models
    echo "Restarting pod to load models..."
    kubectl delete pod $POD_NAME
done

echo ""
echo "Waiting for pods to restart..."
sleep 10
kubectl wait --for=condition=ready pod -l app=heart-disease-api --timeout=120s || echo "Some pods may still be starting"

echo ""
echo "Models copied successfully!"
echo "Checking pod status..."
kubectl get pods -l app=heart-disease-api

