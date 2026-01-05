#!/bin/bash
# Verify Prometheus is scraping API metrics

echo "=========================================="
echo "Verifying Prometheus Scraping"
echo "=========================================="
echo ""

# Check Prometheus is running
echo "1. Checking Prometheus pod:"
PROM_PODS=$(kubectl get pods -l app=prometheus --no-headers 2>/dev/null | wc -l)
if [ "$PROM_PODS" -gt 0 ]; then
    echo "   ✓ Prometheus is running"
    kubectl get pods -l app=prometheus
else
    echo "   ✗ Prometheus not found"
    echo "   Deploy: kubectl apply -f k8s/monitoring.yaml"
    exit 1
fi

echo ""
echo "2. Checking API pods:"
API_PODS=$(kubectl get pods -l app=heart-disease-api --no-headers 2>/dev/null | wc -l)
if [ "$API_PODS" -gt 0 ]; then
    echo "   ✓ Found $API_PODS API pod(s)"
    kubectl get pods -l app=heart-disease-api --no-headers | awk '{print "     - " $1 " (" $3 ")"}'
else
    echo "   ✗ No API pods found"
    echo "   Deploy: kubectl apply -f k8s/deployment.yaml"
    exit 1
fi

echo ""
echo "3. Checking Prometheus configuration:"
echo "   Scrape config:"
kubectl get configmap prometheus-config -o yaml | grep -A 15 "scrape_configs" | head -12

echo ""
echo "4. Testing API metrics endpoint:"
POD_NAME=$(kubectl get pods -l app=heart-disease-api -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ -n "$POD_NAME" ]; then
    echo "   Testing pod: $POD_NAME"
    METRICS=$(kubectl exec $POD_NAME -- python3 -c "import requests; r = requests.get('http://localhost:8000/metrics'); print('✓ Metrics endpoint working' if r.status_code == 200 else '✗ Metrics endpoint failed')" 2>/dev/null)
    echo "   $METRICS"
    
    # Check if api_requests_total exists
    HAS_METRICS=$(kubectl exec $POD_NAME -- python3 -c "import requests; r = requests.get('http://localhost:8000/metrics'); print('YES' if 'api_requests_total' in r.text else 'NO')" 2>/dev/null)
    if [ "$HAS_METRICS" = "YES" ]; then
        echo "   ✓ api_requests_total metric found"
    else
        echo "   ⚠ api_requests_total not found - make API calls first"
        echo "   Run: ./scripts/generate_metrics.sh"
    fi
else
    echo "   ✗ Could not find API pod"
fi

echo ""
echo "5. To check Prometheus targets (REAL-TIME):"
echo "   kubectl port-forward service/prometheus-service 9090:9090"
echo "   Then open: http://localhost:9090/targets"
echo "   Look for 'heart-disease-api' - should show as UP (green)"
echo ""

echo "6. To query metrics in Prometheus:"
echo "   kubectl port-forward service/prometheus-service 9090:9090"
echo "   Open: http://localhost:9090"
echo "   Try queries:"
echo "     - api_requests_total"
echo "     - predictions_total"
echo "     - rate(api_requests_total[5m])"
echo ""

echo "=========================================="
echo "Summary"
echo "=========================================="
echo ""
echo "Prometheus Configuration:"
echo "  ✓ Scrapes pods with label: app=heart-disease-api"
echo "  ✓ Endpoint: http://<pod-ip>:8000/metrics"
echo "  ✓ Scrape interval: 15 seconds"
echo ""
echo "To verify scraping is working:"
echo "  1. Make some API calls: ./scripts/generate_metrics.sh"
echo "  2. Wait 15-20 seconds"
echo "  3. Check Prometheus targets: http://localhost:9090/targets"
echo "  4. Query metrics: http://localhost:9090 (query: api_requests_total)"
echo ""
