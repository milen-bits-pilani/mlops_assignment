#!/bin/bash
# Start MLflow UI

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

cd "$PROJECT_ROOT"

echo "=========================================="
echo "Starting MLflow UI"
echo "=========================================="
echo ""
echo "MLflow UI will be available at:"
echo "  http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Check if mlruns directory exists
if [ ! -d "mlruns" ]; then
    echo "Warning: mlruns directory not found."
    echo "Run model training first to generate experiments."
    echo ""
fi

# Start MLflow UI with explicit backend store URI
mlflow ui --host 0.0.0.0 --port 5000 --backend-store-uri file://$(pwd)/mlruns

