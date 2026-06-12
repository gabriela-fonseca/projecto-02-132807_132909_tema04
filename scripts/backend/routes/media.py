from fastapi import APIRouter
from services.tmdb import search_movie

router = APIRouter()

@router.get("/movie")
def add_movie(title: str):

    movie = search_movie(title)

    if not movie:
        return {"error": "Filme não encontrado"}

    return movie