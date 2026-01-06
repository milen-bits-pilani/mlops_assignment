"""
FastAPI application for Heart Disease Prediction
"""
import os
import pickle
import logging
from pathlib import Path
from typing import List, Dict, Optional
import numpy as np
import pandas as pd
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from src.data.preprocess import HeartDiseasePreprocessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'api_requests_total',
    'Total number of API requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'api_request_duration_seconds',
    'API request duration in seconds',
    ['method', 'endpoint']
)

PREDICTION_COUNT = Counter(
    'predictions_total',
    'Total number of predictions made',
    ['prediction_class']
)

# Global variables for model and preprocessor
model: Optional[object] = None
preprocessor: Optional[HeartDiseasePreprocessor] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    logger.info("Starting Heart Disease Prediction API...")
    load_model()
    if model is not None and preprocessor is not None:
        logger.info("API ready to serve predictions")
    else:
        logger.warning("API started but models not loaded. /predict endpoint will not work until models are copied to pod.")
    yield
    # Shutdown (if needed)
    logger.info("Shutting down API...")


# Initialize FastAPI app
app = FastAPI(
    title="Heart Disease Prediction API",
    description="MLOps API for predicting heart disease risk",
    version="1.0.0",
    lifespan=lifespan
)


class HeartDiseaseInput(BaseModel):
    """Input schema for prediction"""
    age: float = Field(..., ge=0, le=120, description="Age in years")
    sex: int = Field(..., ge=0, le=1, description="Sex (0=female, 1=male)")
    cp: int = Field(..., ge=0, le=3, description="Chest pain type (0-3)")
    trestbps: float = Field(..., ge=0, description="Resting blood pressure")
    chol: float = Field(..., ge=0, description="Serum cholesterol")
    fbs: int = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dl")
    restecg: int = Field(..., ge=0, le=2, description="Resting electrocardiographic results")
    thalach: float = Field(..., ge=0, description="Maximum heart rate achieved")
    exang: int = Field(..., ge=0, le=1, description="Exercise induced angina")
    oldpeak: float = Field(..., ge=0, description="ST depression induced by exercise")
    slope: int = Field(..., ge=0, le=2, description="Slope of peak exercise ST segment")
    ca: float = Field(..., ge=0, le=4, description="Number of major vessels colored by flourosopy")
    thal: float = Field(..., ge=0, le=3, description="Thalassemia (0-3)")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "age": 63,
                "sex": 1,
                "cp": 3,
                "trestbps": 145,
                "chol": 233,
                "fbs": 1,
                "restecg": 0,
                "thalach": 150,
                "exang": 0,
                "oldpeak": 2.3,
                "slope": 0,
                "ca": 0,
                "thal": 1
            }
        }
    }


class PredictionOutput(BaseModel):
    """Output schema for prediction"""
    prediction: int = Field(..., description="Predicted class (0=No Disease, 1=Disease)")
    probability: float = Field(..., description="Probability of heart disease")
    confidence: str = Field(..., description="Confidence level")


def load_model():
    """Load the trained model and preprocessor"""
    global model, preprocessor
    
    model_path = os.getenv("MODEL_PATH", "models/best_model.pkl")
    preprocessor_path = os.getenv("PREPROCESSOR_PATH", "models/preprocessor.pkl")
    
    try:
        # Load model
        if os.path.exists(model_path):
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            logger.info(f"Model loaded from {model_path}")
        else:
            logger.warning(f"Model file not found at {model_path}. API will start but /predict will fail.")
            logger.warning("Copy models to pod using: kubectl cp models/best_model.pkl <pod>:/app/models/")
            model = None
        
        # Load preprocessor
        if os.path.exists(preprocessor_path):
            preprocessor = HeartDiseasePreprocessor.load(preprocessor_path)
            logger.info(f"Preprocessor loaded from {preprocessor_path}")
        else:
            logger.warning(f"Preprocessor file not found at {preprocessor_path}")
            logger.warning("Copy preprocessor to pod using: kubectl cp models/preprocessor.pkl <pod>:/app/models/")
            preprocessor = None
            
    except Exception as e:
        logger.error(f"Error loading model/preprocessor: {e}")
        model = None
        preprocessor = None




@app.post("/reload-models")
async def reload_models():
    """Reload models from disk (useful after copying models to pod)"""
    global model, preprocessor
    logger.info("Reloading models...")
    load_model()
    if model is not None and preprocessor is not None:
        return {"status": "success", "message": "Models reloaded successfully"}
    else:
        raise HTTPException(
            status_code=503,
            detail="Models not found. Please copy models to pod first."
        )


@app.get("/")
async def root():
    """Root endpoint"""
    REQUEST_COUNT.labels(method="GET", endpoint="/", status="200").inc()
    return {
        "message": "Heart Disease Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "/docs": "API documentation",
            "/health": "Health check",
            "/predict": "Make predictions (POST)"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    REQUEST_COUNT.labels(method="GET", endpoint="/health", status="200").inc()
    model_loaded = model is not None and preprocessor is not None
    status_code = 200 if model_loaded else 503
    return {
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "message": "Model not loaded" if not model_loaded else "OK"
    }


@app.post("/predict", response_model=PredictionOutput)
async def predict(input_data: HeartDiseaseInput):
    """
    Predict heart disease risk
    
    Args:
        input_data: Patient health data
        
    Returns:
        Prediction with probability and confidence
    """
    from prometheus_client import Summary
    
    with REQUEST_DURATION.labels(method="POST", endpoint="/predict").time():
        try:
            # Check if model is loaded
            if model is None or preprocessor is None:
                REQUEST_COUNT.labels(method="POST", endpoint="/predict", status="503").inc()
                raise HTTPException(
                    status_code=503,
                    detail="Model not loaded. Please copy models to pod: kubectl cp models/best_model.pkl <pod>:/app/models/"
                )
            
            # Log request
            logger.info(f"Prediction request received: {input_data.dict()}")
            
            # Convert input to DataFrame
            input_dict = input_data.dict()
            feature_order = [
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
            ]
            input_df = pd.DataFrame([input_dict], columns=feature_order)
            
            # Preprocess
            input_processed = preprocessor.transform(input_df)
            
            # Predict
            prediction = model.predict(input_processed)[0]
            probability = model.predict_proba(input_processed)[0][1]
            
            # Determine confidence
            if probability > 0.7:
                confidence = "high"
            elif probability > 0.4:
                confidence = "medium"
            else:
                confidence = "low"
            
            # Update metrics
            PREDICTION_COUNT.labels(prediction_class=str(prediction)).inc()
            REQUEST_COUNT.labels(method="POST", endpoint="/predict", status="200").inc()
            
            logger.info(f"Prediction: {prediction}, Probability: {probability:.4f}")
            
            return PredictionOutput(
                prediction=int(prediction),
                probability=float(probability),
                confidence=confidence
            )
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            REQUEST_COUNT.labels(method="POST", endpoint="/predict", status="500").inc()
            raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    REQUEST_COUNT.labels(method="GET", endpoint="/metrics", status="200").inc()
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

