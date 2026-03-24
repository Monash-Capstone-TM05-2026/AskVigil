from fastapi import FastAPI
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import os

# This path matches the 'volumes' we put in docker-compose.yml
MODEL_PATH = os.getenv("MODEL_PATH", "/app/models/distilbert")

def load_model():
    if os.path.exists(MODEL_PATH):
        # Load from the local folder (Fast!)
        tokenizer = DistilBertTokenizer.from_pretrained(MODEL_PATH)
        model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
    else:
        # If it's the very first time, download it and save it to the volume
        tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
        model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")
        tokenizer.save_pretrained(MODEL_PATH)
        model.save_pretrained(MODEL_PATH)
    return tokenizer, model

app = FastAPI()

@app.get("/api/health")
def health_check():
    # This proves the backend is alive
    return {"status": "running", "environment": "production"}

@app.get("/api/db-test")
def test_db():
    # In Docker, 'db' is the hostname, not an IP!
    db_url = os.getenv("DATABASE_URL")
    return {"message": f"Connecting to {db_url}"}