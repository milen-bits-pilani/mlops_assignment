"""
Unit tests for model training and evaluation
"""

import pytest
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from src.data.preprocess import HeartDiseasePreprocessor


def create_sample_data():
    """Create sample data for testing"""
    np.random.seed(42)
    n_samples = 100

    X = pd.DataFrame(
        {
            "age": np.random.randint(30, 80, n_samples),
            "sex": np.random.randint(0, 2, n_samples),
            "cp": np.random.randint(0, 4, n_samples),
            "trestbps": np.random.randint(90, 200, n_samples),
            "chol": np.random.randint(100, 400, n_samples),
            "fbs": np.random.randint(0, 2, n_samples),
            "restecg": np.random.randint(0, 3, n_samples),
            "thalach": np.random.randint(70, 200, n_samples),
            "exang": np.random.randint(0, 2, n_samples),
            "oldpeak": np.random.uniform(0, 6, n_samples),
            "slope": np.random.randint(0, 3, n_samples),
            "ca": np.random.randint(0, 4, n_samples),
            "thal": np.random.randint(0, 4, n_samples),
        }
    )

    # Create target with some correlation to features
    y = ((X["age"] > 60) | (X["chol"] > 250) | (X["trestbps"] > 140)).astype(int)
    y = pd.Series(y)

    return X, y


def test_logistic_regression_training():
    """Test Logistic Regression model training"""
    X, y = create_sample_data()

    # Preprocess
    preprocessor = HeartDiseasePreprocessor()
    X_processed = preprocessor.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=42
    )

    # Train model
    model = LogisticRegression(max_iter=1000, random_state=42, solver="liblinear")
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)

    # Check predictions
    assert len(predictions) == len(y_test)
    assert all(p in [0, 1] for p in predictions)
    assert probabilities.shape == (len(y_test), 2)
    assert all(0 <= p <= 1 for p in probabilities[:, 1])


def test_random_forest_training():
    """Test Random Forest model training"""
    X, y = create_sample_data()

    # Preprocess
    preprocessor = HeartDiseasePreprocessor()
    X_processed = preprocessor.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)

    # Check predictions
    assert len(predictions) == len(y_test)
    assert all(p in [0, 1] for p in predictions)
    assert probabilities.shape == (len(y_test), 2)
    assert all(0 <= p <= 1 for p in probabilities[:, 1])


def test_model_accuracy():
    """Test that models achieve reasonable accuracy"""
    X, y = create_sample_data()

    # Preprocess
    preprocessor = HeartDiseasePreprocessor()
    X_processed = preprocessor.fit_transform(X)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=42
    )

    # Train Logistic Regression
    lr_model = LogisticRegression(max_iter=1000, random_state=42, solver="liblinear")
    lr_model.fit(X_train, y_train)
    lr_accuracy = lr_model.score(X_test, y_test)

    # Train Random Forest
    rf_model = RandomForestClassifier(n_estimators=10, max_depth=5, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_accuracy = rf_model.score(X_test, y_test)

    # Check that accuracy is reasonable (at least better than random)
    assert lr_accuracy > 0.5
    assert rf_accuracy > 0.5
