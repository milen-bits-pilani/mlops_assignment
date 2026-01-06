"""
Data acquisition script for Heart Disease UCI Dataset
Downloads the dataset from UCI Machine Learning Repository
"""

import os
import urllib.request
import pandas as pd
from pathlib import Path


def download_heart_disease_data(output_dir: str = "data/raw") -> str:
    """
    Download Heart Disease UCI dataset from UCI ML Repository

    Args:
        output_dir: Directory to save the dataset

    Returns:
        Path to the downloaded CSV file
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # UCI Heart Disease dataset URL
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"

    output_path = os.path.join(output_dir, "heart_disease.csv")

    print(f"Downloading Heart Disease dataset from UCI...")
    print(f"URL: {url}")

    try:
        urllib.request.urlretrieve(url, output_path)
        print(f"Dataset downloaded successfully to {output_path}")

        # The UCI dataset doesn't have headers, so we need to add them
        # Based on the dataset documentation, these are the column names
        column_names = [
            "age",
            "sex",
            "cp",
            "trestbps",
            "chol",
            "fbs",
            "restecg",
            "thalach",
            "exang",
            "oldpeak",
            "slope",
            "ca",
            "thal",
            "target",
        ]

        # Read the data and add column names
        df = pd.read_csv(output_path, header=None, names=column_names, na_values="?")

        # Save with proper headers
        df.to_csv(output_path, index=False)
        print(f"Dataset saved with headers to {output_path}")
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")

        return output_path

    except Exception as e:
        print(f"Error downloading dataset: {e}")
        raise


if __name__ == "__main__":
    download_heart_disease_data()
