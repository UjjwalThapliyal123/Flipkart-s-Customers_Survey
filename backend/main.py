from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import logging
import os
import csv
import datetime

# -------------------- Logging Setup --------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("csat-api")

# -------------------- FastAPI App --------------------
app = FastAPI(
    title="CSAT Score Predictor API",
    version="1.0.0",
    description="Predicts Customer Satisfaction Score (1–5) based on customer service inputs"
)

# -------------------- CORS Middleware --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8501",
        "http://127.0.0.1:8501"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Load Artifacts on Startup --------------------
@app.on_event("startup")
def load_artifacts():
    global model, binary_encoder, preprocessor
    logger.info("🔧 Loading model and encoders...")
    model = joblib.load("backend/Artifacts/random_forest.pkl")
    binary_encoder = joblib.load("backend/Artifacts/binary_encoder.pkl")
    preprocessor = joblib.load("backend/Artifacts/preprocessor.pkl")
    logger.info("✅ Artifacts loaded successfully.")

# -------------------- Input Schema --------------------
class CustomerInput(BaseModel):
    channel_name: str
    category: str
    sub_category: str
    remarks: str
    city: str
    product: str
    tenure: str
    shift: str
    issue_reported_day: str
    issue_reported_month: str
    survey_response_day: str
    survey_response_month: str
    issue_time: int = Field(..., ge=0, le=1440)
    response_time: int = Field(..., ge=0, le=1440)
    handling_time: int = Field(..., ge=0, le=1440)
    agent_experience: str
    handle_bucket: str

# -------------------- Root Endpoint --------------------
@app.get("/")
def read_root():
    return {"status": "ok"}

# -------------------- Prediction Endpoint --------------------
@app.post("/predict")
def predict(input: CustomerInput):
    try:
        logger.info("📨 Received prediction request.")

        # Input mapping
        data_dict = {
            'channel_name': input.channel_name,
            'category': input.category,
            'Sub-category': input.sub_category,
            'Customer Remarks': input.remarks,
            'Customer_City': input.city,
            'Product_category': input.product,
            'Tenure Bucket': input.tenure,
            'Agent Shift': input.shift,
            'Issue_reported_day_Name': input.issue_reported_day,
            'Issue_reported_month': input.issue_reported_month,
            'Survey_response_Day_Name': input.survey_response_day,
            'Survey_response_Date_month': input.survey_response_month,
            'Issue_reported_time_minutes': input.issue_time,
            'issue_responded_time_minutes': input.response_time,
            'Handling_Time_minutes': input.handling_time,
            'Agent Experience Level': input.agent_experience,
            'Handling Bucket': input.handle_bucket
        }

        # Convert to DataFrame
        df = pd.DataFrame([data_dict])
        logger.info("🔄 Input converted to DataFrame")

        # Transform input
        df_encoded = binary_encoder.transform(df)
        df_preprocessed = preprocessor.transform(df_encoded)

        # Prediction
        logger.info("🧠 Making prediction...")
        prediction = model.predict(df_preprocessed)[0]

        # Probability (optional)
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(df_preprocessed)[0]
            probabilities = {str(i + 1): round(float(p), 4) for i, p in enumerate(proba)}
        else:
            probabilities = {}

        # Mood logic
        mood = (
            "😞 Unsatisfied" if prediction <= 2
            else "😐 Neutral" if prediction == 3
            else "😄 Satisfied"
        )

        logger.info(f"✅ Prediction complete: {prediction} ({mood})")

        # -------------------- Logging to CSV --------------------
        log_data = data_dict.copy()
        log_data["prediction"] = int(prediction)
        log_data["mood"] = mood
        log_data["timestamp"] = datetime.datetime.now().isoformat()

        log_path = "storage/predictions.csv"
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        write_header = not os.path.exists(log_path)

        with open(log_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=log_data.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(log_data)

        # -------------------- Return Response --------------------
        return {
            "satisfaction_prediction": int(prediction),
            "mood": mood,
            "probabilities": probabilities
        }

    except Exception as e:
        logger.error(f"❌ Error during prediction: {e}")
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")
