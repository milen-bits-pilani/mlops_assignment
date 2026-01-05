# Jupyter Notebooks

This folder contains Jupyter notebooks for EDA, Training, and Inference as required by the assignment deliverables.

## Notebooks

### 1. `01_EDA.ipynb` - Exploratory Data Analysis
- Loads and explores the Heart Disease dataset
- Performs comprehensive data analysis
- Generates visualizations:
  - Class distribution
  - Feature histograms
  - Correlation heatmap
  - Feature distributions by target class
  - Box plots

**Usage:**
```bash
jupyter notebook notebooks/01_EDA.ipynb
```

### 2. `02_Training.ipynb` - Model Training
- Loads and preprocesses data
- Trains Logistic Regression and Random Forest models
- Integrates with MLflow for experiment tracking
- Evaluates models with cross-validation
- Selects and saves the best model

**Usage:**
```bash
jupyter notebook notebooks/02_Training.ipynb
```

### 3. `03_Inference.ipynb` - Model Inference
- Loads trained model and preprocessor
- Demonstrates single prediction
- Shows batch prediction examples
- Tests on test set

**Usage:**
```bash
jupyter notebook notebooks/03_Inference.ipynb
```

## Running Notebooks

### Option 1: Jupyter Notebook
```bash
# Start Jupyter
jupyter notebook

# Navigate to notebooks/ folder and open desired notebook
```

### Option 2: JupyterLab
```bash
# Start JupyterLab
jupyter lab

# Navigate to notebooks/ folder and open desired notebook
```

### Option 3: VS Code
- Open `.ipynb` files directly in VS Code
- Install Jupyter extension if needed

## Prerequisites

1. Install Jupyter:
```bash
pip install jupyter ipykernel
```

2. Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

3. Make sure data is available:
```bash
# Run data download first
python src/data/download_data.py
```

## Notes

- All notebooks use relative paths from the `notebooks/` directory
- Notebooks can be run independently or in sequence
- Visualizations are saved to `../data/eda/` directory
- Models are saved to `../models/` directory
- MLflow experiments are saved to `../mlruns/` directory

## Alternative: Python Scripts

The project also includes equivalent Python scripts:
- `src/eda/explore.py` - EDA script
- `src/models/train.py` - Training script
- `src/api/app.py` - Inference API

Both notebooks and scripts are provided to meet assignment requirements.

