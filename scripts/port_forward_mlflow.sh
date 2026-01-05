#!/bin/bash
# Port forward MLflow UI - tries service first, then pod directly

echo "=========================================="
echo "Port Forwarding MLflow UI"
echo "=========================================="
echo ""

# Try service first
echo "Attempting to port-forward via service..."
kubectl port-forward svc/mlflow-ui-service 5000:5000 2>&1 &
PF_PID=$!
sleep 3

# Test connection
if curl -s http://localhost:5000 > /dev/null 2>&1; then
    echo "✅ Service port-forward working!"
    echo ""
    echo "MLflow UI is available at: http://localhost:5000"
    echo ""
    echo "Press Ctrl+C to stop port-forwarding"
    wait $PF_PID
else
    echo "⚠️  Service port-forward failed, trying direct pod connection..."
    kill $PF_PID 2>/dev/null || true
    
    # Get pod name
    POD_NAME=$(kubectl get pods -l app=mlflow-ui -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    
    if [ -z "$POD_NAME" ]; then
        echo "❌ Error: No MLflow UI pod found"
        exit 1
    fi
    
    echo "Found pod: $POD_NAME"
    echo "Port-forwarding directly to pod..."
    echo ""
    echo "MLflow UI will be available at: http://localhost:5000"
    echo "Press Ctrl+C to stop"
    echo ""
    
    kubectl port-forward pod/$POD_NAME 5000:5000
fi

