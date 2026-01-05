# Screenshots Directory

This folder should contain screenshots for the assignment documentation.

## Required Screenshots

### 1. EDA Visualizations
- `class_distribution.png` - Class balance chart
- `correlation_heatmap.png` - Feature correlations
- `feature_histograms.png` - Feature distributions
- `feature_distributions_by_class.png` - Features by target class
- `boxplots_by_class.png` - Box plots

**Location:** These are auto-generated in `data/eda/` - copy here for documentation

### 2. MLflow Experiments
- `mlflow_experiments_list.png` - Experiments overview
- `mlflow_run_details.png` - Individual run with metrics
- `mlflow_compare_runs.png` - Side-by-side model comparison
- `mlflow_artifacts.png` - Model artifacts view

**How to capture:**
1. Start MLflow UI: `mlflow ui` or `./scripts/start_mlflow_ui.sh`
2. Open: http://localhost:5000
3. Take screenshots of experiments, runs, and comparisons

### 3. CI/CD Pipeline
- `github_actions_pipeline.png` - Pipeline execution view
- `github_actions_lint.png` - Linting job results
- `github_actions_test.png` - Test results with coverage
- `github_actions_build.png` - Docker build results

**How to capture:**
1. Go to GitHub Actions tab
2. Open a workflow run
3. Screenshot each job

### 4. Docker Deployment
- `docker_build.png` - Docker build output
- `docker_run_test.png` - Container running and tested
- `docker_image_list.png` - Docker images

**How to capture:**
```bash
docker images | grep heart-disease-api
docker ps | grep heart-disease-api
```

### 5. Kubernetes Deployment
- `k8s_pods.png` - All pods running
- `k8s_services.png` - Services exposed
- `k8s_deployment_status.png` - Deployment status
- `k8s_api_logs.png` - API pod logs

**How to capture:**
```bash
kubectl get pods
kubectl get svc
kubectl get deployment
kubectl logs -l app=heart-disease-api
```

### 6. Prometheus Monitoring
- `prometheus_targets.png` - Targets showing UP
- `prometheus_query_results.png` - Query results (api_requests_total)
- `prometheus_graph.png` - Metric graphs

**How to capture:**
1. Port forward: `kubectl port-forward service/prometheus-service 9090:9090`
2. Open: http://localhost:9090
3. Go to Targets and Graph pages

### 7. Grafana Dashboards
- `grafana_datasource.png` - Prometheus data source configured
- `grafana_dashboard.png` - Custom dashboard with metrics
- `grafana_queries.png` - Query editor with results

**How to capture:**
1. Port forward: `kubectl port-forward service/grafana-service 3000:3000`
2. Open: http://localhost:3000
3. Login: admin/admin
4. Screenshot data source and dashboards

### 8. API Testing
- `api_health_check.png` - Health endpoint response
- `api_predict_request.png` - Prediction request/response
- `api_metrics_endpoint.png` - Metrics endpoint output
- `api_docs.png` - Swagger UI documentation

**How to capture:**
```bash
# Health
curl http://localhost:8000/health

# Predict
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{...}'

# Metrics
curl http://localhost:8000/metrics

# Docs
# Open: http://localhost:8000/docs
```

## Screenshot Guidelines

1. **Clear and readable** - Use high resolution
2. **Include context** - Show relevant information
3. **Label if needed** - Add annotations for clarity
4. **Organize by category** - Use subfolders if needed
5. **Name descriptively** - Clear file names

## Suggested Folder Structure

```
screenshots/
├── eda/              # EDA visualizations
├── mlflow/           # MLflow screenshots
├── cicd/             # CI/CD pipeline
├── docker/           # Docker deployment
├── kubernetes/       # K8s deployment
├── prometheus/       # Prometheus monitoring
├── grafana/          # Grafana dashboards
└── api/              # API testing
```

## Quick Capture Script

Create a script to help capture screenshots:

```bash
# Example: Capture current state
kubectl get pods > screenshots/k8s_pods.txt
kubectl get svc > screenshots/k8s_services.txt
```

## Notes

- Screenshots are optional but recommended for assignment
- Focus on key components and workflows
- Ensure screenshots demonstrate working system
- Include timestamps if relevant

