from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import os

# New path for the multilingual model
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"
MODEL_PATH = os.getenv("MODEL_PATH", f"/app/models/{MODEL_NAME}")

def load_model():
    if os.path.isdir(MODEL_PATH) and os.listdir(MODEL_PATH):
        # Load from the local folder (Fast!)
        print(f"Loading {MODEL_NAME} from local storage...")
        model = SentenceTransformer(MODEL_PATH)
    else:
        # First time: Download and save to the volume
        print(f"Downloading {MODEL_NAME} (this may take a few minutes)...")
        model = SentenceTransformer(MODEL_NAME)
        model.save(MODEL_PATH)
        print(f"Model saved to {MODEL_PATH}")
    return model

# To use it:
# model = load_model()
# embeddings = model.encode(["Eh boss, tapau satu!", "I am hungry"])

app = FastAPI()

# Add this block immediately after creating the 'app'
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://project2.duckdns.org", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    # This proves the backend is alive
    return {"status": "running", "environment": "production"}

@app.get("/api/db-test")
def test_db():
    # In Docker, 'db' is the hostname, not an IP!
    db_url = os.getenv("DATABASE_URL")
    return {"message": f"Connecting to {db_url}"}