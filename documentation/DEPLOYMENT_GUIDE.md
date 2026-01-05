# Deployment Guide

## Overview

This guide covers deployment of the Heart Disease Prediction API to Kubernetes using kind (Kubernetes in Docker).

## Prerequisites

1. **Docker** installed and running
2. **kind** installed
3. **kubectl** installed and configured
4. **Trained models** available in `models/` directory

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│         Kubernetes Cluster (kind)        │
│                                          │
│  ┌──────────────┐  ┌──────────────┐     │
│  │ API Pod 1    │  │ API Pod 2    │     │
│  │ (Replica)    │  │ (Replica)    │     │
│  └──────┬───────┘  └──────┬───────┘     │
│         │                  │             │
│         └────────┬─────────┘             │
│                  ▼                       │
│         ┌──────────────┐                │
│         │ LoadBalancer │                │
│         │   Service     │                │
│         └──────────────┘                │
└─────────────────────────────────────────┘
```

## Step-by-Step Deployment

### Step 1: Prepare Environment

```bash
# Ensure kind cluster exists
kind get clusters

# If not, create cluster
kind create cluster --name local-k8s-1
```

### Step 2: Build Docker Image

```bash
# Build image
docker build -t heart-disease-api:latest .

# Save as tar (for kind)
docker save heart-disease-api:latest -o heart-disease-api.tar

# Load into kind
sudo kind load image-archive heart-disease-api.tar --name local-k8s-1
```

**Or use automated script:**
```bash
./scripts/build_and_load_k8s.sh
```

### Step 3: Deploy API

```bash
# Apply deployment
kubectl apply -f k8s/deployment.yaml

# Wait for pods
kubectl wait --for=condition=ready pod -l app=heart-disease-api --timeout=300s

# Check status
kubectl get pods -l app=heart-disease-api
```

### Step 4: Copy Models to Pods

```bash
# Copy models to all API pods
./scripts/copy_models_to_k8s.sh
```

**Manual method:**
```bash
# Get pod name
POD_NAME=$(kubectl get pods -l app=heart-disease-api -o jsonpath='{.items[0].metadata.name}')

# Copy models
kubectl exec $POD_NAME -- mkdir -p /app/models
kubectl cp models/best_model.pkl $POD_NAME:/app/models/best_model.pkl
kubectl cp models/preprocessor.pkl $POD_NAME:/app/models/preprocessor.pkl

# Restart pod
kubectl delete pod $POD_NAME
```

### Step 5: Verify Deployment

```bash
# Check pods
kubectl get pods -l app=heart-disease-api

# Check services
kubectl get svc heart-disease-api-service

# Check logs
kubectl logs -l app=heart-disease-api --tail=20
```

### Step 6: Access API

```bash
# Port forward
kubectl port-forward service/heart-disease-api-service 8000:80

# Test health endpoint
curl http://localhost:8000/health

# Test prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
    "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
    "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
  }'
```

## Deploy Monitoring Stack

### Step 1: Deploy Prometheus

```bash
# Apply Prometheus RBAC (required for pod discovery)
kubectl apply -f k8s/prometheus-rbac.yaml

# Apply monitoring stack
kubectl apply -f k8s/monitoring.yaml

# Wait for Prometheus
kubectl wait --for=condition=ready pod -l app=prometheus --timeout=120s
```

### Step 2: Deploy Grafana

```bash
# Grafana is included in monitoring.yaml
# Wait for Grafana
kubectl wait --for=condition=ready pod -l app=grafana --timeout=120s

# Verify
kubectl get pods -l app=grafana
```

### Step 3: Access Monitoring

```bash
# Prometheus
kubectl port-forward service/prometheus-service 9090:9090
# Open: http://localhost:9090

# Grafana
kubectl port-forward service/grafana-service 3000:3000
# Open: http://localhost:3000
# Login: admin/admin
```

## Deploy MLflow UI

### Step 1: Deploy MLflow UI

```bash
# Apply MLflow UI
kubectl apply -f k8s/mlflow-ui.yaml

# Wait for pod
kubectl wait --for=condition=ready pod -l app=mlflow-ui --timeout=120s
```

### Step 2: Copy MLflow Data

```bash
# Copy mlruns to pod
./scripts/copy_mlflow_to_k8s.sh
```

### Step 3: Access MLflow UI

```bash
# Port forward
kubectl port-forward service/mlflow-ui-service 5000:5000

# Open: http://localhost:5000
```

## Complete Deployment Script

Use the automated deployment script:

```bash
./scripts/deploy_k8s.sh
```

This script:
1. Checks/creates kind cluster
2. Builds and loads Docker image
3. Deploys API
4. Deploys monitoring stack
5. Deploys MLflow UI
6. Copies models and MLflow data

## Deployment Verification Checklist

- [ ] API pods running (2 replicas)
- [ ] API health check passing
- [ ] Models copied to pods
- [ ] API predictions working
- [ ] Prometheus scraping API metrics
- [ ] Grafana connected to Prometheus
- [ ] MLflow UI accessible
- [ ] All services accessible via port-forward

## Scaling

### Scale API Pods

```bash
# Scale to 5 replicas
kubectl scale deployment heart-disease-api --replicas=5

# Check scaling
kubectl get pods -l app=heart-disease-api
```

### Resource Limits

Current limits (in `k8s/deployment.yaml`):
- **CPU:** 250m request, 500m limit
- **Memory:** 256Mi request, 512Mi limit

Adjust as needed for your environment.

## Troubleshooting

### Pods Not Starting

```bash
# Check pod status
kubectl get pods -l app=heart-disease-api

# Check logs
kubectl logs -l app=heart-disease-api

# Describe pod for events
kubectl describe pod <pod-name>
```

### Models Not Loading

```bash
# Verify models exist locally
ls -lh models/

# Copy models again
./scripts/copy_models_to_k8s.sh

# Check pod filesystem
kubectl exec <pod-name> -- ls -la /app/models/
```

### Prometheus Not Scraping

```bash
# Check Prometheus targets
kubectl port-forward service/prometheus-service 9090:9090
# Open: http://localhost:9090/targets

# Check Prometheus logs
kubectl logs -l app=prometheus --tail=50

# Verify RBAC
kubectl get serviceaccount prometheus
kubectl get clusterrolebinding prometheus
```

### Service Not Accessible

```bash
# Check service
kubectl get svc heart-disease-api-service

# Check endpoints
kubectl get endpoints heart-disease-api-service

# Test from inside cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- wget -O- http://heart-disease-api-service/predict
```

## Rollback

### Rollback Deployment

```bash
# View deployment history
kubectl rollout history deployment/heart-disease-api

# Rollback to previous version
kubectl rollout undo deployment/heart-disease-api

# Rollback to specific revision
kubectl rollout undo deployment/heart-disease-api --to-revision=2
```

## Cleanup

### Remove All Deployments

```bash
# Delete deployments
kubectl delete -f k8s/deployment.yaml
kubectl delete -f k8s/monitoring.yaml
kubectl delete -f k8s/mlflow-ui.yaml
kubectl delete -f k8s/prometheus-rbac.yaml

# Delete kind cluster (optional)
kind delete cluster --name local-k8s-1
```

## Production Considerations

### For Production Deployment

1. **Use Production Kubernetes:**
   - GKE, EKS, AKS, or managed Kubernetes
   - Not kind (development only)

2. **Security:**
   - Use secrets for sensitive data
   - Enable network policies
   - Use TLS/HTTPS

3. **High Availability:**
   - Multiple replicas
   - Multi-zone deployment
   - Load balancer configuration

4. **Monitoring:**
   - Set up alerting
   - Configure log aggregation
   - Use production-grade monitoring

5. **Backup:**
   - Backup models
   - Backup MLflow data
   - Backup configurations

## Summary

✅ **Complete deployment guide** - Step-by-step instructions
✅ **Automated scripts** - Easy deployment
✅ **Monitoring included** - Prometheus + Grafana
✅ **Troubleshooting guide** - Common issues covered
✅ **Production ready** - Can be adapted for production

**Deployment Time:** ~10-15 minutes for complete setup

