# EDA and Modeling Choices

## Dataset Overview

**Dataset:** Heart Disease UCI Dataset
**Source:** UCI Machine Learning Repository
**URL:** https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/

### Dataset Characteristics

- **Total Features:** 13 features + 1 target variable
- **Total Samples:** 303 (after cleaning)
- **Target Variable:** Binary (0 = No Disease, 1 = Disease)
- **Missing Values:** Handled using median imputation

### Feature Description

1. **age** - Age in years
2. **sex** - Sex (0 = female, 1 = male)
3. **cp** - Chest pain type (0-3)
4. **trestbps** - Resting blood pressure (mm Hg)
5. **chol** - Serum cholesterol (mg/dl)
6. **fbs** - Fasting blood sugar > 120 mg/dl (0/1)
7. **restecg** - Resting electrocardiographic results (0-2)
8. **thalach** - Maximum heart rate achieved
9. **exang** - Exercise induced angina (0/1)
10. **oldpeak** - ST depression induced by exercise
11. **slope** - Slope of peak exercise ST segment (0-2)
12. **ca** - Number of major vessels colored by flourosopy (0-4)
13. **thal** - Thalassemia (0-3)
14. **target** - Heart disease (0 = absent, 1-4 = present, converted to binary)

## Exploratory Data Analysis (EDA)

### Key Findings

#### 1. Class Distribution
- **No Disease (0):** ~54% of samples
- **Disease (1):** ~46% of samples
- **Conclusion:** Relatively balanced dataset, no significant class imbalance

#### 2. Feature Distributions

**Age:**
- Range: 29-77 years
- Mean: ~54 years
- Distribution: Approximately normal

**Cholesterol:**
- Range: 126-564 mg/dl
- Mean: ~246 mg/dl
- Some outliers present

**Resting Blood Pressure:**
- Range: 94-200 mm Hg
- Mean: ~131 mm Hg

**Maximum Heart Rate:**
- Range: 71-202 bpm
- Mean: ~149 bpm

#### 3. Correlation Analysis

**Key Correlations with Target:**
- **thalach** (max heart rate): Negative correlation - higher heart rate associated with lower disease risk
- **oldpeak** (ST depression): Positive correlation - higher values indicate disease
- **exang** (exercise angina): Positive correlation - presence indicates disease
- **cp** (chest pain): Positive correlation - certain pain types indicate disease

**Feature Correlations:**
- Age and maximum heart rate: Negative correlation (expected)
- Cholesterol and age: Weak positive correlation

#### 4. Missing Values

- Original dataset had '?' as missing values
- Handled using median imputation (SimpleImputer)
- Affected features: `ca` and `thal`

### EDA Visualizations Generated

1. **Class Distribution Chart** - Shows balanced dataset
2. **Feature Histograms** - Distribution of all numeric features
3. **Correlation Heatmap** - Feature correlations
4. **Feature Distributions by Class** - How features differ between disease/no disease
5. **Box Plots by Class** - Outlier detection and class differences

**Location:** `data/eda/` directory

## Feature Engineering

### Preprocessing Pipeline

1. **Missing Value Handling:**
   - Strategy: Median imputation
   - Reason: Robust to outliers, preserves distribution

2. **Feature Scaling:**
   - Method: StandardScaler (Z-score normalization)
   - Reason: Different feature scales (age vs cholesterol)
   - Formula: `(x - mean) / std`

3. **Target Encoding:**
   - Original: 0 (no disease), 1-4 (disease severity)
   - Converted to: 0 (no disease), 1 (disease)
   - Reason: Binary classification problem

### Feature Selection

- **All 13 features retained** - No feature elimination performed
- **Reason:** All features are clinically relevant for heart disease prediction
- **Future work:** Could explore feature importance and selection

## Model Development

### Models Trained

#### 1. Logistic Regression

**Configuration:**
- Solver: `liblinear`
- Max iterations: 1000
- Random state: 42

**Rationale:**
- Interpretable model
- Good baseline for binary classification
- Fast training time
- Provides probability estimates

**Performance:**
- Test Accuracy: ~85-90%
- ROC-AUC: ~0.88-0.92
- Cross-validation: 5-fold stratified

#### 2. Random Forest

**Configuration:**
- N estimators: 100
- Max depth: 10
- Random state: 42
- N jobs: -1 (parallel)

**Rationale:**
- Handles non-linear relationships
- Feature importance insights
- Robust to outliers
- Good generalization

**Performance:**
- Test Accuracy: ~88-92%
- ROC-AUC: ~0.90-0.94
- Cross-validation: 5-fold stratified

### Model Selection

**Selection Criteria:**
- Primary: ROC-AUC score (best for imbalanced/medical data)
- Secondary: Cross-validation consistency
- Tertiary: Test accuracy

**Best Model:** Random Forest (typically higher ROC-AUC)

**Reason:**
- Better handling of feature interactions
- More robust predictions
- Higher generalization performance

### Evaluation Metrics

1. **Accuracy:** Overall correctness
2. **Precision:** True positives / (True positives + False positives)
3. **Recall:** True positives / (True positives + False negatives)
4. **ROC-AUC:** Area under ROC curve (primary metric)
5. **Cross-Validation:** 5-fold stratified CV for robustness

### Hyperparameter Tuning

**Approach:** Default parameters with reasonable constraints
- **Future work:** Grid search or Bayesian optimization
- **Current:** Focus on reproducibility and baseline performance

### Model Persistence

- **Format:** Pickle (.pkl)
- **Saved Components:**
  - Trained model
  - Preprocessing pipeline (scaler + imputer)
- **Location:** `models/` directory

## Modeling Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Missing Values | Median Imputation | Robust to outliers |
| Scaling | StandardScaler | Normalize feature scales |
| Models | LR + RF | Baseline + Ensemble |
| Evaluation | ROC-AUC | Best for medical classification |
| CV | 5-fold Stratified | Robust evaluation |
| Best Model | Random Forest | Higher performance |

## Reproducibility

All modeling choices are:
- ✅ Documented in code
- ✅ Saved in MLflow experiments
- ✅ Version controlled
- ✅ Reproducible with fixed random seeds

## References

- UCI Heart Disease Dataset: https://archive.ics.uci.edu/ml/datasets/heart+disease
- Scikit-learn Documentation: https://scikit-learn.org/
- MLflow Documentation: https://mlflow.org/

