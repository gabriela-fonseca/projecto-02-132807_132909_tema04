import os
import httpx
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

TMDB_KEY = os.getenv("TMDB_API_KEY")
TMDB_BASE = "https://api.themoviedb.org/3"
TMDB_IMG = "https://image.tmdb.org/t/p/w342"
LANG = "pt-PT"

GENEROS_MAP = {
    28: "action", 12: "action", 35: "comedy", 80: "thriller",
    18: "drama", 27: "horror", 878: "scifi", 53: "thriller",
    9648: "thriller", 10749: "drama", 10752: "action",
}


async def pesquisar_filmes(titulo: str) -> list[dict]:
    if not TMDB_KEY:
        return []
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{TMDB_BASE}/search/movie",
            params={"api_key": TMDB_KEY, "query": titulo, "language": LANG},
            timeout=10,
        )
        resp.raise_for_status()
        resultados = resp.json().get("results", [])
        return [
            {
                "tmdb_id": m["id"],
                "titulo": m["title"],
                "ano": m["release_date"][:4] if m.get("release_date") else None,
                "nota": round(m["vote_average"], 1) if m.get("vote_average") else None,
                "cartaz_url": f"{TMDB_IMG}{m['poster_path']}" if m.get("poster_path") else None,
            }
            for m in resultados[:8]
        ]


async def obter_trailer(tmdb_id: int) -> Optional[str]:
    if not TMDB_KEY:
        return None
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{TMDB_BASE}/movie/{tmdb_id}/videos",
            params={"api_key": TMDB_KEY, "language": LANG},
            timeout=10,
        )
        resp.raise_for_status()
        videos = resp.json().get("results", [])

        trailer = next(
            (v for v in videos if v["site"] == "YouTube" and v["type"] == "Trailer"),
            None,
        )

        if not trailer:
            resp_en = await client.get(
                f"{TMDB_BASE}/movie/{tmdb_id}/videos",
                params={"api_key": TMDB_KEY},
                timeout=10,
            )
            videos_en = resp_en.json().get("results", [])
            trailer = next(
                (v for v in videos_en if v["site"] == "YouTube" and v["type"] == "Trailer"),
                None,
            )

        if trailer:
            return f"https://www.youtube.com/embed/{trailer['key']}"
        return None


async def obter_detalhes_filme(tmdb_id: int) -> Optional[dict]:
    if not TMDB_KEY:
        return None
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{TMDB_BASE}/movie/{tmdb_id}",
            params={"api_key": TMDB_KEY, "language": LANG},
            timeout=10,
        )
        resp.raise_for_status()
        m = resp.json()

        genero_id = m["genres"][0]["id"] if m.get("genres") else None
        genero_nome = m["genres"][0]["name"] if m.get("genres") else None

        trailer_url = await obter_trailer(tmdb_id)

        return {
            "tmdb_id": m["id"],
            "titulo": m["title"],
            "titulo_original": m.get("original_title"),
            "ano": int(m["release_date"][:4]) if m.get("release_date") else None,
            "nota": round(m["vote_average"], 1) if m.get("vote_average") else None,
            "votos": m.get("vote_count"),
            "popularidade": m.get("popularity"),
            "genero": GENEROS_MAP.get(genero_id, "other") if genero_id else None,
            "genero_nome": genero_nome,
            "cartaz_url": f"{TMDB_IMG}{m['poster_path']}" if m.get("poster_path") else None,
            "sinopse": m.get("overview"),
            "duracao_min": m.get("runtime"),
            "trailer_url": trailer_url,
        }
