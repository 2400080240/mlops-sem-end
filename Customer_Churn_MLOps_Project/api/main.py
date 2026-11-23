from pathlib import Path
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "churn_model.pkl"

app = FastAPI(title="Customer Churn Prediction API", version="1.0.0")
model = None

class Customer(BaseModel):
    gender: str
    SeniorCitizen: int = Field(ge=0, le=1)
    Partner: str
    Dependents: str
    tenure: int = Field(ge=0, le=100)
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float = Field(ge=0)
    TotalCharges: float = Field(ge=0)

@app.on_event("startup")
def load_model():
    global model
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Run python src/train.py first.")
    model = joblib.load(MODEL_PATH)

@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
def predict(customer: Customer):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")
    row = pd.DataFrame([customer.model_dump()])
    try:
        prediction = int(model.predict(row)[0])
        probability = float(model.predict_proba(row)[0][1])
        return {"prediction": prediction, "churn_probability": probability}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
