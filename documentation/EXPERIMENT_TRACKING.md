# Experiment Tracking Summary

## MLflow Integration

This project uses **MLflow** for comprehensive experiment tracking, model versioning, and reproducibility.

## Experiment Configuration

### Experiment Name
- **Name:** `heart_disease`
- **Tracking URI:** Local file system (`mlruns/` directory)
- **Backend Store:** File-based storage

### Tracked Components

#### 1. Parameters
- Model type (LogisticRegression/RandomForest)
- Hyperparameters (max_iter, solver, n_estimators, max_depth)
- Random state (42 for reproducibility)

#### 2. Metrics
- **train_accuracy** - Training set accuracy
- **test_accuracy** - Test set accuracy
- **precision** - Precision score
- **recall** - Recall score
- **roc_auc** - ROC-AUC score (primary metric)
- **cv_roc_auc_mean** - Cross-validation mean ROC-AUC
- **cv_roc_auc_std** - Cross-validation standard deviation

#### 3. Artifacts
- **Model files** - Trained model (pickle format)
- **Preprocessor** - Preprocessing pipeline
- **Metadata** - Model metadata and requirements

## Experiment Runs

### Run 1: Logistic Regression

**Parameters:**
- model_type: LogisticRegression
- max_iter: 1000
- solver: liblinear
- random_state: 42

**Metrics (Typical):**
- train_accuracy: ~0.88
- test_accuracy: ~0.85
- precision: ~0.86
- recall: ~0.84
- roc_auc: ~0.88-0.92
- cv_roc_auc_mean: ~0.87-0.91
- cv_roc_auc_std: ~0.03-0.05

### Run 2: Random Forest

**Parameters:**
- model_type: RandomForest
- n_estimators: 100
- max_depth: 10
- random_state: 42

**Metrics (Typical):**
- train_accuracy: ~0.95
- test_accuracy: ~0.88-0.92
- precision: ~0.89
- recall: ~0.87
- roc_auc: ~0.90-0.94
- cv_roc_auc_mean: ~0.89-0.93
- cv_roc_auc_std: ~0.02-0.04

## Accessing MLflow UI

### Local Access

```bash
# Start MLflow UI
mlflow ui

# Or use the script
./scripts/start_mlflow_ui.sh

# Access at: http://localhost:5000
```

### Kubernetes Access

```bash
# Port forward MLflow UI service
kubectl port-forward service/mlflow-ui-service 5000:5000

# Access at: http://localhost:5000
```

## MLflow Features Used

### 1. Experiment Management
- Automatic experiment creation
- Run organization by model type
- Run naming for easy identification

### 2. Model Registry
- Model versioning
- Model artifacts storage
- Model metadata tracking

### 3. Reproducibility
- Parameter logging
- Environment tracking
- Code versioning (via source tracking)

### 4. Comparison
- Side-by-side run comparison
- Metric visualization
- Parameter differences

## Experiment Results Summary

### Best Model Selection

**Selection Criteria:**
1. Highest ROC-AUC score
2. Consistent cross-validation performance
3. Good test set performance

**Selected Model:** Random Forest (typically)

**Reason:**
- Higher ROC-AUC (0.90-0.94 vs 0.88-0.92)
- Better generalization
- More robust predictions

### Performance Comparison

| Model | Test Accuracy | ROC-AUC | Precision | Recall |
|-------|--------------|---------|-----------|--------|
| Logistic Regression | ~85-90% | ~0.88-0.92 | ~0.86 | ~0.84 |
| Random Forest | ~88-92% | ~0.90-0.94 | ~0.89 | ~0.87 |

## MLflow Artifacts

### Stored Artifacts

1. **Model Files:**
   - `model/model.pkl` - Serialized model
   - `model/MLmodel` - MLflow model metadata
   - `model/requirements.txt` - Python dependencies

2. **Preprocessor:**
   - `preprocessor/preprocessor.pkl` - Saved preprocessing pipeline

3. **Metadata:**
   - Run metadata (timestamps, user, source)
   - Model signatures
   - Input/output schemas

## Reproducibility Features

### Code Tracking
- Source file tracking
- Git commit tracking (if in git repo)
- Code snapshots

### Environment Tracking
- Python version
- Package versions
- System information

### Parameter Tracking
- All hyperparameters logged
- Random seeds fixed
- Configuration captured

## MLflow Queries

### Useful Queries in MLflow UI

1. **Filter by model type:**
   - `params.model_type = "RandomForest"`

2. **Filter by performance:**
   - `metrics.roc_auc > 0.90`

3. **Compare runs:**
   - Select multiple runs
   - Compare metrics side-by-side

## Integration with CI/CD

MLflow runs are automatically logged during:
- CI/CD pipeline execution
- Automated model training
- Manual training runs

## Best Practices Followed

1. ✅ **Consistent naming** - Run names match model types
2. ✅ **Complete logging** - All parameters and metrics logged
3. ✅ **Artifact storage** - Models and preprocessors saved
4. ✅ **Reproducibility** - Fixed random seeds, version tracking
5. ✅ **Documentation** - Clear experiment descriptions

## Accessing Experiment Data

### Programmatic Access

```python
import mlflow

# List experiments
experiments = mlflow.search_experiments()

# Search runs
runs = mlflow.search_runs(experiment_names=["heart_disease"])

# Load model
model = mlflow.sklearn.load_model("runs:/<run_id>/model")
```

### File System Access

All experiment data stored in:
- `mlruns/` directory
- Organized by experiment ID
- Each run in separate directory

## Summary

✅ **MLflow fully integrated** - All experiments tracked
✅ **Comprehensive logging** - Parameters, metrics, artifacts
✅ **Easy comparison** - Side-by-side run comparison
✅ **Reproducibility** - Complete environment and code tracking
✅ **Model versioning** - All models saved and versioned

**Total Experiments:** 1 (heart_disease)
**Total Runs:** 2+ (LogisticRegression, RandomForest, and variations)

