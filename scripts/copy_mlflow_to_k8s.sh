#!/bin/bash
# Copy MLflow runs to Kubernetes pod using kubectl cp

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "Copying MLflow Data to Kubernetes Pod"
echo "=========================================="
echo ""

# Check if mlruns exists
if [ ! -d "mlruns" ]; then
    echo "❌ Error: mlruns directory not found. Please run training first."
    echo "   Run: python src/models/train.py data/raw/heart_disease.csv"
    exit 1
fi

echo "✅ Found mlruns directory"
echo ""

# Wait for pod to be ready
echo "Waiting for MLflow UI pod to be ready..."
kubectl wait --for=condition=ready pod -l app=mlflow-ui --timeout=120s 2>/dev/null || {
    echo "❌ Error: MLflow UI pod not found. Please deploy it first:"
    echo "   kubectl apply -f k8s/mlflow-ui.yaml"
    exit 1
}

# Get pod name
POD_NAME=$(kubectl get pods -l app=mlflow-ui -o jsonpath='{.items[0].metadata.name}')
echo "✅ Found pod: $POD_NAME"
echo ""

# Clear existing data in pod
echo "Clearing existing data in pod..."
kubectl exec $POD_NAME -- rm -rf /mlruns/* 2>/dev/null || true
kubectl exec $POD_NAME -- mkdir -p /mlruns 2>/dev/null || true

# Copy each experiment directory
echo "Copying experiments to pod..."
for exp_dir in mlruns/*/; do
    if [ -d "$exp_dir" ] && [ "$(basename $exp_dir)" != ".trash" ]; then
        exp_name=$(basename $exp_dir)
        echo "  Copying experiment: $exp_name"
        kubectl cp "$exp_dir" $POD_NAME:/mlruns/$exp_name
    fi
done

# Verify data was copied
echo ""
echo "Verifying data in pod..."
EXPERIMENTS=$(kubectl exec $POD_NAME -- ls /mlruns/ 2>/dev/null | grep -E "^[0-9]" | wc -l)
if [ "$EXPERIMENTS" -gt 0 ]; then
    echo "✅ Found $EXPERIMENTS experiment(s) in pod"
    kubectl exec $POD_NAME -- ls /mlruns/ | grep -E "^[0-9]"
else
    echo "⚠️  Warning: No experiments found in pod"
fi

# Restart the pod to pick up the new data
echo ""
echo "Restarting pod to load MLflow data..."
kubectl delete pod $POD_NAME

echo "Waiting for pod to restart..."
kubectl wait --for=condition=ready pod -l app=mlflow-ui --timeout=120s

NEW_POD=$(kubectl get pods -l app=mlflow-ui -o jsonpath='{.items[0].metadata.name}')
echo "✅ Pod restarted: $NEW_POD"

# Final verification
echo ""
echo "Final verification..."
sleep 3
FINAL_EXPERIMENTS=$(kubectl exec $NEW_POD -- ls /mlruns/ 2>/dev/null | grep -E "^[0-9]" | wc -l)
if [ "$FINAL_EXPERIMENTS" -gt 0 ]; then
    echo "✅ MLflow data is ready in pod!"
    echo ""
    echo "Experiments found:"
    kubectl exec $NEW_POD -- ls /mlruns/ | grep -E "^[0-9]"
else
    echo "⚠️  Warning: Data may not have persisted. The pod uses hostPath mount."
    echo "   Try accessing MLflow UI - it may still work if data is in the mount."
fi

echo ""
echo "=========================================="
echo "✅ Copy process complete!"
echo "=========================================="
echo ""
echo "Access MLflow UI:"
echo "  kubectl port-forward service/mlflow-ui-service 5000:5000"
echo "  Then open: http://localhost:5000"
echo ""
echo "You should now see the 'heart_disease' experiment with all runs!"
echo ""
