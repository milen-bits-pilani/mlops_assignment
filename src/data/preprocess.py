"""
Data preprocessing and cleaning module
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from typing import Tuple
import pickle
from pathlib import Path


class HeartDiseasePreprocessor:
    """Preprocessing pipeline for Heart Disease dataset"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.imputer = SimpleImputer(strategy='median')
        self.is_fitted = False
        
    def fit(self, X: pd.DataFrame):
        """Fit the preprocessor on training data"""
        # Handle missing values
        X_imputed = pd.DataFrame(
            self.imputer.fit_transform(X),
            columns=X.columns,
            index=X.index
        )
        
        # Fit scaler
        self.scaler.fit(X_imputed)
        self.is_fitted = True
        
        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Transform data using fitted preprocessor"""
        if not self.is_fitted:
            raise ValueError("Preprocessor must be fitted before transform")
        
        # Handle missing values
        X_imputed = pd.DataFrame(
            self.imputer.transform(X),
            columns=X.columns,
            index=X.index
        )
        
        # Scale features
        X_scaled = pd.DataFrame(
            self.scaler.transform(X_imputed),
            columns=X.columns,
            index=X.index
        )
        
        return X_scaled
    
    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Fit and transform in one step"""
        return self.fit(X).transform(X)
    
    def save(self, filepath: str):
        """Save preprocessor to disk"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'wb') as f:
            pickle.dump({
                'scaler': self.scaler,
                'imputer': self.imputer,
                'is_fitted': self.is_fitted
            }, f)
    
    @classmethod
    def load(cls, filepath: str):
        """Load preprocessor from disk"""
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        preprocessor = cls()
        preprocessor.scaler = data['scaler']
        preprocessor.imputer = data['imputer']
        preprocessor.is_fitted = data['is_fitted']
        
        return preprocessor


def load_and_clean_data(data_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Load and clean the Heart Disease dataset
    
    Args:
        data_path: Path to the CSV file
        
    Returns:
        Tuple of (X, y) where X is features and y is target
    """
    # Load data
    df = pd.read_csv(data_path)
    
    print(f"Original dataset shape: {df.shape}")
    print(f"Missing values:\n{df.isnull().sum()}")
    
    # Convert target to binary (0 = no disease, 1 = disease)
    # Original target: 0 = no disease, 1-4 = disease
    df['target'] = (df['target'] > 0).astype(int)
    
    # Separate features and target
    feature_columns = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]
    
    X = df[feature_columns].copy()
    y = df['target'].copy()
    
    # Handle missing values (replace '?' with NaN)
    X = X.replace('?', np.nan)
    
    # Convert to numeric
    for col in X.columns:
        X[col] = pd.to_numeric(X[col], errors='coerce')
    
    print(f"After cleaning - Features shape: {X.shape}, Target shape: {y.shape}")
    print(f"Class distribution:\n{y.value_counts()}")
    
    return X, y

