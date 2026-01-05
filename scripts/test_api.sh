#!/bin/bash
# Test script for API endpoints

API_URL=${1:-http://localhost:8000}

echo "Testing Heart Disease Prediction API at $API_URL"
echo "=========================================="

# Test root endpoint
echo ""
echo "1. Testing root endpoint..."
curl -s $API_URL/ | jq '.' || echo "Failed"

# Test health endpoint
echo ""
echo "2. Testing health endpoint..."
curl -s $API_URL/health | jq '.' || echo "Failed"

# Test predict endpoint
echo ""
echo "3. Testing predict endpoint..."
curl -s -X POST $API_URL/predict \
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
  }' | jq '.' || echo "Failed"

# Test metrics endpoint
echo ""
echo "4. Testing metrics endpoint..."
curl -s $API_URL/metrics | head -20 || echo "Failed"

echo ""
echo "=========================================="
echo "API testing complete!"

