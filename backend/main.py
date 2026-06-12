from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "API a funcionar 🚀"}

@app.get("/media")
def get_media():
    return {"media": []}