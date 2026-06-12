from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Gestor de Biblioteca API"}

from database import engine
from models import Base

Base.metadata.create_all(bind=engine)

from routes.media import router as media_router

app.include_router(media_router)