from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import FilmeCriar, FilmeResposta
from app import crud
from typing import Optional

router = APIRouter()


@router.get("/")
def listar_filmes(
    pesquisa: Optional[str] = Query(None),
    genero: Optional[str] = Query(None),
    nota_minima: Optional[float] = Query(None),
    ordenar: Optional[str] = Query("adicionado_em"),
    pagina: int = Query(1, ge=1),
    por_pagina: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    filmes, total = crud.obter_filmes(
        db, pesquisa, genero, nota_minima, ordenar, pagina, por_pagina
    )
    return {
        "total": total,
        "pagina": pagina,
        "por_pagina": por_pagina,
        "filmes": [FilmeResposta.model_validate(f) for f in filmes],
    }


@router.post("/", response_model=FilmeResposta, status_code=201)
def adicionar_filme(filme: FilmeCriar, db: Session = Depends(get_db)):
    if filme.tmdb_id and crud.filme_ja_existe(db, filme.tmdb_id):
        raise HTTPException(status_code=409, detail="Filme já existe na biblioteca")
    return crud.criar_filme(db, filme)


@router.get("/{filme_id}", response_model=FilmeResposta)
def obter_filme(filme_id: int, db: Session = Depends(get_db)):
    filme = crud.obter_filme_por_id(db, filme_id)
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme


@router.delete("/{filme_id}", status_code=204)
def apagar_filme(filme_id: int, db: Session = Depends(get_db)):
    if not crud.apagar_filme(db, filme_id):
        raise HTTPException(status_code=404, detail="Filme não encontrado")
