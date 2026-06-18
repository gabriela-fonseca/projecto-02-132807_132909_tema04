from fastapi import APIRouter, HTTPException, Query
from app.tmdb_client import pesquisar_filmes, obter_detalhes_filme

router = APIRouter()


@router.get("/")
async def pesquisar(titulo: str = Query(..., min_length=2)):
    resultados = await pesquisar_filmes(titulo)
    return {"resultados": resultados}


@router.get("/{tmdb_id}")
async def detalhes(tmdb_id: int):
    filme = await obter_detalhes_filme(tmdb_id)
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado no TMDB")
    return filme
