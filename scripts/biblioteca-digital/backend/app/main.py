from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import filmes, pesquisa

# cria todas as tabelas na base de dados ao arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Biblioteca Digital",
    description="API para gerir uma biblioteca de filmes",
    version="1.0.0",
)

# permite que o frontend (a correr noutro porto) fale com a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(filmes.router, prefix="/filmes", tags=["Filmes"])
app.include_router(pesquisa.router, prefix="/pesquisa", tags=["Pesquisa TMDB"])


@app.get("/")
def raiz():
    return {"status": "ok", "mensagem": "Biblioteca Digital API"}
    

