# Quick Reference Guide

## For Evaluators - Quick Start

### Reproduce the Project (30 minutes)

```bash
# 1. Setup (5 min)
cd mlops_project
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
./scripts/init_project.sh

# 2. Run Pipeline (10 min)
./scripts/run_pipeline.sh

# 3. Deploy (10 min)
./scripts/build_and_load_k8s.sh
./scripts/deploy_k8s.sh
./scripts/copy_models_to_k8s.sh
./scripts/copy_mlflow_to_k8s.sh

# 4. Verify (5 min)
kubectl get pods
kubectl port-forward service/heart-disease-api-service 8000:80
curl http://localhost:8000/health
```

## Documentation Map

| Need | Document |
|------|----------|
| **Setup from scratch** | [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) |
| **Reproduce everything** | [REPRODUCIBILITY_GUIDE.md](REPRODUCIBILITY_GUIDE.md) |
| **Understand EDA** | [EDA_AND_MODELING.md](EDA_AND_MODELING.md) |
| **Check MLflow** | [EXPERIMENT_TRACKING.md](EXPERIMENT_TRACKING.md) |
| **See architecture** | [ARCHITECTURE.md](ARCHITECTURE.md) |
| **CI/CD details** | [CI_CD_WORKFLOW.md](CI_CD_WORKFLOW.md) |
| **Deploy to K8s** | [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) |
| **Complete report** | [COMPLETE_REPORT.md](COMPLETE_REPORT.md) |

## Key Files Location

```
mlops_project/
├── src/                    # Source code
├── tests/                  # Unit tests
├── k8s/                    # Kubernetes manifests
├── scripts/                # Automation scripts
├── documentation/          # 📚 All documentation here
│   ├── README.md          # Start here
│   ├── INDEX.md           # Documentation index
│   └── ...                # All other docs
└── requirements.txt        # Dependencies
```

## Verification Commands

```bash
# Check setup
python verify_setup.py

# Check API
curl http://localhost:8000/health
curl http://localhost:8000/metrics

# Check Kubernetes
kubectl get pods
kubectl get svc

# Check Prometheus
kubectl port-forward service/prometheus-service 9090:9090
# Open: http://localhost:9090/targets

# Check Grafana
kubectl port-forward service/grafana-service 3000:3000
# Open: http://localhost:3000 (admin/admin)
```

## Task Coverage

✅ Task 1: Data Acquisition & EDA
✅ Task 2: Feature Engineering & Model Development  
✅ Task 3: Experiment Tracking
✅ Task 4: Model Packaging & Reproducibility
✅ Task 5: CI/CD Pipeline & Automated Testing
✅ Task 6: Model Containerization
✅ Task 7: Production Deployment
✅ Task 8: Monitoring & Logging
✅ Task 9: Documentation & Reporting

## Contact

All documentation is self-contained. For questions, refer to:
- [REPRODUCIBILITY_GUIDE.md](REPRODUCIBILITY_GUIDE.md) for step-by-step
- [COMPLETE_REPORT.md](COMPLETE_REPORT.md) for executive summary

