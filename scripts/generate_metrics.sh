#!/bin/bash
# Generate API metrics by making requests

echo "Generating API metrics..."

# Port forward API (in background)
kubectl port-forward service/heart-disease-api-service 8000:80 > /dev/null 2>&1 &
PF_PID=$!
sleep 3

echo "Making API calls to generate metrics..."

# Make some requests to generate metrics
for i in {1..10}; do
  echo -n "."
  curl -s -X POST http://localhost:8000/predict \
    -H "Content-Type: application/json" \
    -d '{
      "age": 63,
      "sex": 1,
      "cp": 3,
      "trestbps": 145,
      "chol": 233,
      "fbs": 1,
      "restecg": 0,
      "thalach": 150,
      "exang": 0,
      "oldpeak": 2.3,
      "slope": 0,
      "ca": 0,
      "thal": 1
    }' > /dev/null 2>&1
  sleep 0.5
done

echo ""
echo "Checking metrics..."

# Check metrics
METRICS=$(curl -s http://localhost:8000/metrics 2>/dev/null | grep "api_requests_total" | grep -v "^#")

if [ -n "$METRICS" ]; then
    echo ""
    echo "✅ Metrics found:"
    echo "$METRICS" | head -5
    echo ""
    echo "Full metrics available at: http://localhost:8000/metrics"
else
    echo ""
    echo "⚠️  No metrics yet. Try making more API calls."
fi

# Kill port forward
kill $PF_PID 2>/dev/null || true

echo ""
echo "To check metrics directly:"
echo "  kubectl port-forward service/heart-disease-api-service 8000:80"
echo "  curl http://localhost:8000/metrics | grep api_requests_total"

