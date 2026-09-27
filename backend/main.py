from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import json
from datetime import datetime


# ---------------------------------
# Create FastAPI application
# ---------------------------------

app = FastAPI()


# ---------------------------------
# CORS Configuration
# Allows React frontend to connect
# with FastAPI backend
# ---------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------
# Load trained ML model
# and TF-IDF vectorizer
# ---------------------------------

model = joblib.load("model/job_scam_model.pkl")
tfidf = joblib.load("model/tfidf_vectorizer.pkl")


# ---------------------------------
# History file
# ---------------------------------

HISTORY_FILE = "backend/history.json"


# ---------------------------------
# Input structure
# ---------------------------------

class JobInput(BaseModel):
    title: str
    company_profile: str
    description: str
    requirements: str
    benefits: str


# ---------------------------------
# Home API
# ---------------------------------

@app.get("/")
def home():
    return {
        "message": "Job Scam Detection API is running"
    }


# ---------------------------------
# Prediction API
# ---------------------------------

@app.post("/predict")
def predict_job(data: JobInput):

    # Combine all job information
    combined_text = (
        data.title + " " +
        data.company_profile + " " +
        data.description + " " +
        data.requirements + " " +
        data.benefits
    )


    # ---------------------------------
    # Convert text using TF-IDF
    # ---------------------------------

    job_vector = tfidf.transform([combined_text])


    # ---------------------------------
    # Machine Learning Prediction
    # ---------------------------------

    prediction = model.predict(job_vector)[0]
    probability = model.predict_proba(job_vector)[0]

    fraud_probability = round(
        float(probability[1]) * 100,
        2
    )

    legitimate_probability = round(
        float(probability[0]) * 100,
        2
    )


    # ---------------------------------
    # Final Prediction Result
    # ---------------------------------

    if prediction == 1:
        result = "Suspicious / Fraudulent Job"
    else:
        result = "Likely Legitimate Job"


    # ---------------------------------
    # Risk Level
    # ---------------------------------

    if fraud_probability >= 70:
        risk_level = "High"

    elif fraud_probability >= 40:
        risk_level = "Medium"

    else:
        risk_level = "Low"


    # ---------------------------------
    # Explanation / Warning Indicators
    # ---------------------------------

    reasons = []

    text_lower = combined_text.lower()


    suspicious_phrases = {

        # Payment related
        "registration fee":
            "Job asks for a registration fee",

        "pay fee":
            "Job mentions payment of a fee",

        "pay money":
            "Job asks the applicant to pay money",

        "processing fee":
            "Job asks for a processing fee",

        "security deposit":
            "Job asks for a security deposit",


        # Interview / experience related
        "no interview":
            "Job claims no interview is required",

        "no experience required":
            "Job claims no experience is required",


        # Fake promises
        "guaranteed job":
            "Job guarantees employment",

        "guaranteed income":
            "Job promises guaranteed income",

        "earn $5000":
            "Job contains an unusually high earning claim",

        "earn money fast":
            "Job promises unusually fast earnings",

        "work from home and earn":
            "Job uses a suspicious work-from-home earning claim",


        # Urgency
        "immediate joining":
            "Job uses urgent joining language",

        "join immediately":
            "Job asks for immediate joining",


        # Suspicious communication
        "whatsapp":
            "Job asks applicants to communicate through WhatsApp",

        "telegram":
            "Job asks applicants to communicate through Telegram",


        # Sensitive information
        "bank details":
            "Job asks for sensitive bank information",

        "account number":
            "Job asks for account details",

        "otp":
            "Job asks for an OTP, which is a serious warning sign",

        "aadhaar":
            "Job may be requesting sensitive identity information",

        "aadhar":
            "Job may be requesting sensitive identity information",

        "credit card":
            "Job asks for sensitive payment information",
    }


    # ---------------------------------
    # Check suspicious phrases
    # ---------------------------------

    for phrase, reason in suspicious_phrases.items():

        if phrase in text_lower:
            reasons.append(reason)


    # ---------------------------------
    # Check company profile
    # ---------------------------------

    if data.company_profile.strip().lower() in [
        "",
        "unknown",
        "unknown company",
        "not available",
        "n/a",
    ]:

        reasons.append(
            "Company profile is missing or unclear"
        )


    # ---------------------------------
    # Check job description length
    # ---------------------------------

    if len(data.description.strip()) < 40:

        reasons.append(
            "Job description contains very little information"
        )


    # ---------------------------------
    # Check requirements length
    # ---------------------------------

    if len(data.requirements.strip()) < 20:

        reasons.append(
            "Job requirements are too vague or incomplete"
        )


    # ---------------------------------
    # If no suspicious rule is detected
    # ---------------------------------

    if not reasons:

        reasons.append(
            "No obvious rule-based scam indicators were detected"
        )


    # ---------------------------------
    # Save prediction to history.json
    # ---------------------------------

    history_item = {
        "title": data.title,
        "result": result,
        "risk_level": risk_level,
        "fraud_probability": fraud_probability,
        "legitimate_probability": legitimate_probability,
        "reasons": reasons,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        history = []


    history.append(history_item)


    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            history,
            file,
            indent=4
        )


       # ---------------------------------
    # Send result to React frontend
    # ---------------------------------

    return {
        "result": result,
        "risk_level": risk_level,
        "fraud_probability": fraud_probability,
        "legitimate_probability": legitimate_probability,
        "reasons": reasons
    }


# ---------------------------------
# Get Prediction History API
# ---------------------------------

@app.get("/history")
def get_history():
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        history = []

    return history