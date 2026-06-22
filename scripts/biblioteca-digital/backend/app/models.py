from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Filme(Base):
    __tablename__ = "filmes"

    id = Column(Integer, primary_key=True, index=True)
    tmdb_id = Column(Integer, unique=True, nullable=True)
    titulo = Column(String(255), nullable=False)
    titulo_original = Column(String(255), nullable=True)
    ano = Column(Integer, nullable=True)
    nota = Column(Float, nullable=True)
    votos = Column(Integer, nullable=True)
    popularidade = Column(Float, nullable=True)
    genero = Column(String(100), nullable=True)
    genero_nome = Column(String(100), nullable=True)
    cartaz_url = Column(String(500), nullable=True)
    sinopse = Column(Text, nullable=True)
    duracao_min = Column(Integer, nullable=True)
    favorito = Column(Boolean, default=False, nullable=False)
    quero_ver = Column(Boolean, default=False, nullable=False)
    trailer_url = Column(String(500), nullable=True)
    adicionado_em = Column(DateTime(timezone=True), server_default=func.now())
