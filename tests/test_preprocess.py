"""
Unit tests for data preprocessing
"""
import pytest
import pandas as pd
import numpy as np
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from src.data.preprocess import HeartDiseasePreprocessor, load_and_clean_data


def test_preprocessor_fit_transform():
    """Test preprocessor fit and transform"""
    preprocessor = HeartDiseasePreprocessor()
    
    # Create sample data
    X = pd.DataFrame({
        'age': [63, 67, 67],
        'sex': [1, 1, 1],
        'cp': [3, 0, 0],
        'trestbps': [145, 160, 120],
        'chol': [233, 286, 229],
        'fbs': [1, 0, 0],
        'restecg': [0, 1, 1],
        'thalach': [150, 108, 129],
        'exang': [0, 1, 1],
        'oldpeak': [2.3, 1.5, 2.6],
        'slope': [0, 2, 2],
        'ca': [0, 3, 2],
        'thal': [1, 2, 4]
    })
    
    # Fit and transform
    X_transformed = preprocessor.fit_transform(X)
    
    # Check that output is DataFrame
    assert isinstance(X_transformed, pd.DataFrame)
    
    # Check that shape is preserved
    assert X_transformed.shape == X.shape
    
    # Check that columns are preserved
    assert list(X_transformed.columns) == list(X.columns)


def test_preprocessor_handles_missing_values():
    """Test preprocessor handles missing values"""
    preprocessor = HeartDiseasePreprocessor()
    
    # Create data with missing values
    X = pd.DataFrame({
        'age': [63, np.nan, 67],
        'sex': [1, 1, 1],
        'cp': [3, 0, 0],
        'trestbps': [145, 160, np.nan],
        'chol': [233, 286, 229],
        'fbs': [1, 0, 0],
        'restecg': [0, 1, 1],
        'thalach': [150, 108, 129],
        'exang': [0, 1, 1],
        'oldpeak': [2.3, 1.5, 2.6],
        'slope': [0, 2, 2],
        'ca': [0, 3, 2],
        'thal': [1, 2, 4]
    })
    
    # Should not raise error
    X_transformed = preprocessor.fit_transform(X)
    
    # Check no NaN values in output
    assert not X_transformed.isnull().any().any()


def test_preprocessor_save_load():
    """Test preprocessor save and load"""
    preprocessor = HeartDiseasePreprocessor()
    
    X = pd.DataFrame({
        'age': [63, 67, 67],
        'sex': [1, 1, 1],
        'cp': [3, 0, 0],
        'trestbps': [145, 160, 120],
        'chol': [233, 286, 229],
        'fbs': [1, 0, 0],
        'restecg': [0, 1, 1],
        'thalach': [150, 108, 129],
        'exang': [0, 1, 1],
        'oldpeak': [2.3, 1.5, 2.6],
        'slope': [0, 2, 2],
        'ca': [0, 3, 2],
        'thal': [1, 2, 4]
    })
    
    # Fit preprocessor
    preprocessor.fit(X)
    
    # Save
    preprocessor.save("test_preprocessor.pkl")
    
    # Load
    loaded_preprocessor = HeartDiseasePreprocessor.load("test_preprocessor.pkl")
    
    # Check that loaded preprocessor is fitted
    assert loaded_preprocessor.is_fitted
    
    # Check that transformations are similar
    X_transformed_original = preprocessor.transform(X)
    X_transformed_loaded = loaded_preprocessor.transform(X)
    
    pd.testing.assert_frame_equal(X_transformed_original, X_transformed_loaded)
    
    # Cleanup
    import os
    if os.path.exists("test_preprocessor.pkl"):
        os.remove("test_preprocessor.pkl")


def test_load_and_clean_data():
    """Test data loading and cleaning"""
    # This test requires the dataset to be downloaded first
    # We'll create a mock dataset for testing
    import tempfile
    
    # Create temporary CSV file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target\n")
        f.write("63,1,3,145,233,1,0,150,0,2.3,0,0,1,1\n")
        f.write("67,1,0,160,286,0,1,108,1,1.5,2,3,2,2\n")
        f.write("67,1,0,120,229,0,1,129,1,2.6,2,2,4,3\n")
        temp_path = f.name
    
    try:
        X, y = load_and_clean_data(temp_path)
        
        # Check that X and y are returned
        assert X is not None
        assert y is not None
        
        # Check shapes
        assert len(X) == len(y)
        assert len(X) == 3
        
        # Check that target is binary
        assert set(y.unique()).issubset({0, 1})
        
    finally:
        # Cleanup
        import os
        if os.path.exists(temp_path):
            os.remove(temp_path)

