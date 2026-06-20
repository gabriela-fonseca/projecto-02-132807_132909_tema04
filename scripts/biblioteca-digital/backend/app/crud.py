from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Filme
from app.schemas import FilmeCriar
from typing import Optional


def criar_filme(db: Session, filme: FilmeCriar) -> Filme:
    db_filme = Filme(**filme.model_dump())
    db.add(db_filme)
    db.commit()
    db.refresh(db_filme)
    return db_filme


def obter_filmes(
    db: Session,
    pesquisa: Optional[str] = None,
    genero: Optional[str] = None,
    nota_minima: Optional[float] = None,
    ano_min: Optional[int] = None,
    ano_max: Optional[int] = None,
    apenas_favoritos: Optional[bool] = None,
    ordenar: Optional[str] = "adicionado_em",
    pagina: int = 1,
    por_pagina: int = 20,
) -> tuple[list[Filme], int]:
    query = db.query(Filme)

    if pesquisa:
        query = query.filter(
            or_(
                Filme.titulo.ilike(f"%{pesquisa}%"),
                Filme.sinopse.ilike(f"%{pesquisa}%"),
            )
        )

    if genero:
        query = query.filter(Filme.genero == genero)

    if nota_minima is not None:
        query = query.filter(Filme.nota >= nota_minima)

    if ano_min is not None:
        query = query.filter(Filme.ano >= ano_min)

    if ano_max is not None:
        query = query.filter(Filme.ano <= ano_max)

    if apenas_favoritos:
        query = query.filter(Filme.favorito == True)

    total = query.count()

    colunas_ordem = {
        "adicionado_em": Filme.adicionado_em.desc(),
        "nota": Filme.nota.desc(),
        "titulo": Filme.titulo.asc(),
        "ano": Filme.ano.desc(),
    }
    ordem = colunas_ordem.get(ordenar, Filme.adicionado_em.desc())
    query = query.order_by(ordem)

    offset = (pagina - 1) * por_pagina
    filmes = query.offset(offset).limit(por_pagina).all()

    return filmes, total

def obter_filme_por_id(db: Session, filme_id: int) -> Optional[Filme]:
    return db.query(Filme).filter(Filme.id == filme_id).first()


def filme_ja_existe(db: Session, tmdb_id: int) -> bool:
    return db.query(Filme).filter(Filme.tmdb_id == tmdb_id).first() is not None


def apagar_filme(db: Session, filme_id: int) -> bool:
    filme = obter_filme_por_id(db, filme_id)
    if not filme:
        return False
    db.delete(filme)
    db.commit()
    return True
    
def alternar_favorito(db: Session, filme_id: int) -> Optional[Filme]:
    filme = obter_filme_por_id(db, filme_id)
    if not filme:
        return None
    filme.favorito = not filme.favorito
    db.commit()
    db.refresh(filme)
    return filme
