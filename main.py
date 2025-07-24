from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np

# Define Pydantic model
class PropertyFeatures(BaseModel):
    Area_sqft: float
    Bedrooms: int
    Bathrooms: int
    Location: str
    Age_years: float

# Initialize app
app = FastAPI(title="TruValue Property Price Predictor")

# Load model pipeline at startup
try:
    model = joblib.load("truvalue_model.pkl")
    print("✅ Model loaded successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

@app.post("/predict")
def predict_price(features: PropertyFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not available.")

    # Convert input to DataFrame
    input_df = pd.DataFrame([features.dict()])

    try:
        prediction = model.predict(input_df)
        predicted_price = max(0, float(np.round(prediction[0], 2)))  # Ensure no negative
        return {"predicted_price": predicted_price}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")
    
from fastapi import File, UploadFile
import threading
import io
from train_model import train_from_df

# Thread lock for concurrency control
model_lock = threading.Lock()

@app.post("/retrain")
async def retrain_model(file: UploadFile = File(...)):
    if file.content_type != 'text/csv':
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")

    try:
        # Read uploaded file contents
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))


        # Thread-safe model retraining
        with model_lock:
            new_model, _ = train_from_df(df)
            global model
            model = new_model

        return {"status": "✅ Model retrained and updated in memory."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")
