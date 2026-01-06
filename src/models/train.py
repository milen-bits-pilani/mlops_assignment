"""
Model training script with MLflow integration
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
import mlflow
import mlflow.sklearn
from pathlib import Path
import pickle
import sys
import os

# Add project root to path
project_root = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from src.data.preprocess import HeartDiseasePreprocessor, load_and_clean_data


def train_models(
    data_path: str, output_dir: str = "models", mlflow_experiment: str = "heart_disease"
):
    """
    Train and evaluate multiple models with MLflow tracking

    Args:
        data_path: Path to the dataset
        output_dir: Directory to save models
        mlflow_experiment: MLflow experiment name
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Set MLflow tracking URI to local directory
    # Always use current working directory to ensure writable location
    # This works in both local and CI/CD environments
    cwd = os.getcwd()
    mlruns_dir = os.path.join(cwd, "mlruns")

    # Ensure directory exists and is writable BEFORE setting tracking URI
    # This prevents MLflow from trying to create parent directories
    try:
        Path(mlruns_dir).mkdir(parents=True, exist_ok=True)
        # Test write permissions
        test_file = os.path.join(mlruns_dir, ".test_write")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print(f"MLruns directory verified: {mlruns_dir}")
    except (OSError, PermissionError) as e:
        raise RuntimeError(
            f"Cannot create or write to mlruns directory at {mlruns_dir}: {e}"
        )

    # Use absolute path for MLflow tracking URI
    # Check environment variable first (for CI/CD), but ensure path is in workspace
    if "MLFLOW_TRACKING_URI" in os.environ:
        env_uri = os.environ["MLFLOW_TRACKING_URI"]
        # Extract path from URI
        if env_uri.startswith("file://"):
            env_path = env_uri[7:]
        else:
            env_path = env_uri
        # Use environment URI if it's within workspace, otherwise use workspace mlruns
        if os.path.commonpath([cwd, os.path.abspath(env_path)]) == cwd:
            tracking_uri = env_uri
            mlruns_dir = os.path.abspath(env_path)
        else:
            # Fall back to workspace mlruns
            mlflow_tracking_uri = os.path.abspath(os.path.normpath(mlruns_dir))
            tracking_uri = f"file://{mlflow_tracking_uri}"
    else:
        # Use workspace mlruns directory
        mlflow_tracking_uri = os.path.abspath(os.path.normpath(mlruns_dir))
        tracking_uri = f"file://{mlflow_tracking_uri}"

    # Set tracking URI AFTER ensuring directory exists
    mlflow.set_tracking_uri(tracking_uri)
    print(f"MLflow tracking URI set to: {tracking_uri}")

    # Verify tracking URI is set correctly
    actual_uri = mlflow.get_tracking_uri()
    print(f"Actual MLflow tracking URI: {actual_uri}")

    # Set MLflow experiment
    mlflow.set_experiment(mlflow_experiment)

    # Load and clean data
    print("Loading and cleaning data...")
    X, y = load_and_clean_data(data_path)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Train set: {X_train.shape}, Test set: {X_test.shape}")

    # Preprocess data
    print("Preprocessing data...")
    preprocessor = HeartDiseasePreprocessor()
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    # Save preprocessor
    preprocessor_path = os.path.join(output_dir, "preprocessor.pkl")
    preprocessor.save(preprocessor_path)
    print(f"Preprocessor saved to {preprocessor_path}")

    # Define models to train
    models = {
        "LogisticRegression": LogisticRegression(
            max_iter=1000, random_state=42, solver="liblinear"
        ),
        "RandomForest": RandomForestClassifier(
            n_estimators=100, max_depth=10, random_state=42, n_jobs=-1
        ),
    }

    # Cross-validation setup
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    results = {}

    # Train each model
    for model_name, model in models.items():
        print(f"\n{'='*80}")
        print(f"Training {model_name}")
        print(f"{'='*80}")

        with mlflow.start_run(run_name=model_name):
            # Train model
            model.fit(X_train_processed, y_train)

            # Predictions
            y_train_pred = model.predict(X_train_processed)
            y_test_pred = model.predict(X_test_processed)
            y_test_proba = model.predict_proba(X_test_processed)[:, 1]

            # Calculate metrics
            train_accuracy = accuracy_score(y_train, y_train_pred)
            test_accuracy = accuracy_score(y_test, y_test_pred)
            precision = precision_score(y_test, y_test_pred)
            recall = recall_score(y_test, y_test_pred)
            roc_auc = roc_auc_score(y_test, y_test_proba)

            # Cross-validation scores
            cv_scores = cross_val_score(
                model, X_train_processed, y_train, cv=cv, scoring="roc_auc", n_jobs=-1
            )
            cv_mean = cv_scores.mean()
            cv_std = cv_scores.std()

            # Log parameters
            if model_name == "LogisticRegression":
                mlflow.log_param("max_iter", 1000)
                mlflow.log_param("solver", "liblinear")
            elif model_name == "RandomForest":
                mlflow.log_param("n_estimators", 100)
                mlflow.log_param("max_depth", 10)

            mlflow.log_param("model_type", model_name)
            mlflow.log_param("random_state", 42)

            # Log metrics
            mlflow.log_metric("train_accuracy", train_accuracy)
            mlflow.log_metric("test_accuracy", test_accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("roc_auc", roc_auc)
            mlflow.log_metric("cv_roc_auc_mean", cv_mean)
            mlflow.log_metric("cv_roc_auc_std", cv_std)

            # Log model
            # Ensure we're using absolute paths for artifacts
            mlflow.sklearn.log_model(model, "model")

            # Log preprocessor - use absolute path
            abs_preprocessor_path = os.path.abspath(preprocessor_path)
            mlflow.log_artifact(abs_preprocessor_path, "preprocessor")

            # Print results
            print(f"\n{model_name} Results:")
            print(f"  Train Accuracy: {train_accuracy:.4f}")
            print(f"  Test Accuracy: {test_accuracy:.4f}")
            print(f"  Precision: {precision:.4f}")
            print(f"  Recall: {recall:.4f}")
            print(f"  ROC-AUC: {roc_auc:.4f}")
            print(f"  CV ROC-AUC: {cv_mean:.4f} (+/- {cv_std:.4f})")

            print(f"\n  Confusion Matrix:")
            print(confusion_matrix(y_test, y_test_pred))

            print(f"\n  Classification Report:")
            print(classification_report(y_test, y_test_pred))

            # Save model
            model_path = os.path.join(output_dir, f"{model_name.lower()}_model.pkl")
            with open(model_path, "wb") as f:
                pickle.dump(model, f)
            print(f"\n  Model saved to {model_path}")

            results[model_name] = {
                "model": model,
                "test_accuracy": test_accuracy,
                "roc_auc": roc_auc,
                "precision": precision,
                "recall": recall,
                "cv_mean": cv_mean,
            }

    # Select best model based on ROC-AUC
    best_model_name = max(results, key=lambda x: results[x]["roc_auc"])
    best_model = results[best_model_name]["model"]

    print(f"\n{'='*80}")
    print(f"Best Model: {best_model_name}")
    print(f"  ROC-AUC: {results[best_model_name]['roc_auc']:.4f}")
    print(f"{'='*80}")

    # Save best model
    best_model_path = os.path.join(output_dir, "best_model.pkl")
    with open(best_model_path, "wb") as f:
        pickle.dump(best_model, f)
    print(f"Best model saved to {best_model_path}")

    return best_model, preprocessor, results


if __name__ == "__main__":
    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/raw/heart_disease.csv"
    train_models(data_path)
