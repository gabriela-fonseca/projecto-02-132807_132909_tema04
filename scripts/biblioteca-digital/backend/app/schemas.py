from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FilmeBase(BaseModel):
    titulo: str
    titulo_original: Optional[str] = None
    ano: Optional[int] = None
    nota: Optional[float] = None
    votos: Optional[int] = None
    popularidade: Optional[float] = None
    genero: Optional[str] = None
    genero_nome: Optional[str] = None
    cartaz_url: Optional[str] = None
    sinopse: Optional[str] = None
    duracao_min: Optional[int] = None
    tmdb_id: Optional[int] = None
    favorito: Optional[bool] = False
    quero_ver: Optional[bool] = False
    

class FilmeCriar(FilmeBase):
    # usado quando o utilizador envia dados para criar um filme
    # herda tudo do FilmeBase, sem adicionar nada por agora
    pass


class FilmeResposta(FilmeBase):
    # usado quando a API devolve um filme — inclui campos gerados pelo Postgres
    id: int
    adicionado_em: datetime

    class Config:
        from_attributes = True  # permite converter objeto SQLAlchemy → Pydantic
